import asyncio
import time
from blackteam.evaluator import evaluate, evaluate_tool_calls
from blackteam.storage.sqlite import Storage


class Engine:
    def __init__(self, db_path=":memory:"):
        self.storage = Storage(db_path)

    def run_single(self, provider, attack, target):
        results = []
        prompts = attack.generate_prompts(target)

        for prompt in prompts:
            start = time.time()
            result = provider.send_prompt(prompt)
            duration = int((time.time() - start) * 1000)

            eval_result = evaluate(result.response, target)

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
            )
            self.storage.save_turn(run_id, 1, "user", prompt)
            self.storage.save_turn(run_id, 2, "assistant", result.response)

            results.append({
                "run_id": run_id,
                "prompt": prompt[:100],
                "verdict": eval_result["verdict"],
                "confidence": eval_result["confidence"],
                "response_preview": result.response[:200],
            })

        return results

    def run_multi_turn(self, provider, attack, target):
        turns = attack.generate_turns(target)
        messages = []
        all_responses = []

        start = time.time()
        for turn_text in turns:
            messages.append({"role": "user", "content": turn_text})
            result = provider.send_in_conversation(messages)
            messages.append({"role": "assistant", "content": result.response})
            all_responses.append(result.response)

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
        )

        for i, (user_msg, assistant_msg) in enumerate(zip(turns, all_responses)):
            self.storage.save_turn(run_id, i * 2 + 1, "user", user_msg)
            self.storage.save_turn(run_id, i * 2 + 2, "assistant", assistant_msg)

        return {
            "run_id": run_id,
            "turns": len(turns),
            "verdict": eval_result["verdict"],
            "confidence": eval_result["confidence"],
            "final_response_preview": all_responses[-1][:200] if all_responses else "",
        }

    def run_tool_use(self, provider, attack, target):
        tools = attack.get_tools()
        messages_text = attack.generate_tool_messages(target, tools=tools)
        messages = []
        all_tool_calls = []
        all_responses = []

        start = time.time()
        for msg_text in messages_text:
            messages.append({"role": "user", "content": msg_text})
            result = provider.send_with_tools(messages, tools)

            # Record tool calls
            for call in result.tool_calls:
                all_tool_calls.append(call)
                # Simulate a generic tool response so the conversation can continue
                messages.append({"role": "assistant", "content": [
                    {"type": "tool_use", "id": call["id"], "name": call["tool"], "input": call["input"]}
                ]})
                messages.append({"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": call["id"],
                     "content": f"[simulated] Tool '{call['tool']}' called with {call['input']}"}
                ]})

            if result.response:
                all_responses.append(result.response)
                if not result.tool_calls:
                    messages.append({"role": "assistant", "content": result.response})

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
            tokens_in=None, tokens_out=None,
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

    def run(self, provider, attack, target):
        if attack.mode == "tool-use":
            return self.run_tool_use(provider, attack, target)
        elif attack.mode == "multi-turn":
            return self.run_multi_turn(provider, attack, target)
        else:
            return self.run_single(provider, attack, target)

    # ── Async parallel execution ──────────────────────────────────────

    async def run_batch_async(self, provider, attacks, target, max_workers=5, on_complete=None):
        semaphore = asyncio.Semaphore(max_workers)
        results = []
        db_path = self.storage.db_path

        async def _run_one(attack):
            async with semaphore:
                try:
                    # Each thread gets its own Engine + Storage to avoid SQLite thread issues
                    def _run_in_thread():
                        thread_engine = Engine(db_path=db_path)
                        return thread_engine.run(provider, attack, target)

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
        return results

    def run_batch_parallel(self, provider, attacks, target, max_workers=5, on_complete=None):
        return asyncio.run(
            self.run_batch_async(provider, attacks, target, max_workers, on_complete)
        )
