import asyncio
import time
from blackteam.evaluator import evaluate
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

    def run(self, provider, attack, target):
        if attack.mode == "multi-turn":
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
