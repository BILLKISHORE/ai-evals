import asyncio
import time
from ai_blackteam.evaluator import evaluate, evaluate_tool_calls
from ai_blackteam.logging_config import get_logger
from ai_blackteam.signals import SIGNAL_REASONING, has_content, resolve_signal
from ai_blackteam.storage.sqlite import Storage

logger = get_logger("engine")


def _json_or_none(details):
    """stop_details is a dict from the provider; the store holds TEXT."""
    if not details:
        return None
    import json
    return json.dumps(details, sort_keys=True)




class _Total:
    """A running sum that stays None until something is actually reported.

    Summing straight into 0 would turn "the vendor told us nothing" into
    "this cost nothing", which is the failure-becomes-a-plausible-value
    pattern this codebase keeps tripping over. A reported 0 is a real
    measurement and is kept as 0.
    """

    __slots__ = ("value",)

    def __init__(self):
        self.value = None

    def add(self, n):
        if not isinstance(n, int) or isinstance(n, bool):
            return
        self.value = n if self.value is None else self.value + n



# An attack whose declared channel came back empty measured nothing. ERROR is
# already the non-scoring verdict (see scoring.NON_SCORING_VERDICTS), so it is
# excluded from bypass-rate maths rather than counted as a block.
_UNMEASURED = {
    "verdict": "ERROR",
    "keyword_score": 0,
    "regex_matches": 0,
    "confidence": 0.0,
}


def _evaluate_channels(result, target, signal):
    """Score the answer, and the thinking when there is any.

    Returns (run_eval, response_verdict, reasoning_verdict). The run verdict
    comes from the channel the attack declared; both channel verdicts are
    recorded either way, because the disagreement between them is the finding
    a reasoning-layer attack is looking for.
    """
    response_eval = evaluate(result.response, target)
    reasoning_eval = None
    if has_content(result.reasoning):
        reasoning_eval = evaluate(result.reasoning, target)

    response_verdict = response_eval["verdict"]
    reasoning_verdict = reasoning_eval["verdict"] if reasoning_eval else None

    if signal != SIGNAL_REASONING:
        return response_eval, response_verdict, reasoning_verdict
    if reasoning_eval is None:
        # Scoring the answer here would report a refusal for a run that never
        # produced the evidence the attack depends on.
        return dict(_UNMEASURED), response_verdict, None
    return reasoning_eval, response_verdict, reasoning_verdict


class Engine:
    def __init__(self, db_path=":memory:"):
        self.storage = Storage(db_path)

    def run_single(self, provider, attack, target, system_prompt=None,
                    verify=False, verify_llm=False):
        logger.info(f"Running {attack.technique_id} (single-turn) against target")
        results = []
        signal = resolve_signal(attack)
        prompts = attack.generate_prompts(target)
        vuln_samples = attack.get_samples() if verify and hasattr(attack, 'get_samples') else None

        for i, prompt in enumerate(prompts):
            try:
                start = time.time()
                result = provider.send_prompt(prompt, system_prompt=system_prompt)
                duration = int((time.time() - start) * 1000)

                eval_result, response_verdict, reasoning_verdict = _evaluate_channels(
                    result, target, signal)
                logger.info(f"Attack {attack.technique_id} prompt {i+1}/{len(prompts)}: {eval_result['verdict']}")
                logger.debug(f"Response preview: {result.response[:100]}")

                verify_status = None
                verify_confidence = None
                verify_ground_truth = None
                if verify:
                    from ai_blackteam.verifier import combined_verify
                    sample_idx = i // 3 if vuln_samples else None
                    vuln_info = vuln_samples[sample_idx] if vuln_samples and sample_idx is not None and sample_idx < len(vuln_samples) else None
                    v_result = combined_verify(result.response, vuln_info=vuln_info, use_llm=verify_llm)
                    verify_status = v_result.status
                    verify_confidence = v_result.confidence
                    verify_ground_truth = v_result.ground_truth_match

                run_id = self.storage.save_run(
                    provider=result.provider, model=result.model,
                    attack=attack.technique_id, target=target,
                    mode="single-turn", verdict=eval_result["verdict"],
                    keyword_score=eval_result["keyword_score"],
                    regex_matches=eval_result["regex_matches"],
                    llm_judge_score=None,
                    confidence=eval_result["confidence"],
                    duration_ms=duration,
                    tokens_in=result.tokens_in,
                    tokens_out=result.tokens_out,
                    verify_status=verify_status,
                    verify_confidence=verify_confidence,
                    verify_ground_truth=verify_ground_truth,
                    stop_reason=result.stop_reason,
                    stop_details=_json_or_none(result.stop_details),
                    # Absent means the vendor did not report one, which is
                    # NULL rather than a fabricated zero.
                    reasoning_tokens=result.reasoning_tokens,
                    response_verdict=response_verdict,
                    reasoning_verdict=reasoning_verdict,
                )
                self.storage.save_turn(run_id, 1, "user", prompt)
                self.storage.save_turn(run_id, 2, "assistant", result.response)
                # Stored under its own role, not merged into the assistant
                # turn: reasoning-layer attacks put harmful content in the
                # thinking while the answer stays clean, so the two have to
                # stay separable when scoring.
                if result.reasoning:
                    self.storage.save_turn(run_id, 2, "reasoning", result.reasoning)

                results.append({
                    "run_id": run_id,
                    "prompt": prompt[:100],
                    "verdict": eval_result["verdict"],
                    "confidence": eval_result["confidence"],
                    "verify_status": verify_status,
                    "verify_confidence": verify_confidence,
                    "response_preview": result.response[:200],
                })
            except Exception as e:
                logger.error(f"Attack {attack.technique_id} prompt {i+1} failed: {e}")
                results.append({
                    "run_id": None,
                    "prompt": prompt[:100],
                    "verdict": "ERROR",
                    "confidence": 0.0,
                    "response_preview": str(e)[:200],
                    "error": str(e),
                })

        return results

    def run_multi_turn(self, provider, attack, target, system_prompt=None):
        logger.info(f"Running {attack.technique_id} (multi-turn) against target")
        turns = attack.generate_turns(target)
        messages = []
        all_responses = []

        start = time.time()
        try:
            for turn_text in turns:
                messages.append({"role": "user", "content": turn_text})
                result = provider.send_in_conversation(messages, system_prompt=system_prompt)
                messages.append({"role": "assistant", "content": result.response})
                all_responses.append(result.response)
        except Exception as e:
            logger.error(f"Attack {attack.technique_id} multi-turn failed at turn {len(all_responses) + 1}: {e}")
            if not all_responses:
                return {
                    "run_id": None,
                    "turns": 0,
                    "verdict": "ERROR",
                    "confidence": 0.0,
                    "final_response_preview": "",
                    "error": str(e),
                }

        duration = int((time.time() - start) * 1000)
        combined = " ".join(all_responses)
        eval_result = evaluate(combined, target)

        run_id = self.storage.save_run(
            provider=result.provider, model=result.model,
            attack=attack.technique_id, target=target,
            mode="multi-turn", verdict=eval_result["verdict"],
            keyword_score=eval_result["keyword_score"],
            regex_matches=eval_result["regex_matches"],
            llm_judge_score=None,
            confidence=eval_result["confidence"],
            duration_ms=duration,
            tokens_in=result.tokens_in,
            tokens_out=result.tokens_out,
            stop_reason=result.stop_reason,
            stop_details=_json_or_none(result.stop_details),
            # Absent stays NULL, never a fabricated zero.
            reasoning_tokens=result.reasoning_tokens,
        )

        for i, (user_msg, assistant_msg) in enumerate(zip(turns, all_responses)):
            self.storage.save_turn(run_id, i * 2 + 1, "user", user_msg)
            self.storage.save_turn(run_id, i * 2 + 2, "assistant", assistant_msg)
        if getattr(result, "reasoning", None):
            self.storage.save_turn(run_id, len(turns) * 2, "reasoning", result.reasoning)

        return {
            "run_id": run_id,
            "turns": len(turns),
            "verdict": eval_result["verdict"],
            "confidence": eval_result["confidence"],
            "final_response_preview": all_responses[-1][:200] if all_responses else "",
        }

    def run_tool_use(self, provider, attack, target, system_prompt=None):
        logger.info(f"Running {attack.technique_id} (tool-use) against target")
        tools = attack.get_tools()
        messages_text = attack.generate_tool_messages(target, tools=tools)
        custom_responses = attack.get_tool_responses() if hasattr(attack, 'get_tool_responses') else None
        messages = []
        all_tool_calls = []
        all_responses = []
        last_stop_reason = None
        last_stop_details = None
        # Summed across the loop, because the cost of a tool-use run is the
        # whole conversation, not its final leg. _Total keeps "nothing was
        # ever reported" (None) distinct from "reported as zero" (0).
        total_tokens_in = _Total()
        total_tokens_out = _Total()
        total_reasoning_tokens = _Total()

        start = time.time()
        try:
            for msg_text in messages_text:
                messages.append({"role": "user", "content": msg_text})
                result = provider.send_with_tools(messages, tools, system_prompt=system_prompt)
                last_stop_reason = result.stop_reason
                last_stop_details = result.stop_details
                total_tokens_in.add(result.tokens_in)
                total_tokens_out.add(result.tokens_out)
                total_reasoning_tokens.add(result.reasoning_tokens)

                # Record tool calls
                for call in result.tool_calls:
                    all_tool_calls.append(call)
                    # Use custom response if available (for XPIA), otherwise generic
                    tool_name = call["tool"]
                    if custom_responses and tool_name in custom_responses:
                        sim_content = custom_responses[tool_name]
                    else:
                        sim_content = f"[simulated] Tool '{tool_name}' called with {call['input']}"
                    messages.append({"role": "assistant", "content": [
                        {"type": "tool_use", "id": call["id"], "name": tool_name, "input": call["input"]}
                    ]})
                    messages.append({"role": "user", "content": [
                        {"type": "tool_result", "tool_use_id": call["id"],
                         "content": sim_content}
                    ]})

                if result.response:
                    all_responses.append(result.response)
                    if not result.tool_calls:
                        messages.append({"role": "assistant", "content": result.response})
        except Exception as e:
            logger.error(f"Attack {attack.technique_id} tool-use failed: {e}")
            if not all_tool_calls and not all_responses:
                return {
                    "run_id": None,
                    "messages": 0,
                    "tool_calls": 0,
                    "sensitive_calls": 0,
                    "verdict": "ERROR",
                    "confidence": 0.0,
                    "error": str(e),
                }

        duration = int((time.time() - start) * 1000)

        # Evaluate based on tool calls, not text
        eval_result = evaluate_tool_calls(all_tool_calls, " ".join(all_responses) if all_responses else None)

        run_id = self.storage.save_run(
            provider=provider.get_model_info()["provider"],
            model=provider.model,
            attack=attack.technique_id, target=target,
            mode="tool-use", verdict=eval_result["verdict"],
            keyword_score=0, regex_matches=0,
            llm_judge_score=None,
            confidence=eval_result["confidence"],
            duration_ms=duration,
            # The ToolResult carried these all along; they used to be dropped
            # one line before the INSERT. OTora is a reasoning denial of
            # service whose success signal IS the reasoning burn, and tool-use
            # is the only mode it runs in, so discarding the count made the
            # one number that attack measures permanently unrecoverable.
            tokens_in=total_tokens_in.value, tokens_out=total_tokens_out.value,
            reasoning_tokens=total_reasoning_tokens.value,
            stop_reason=last_stop_reason,
            stop_details=_json_or_none(last_stop_details),
        )

        # Store each tool call
        for i, call in enumerate(all_tool_calls):
            is_sensitive = call in [sc for sc in eval_result.get("sensitive_calls", [])]
            self.storage.save_tool_call(
                run_id, i + 1, call["tool"],
                str(call["input"]),
                is_dangerous=is_sensitive,
            )

        # Store conversation turns
        for i, msg_text in enumerate(messages_text):
            self.storage.save_turn(run_id, i * 2 + 1, "user", msg_text)

        return {
            "run_id": run_id,
            "messages": len(messages_text),
            "tool_calls": len(all_tool_calls),
            "sensitive_calls": len(eval_result.get("sensitive_calls", [])),
            "verdict": eval_result["verdict"],
            "confidence": eval_result["confidence"],
        }

    def run(self, provider, attack, target, system_prompt=None, verify=False, verify_llm=False):
        if attack.mode == "tool-use":
            return self.run_tool_use(provider, attack, target, system_prompt=system_prompt)
        elif attack.mode == "multi-turn":
            return self.run_multi_turn(provider, attack, target, system_prompt=system_prompt)
        else:
            return self.run_single(provider, attack, target, system_prompt=system_prompt,
                                   verify=verify, verify_llm=verify_llm)

    # ── Async parallel execution ──────────────────────────────────────

    async def run_batch_async(self, provider, attacks, target, max_workers=5, on_complete=None, system_prompt=None):
        semaphore = asyncio.Semaphore(max_workers)
        results = []
        db_path = self.storage.db_path

        async def _run_one(attack):
            async with semaphore:
                try:
                    def _run_in_thread():
                        thread_engine = Engine(db_path=db_path)
                        return thread_engine.run(provider, attack, target, system_prompt=system_prompt)

                    result = await asyncio.to_thread(_run_in_thread)
                    entry = {"attack": attack.technique_id, "results": result, "error": None}
                except Exception as e:
                    entry = {"attack": attack.technique_id, "results": None, "error": str(e)}
            results.append(entry)
            if on_complete:
                on_complete(entry)
            return entry

        tasks = [_run_one(attack) for attack in attacks]
        await asyncio.gather(*tasks)
        errors = len([r for r in results if r.get("error")])
        logger.info(f"Batch complete: {len(results)} attacks, {errors} errors")
        return results

    def run_batch_parallel(self, provider, attacks, target, max_workers=5, on_complete=None, system_prompt=None):
        """Run a batch of attacks in parallel from a synchronous caller.

        Robust against three deployment shapes:
          * plain sync code (CLI, prefork Celery worker): ``asyncio.run`` works.
          * already-running loop (jupyter, FastAPI handler, async test):
            running ``asyncio.run`` would raise ``RuntimeError: This event
            loop is already running``. We off-thread the coroutine so we
            neither block nor re-enter the caller's loop.
          * gevent/eventlet monkey-patched worker: there is no asyncio loop
            but stdlib sockets are patched. Off-threading via a real OS thread
            also covers this path because ``concurrent.futures`` uses a real
            thread executor.
        """
        def _make_coro():
            return self.run_batch_async(
                provider, attacks, target, max_workers, on_complete,
                system_prompt=system_prompt,
            )

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # No running loop -- safe to start one.
            return asyncio.run(_make_coro())

        # A loop is already running. Off-thread the coroutine so we don't block
        # the caller's loop and don't re-enter it.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(lambda: asyncio.run(_make_coro()))
            return future.result()
