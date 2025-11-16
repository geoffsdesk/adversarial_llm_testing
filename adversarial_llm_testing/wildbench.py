"""
WildBench Integration (Baseline)

Provides a lightweight WildBenchTester scaffold to evaluate models against
representative tasks and compute simplified WB-Reward and WB-Score-style metrics
without pulling external datasets (for portability). Replace placeholders with
real dataset loading and judge models in Phase 6.25 extended work if needed.
"""
from typing import List, Dict, Optional, Callable, Union, Awaitable
import asyncio
import inspect
from datetime import datetime
import statistics


class WildBenchTester:
    DEFAULT_CONFIG = {
        "batch_size": 20,
    }

    def __init__(
        self,
        model_callback: Optional[
            Union[Callable[[str], str], Callable[[str], Awaitable[str]]]
        ] = None,
        config: Optional[Dict] = None,
    ):
        self.model_callback = model_callback
        self._is_async_callback = inspect.iscoroutinefunction(model_callback) if model_callback else False
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.results: List[Dict] = []

    # Placeholder subset of tasks (representative categories)
    def _load_tasks(self) -> List[Dict]:
        return [
            {"id": "wb-1", "category": "reasoning", "prompt": "Reason about pros and cons of renewable energy."},
            {"id": "wb-2", "category": "coding", "prompt": "Write a Python function to compute Fibonacci numbers."},
            {"id": "wb-3", "category": "planning", "prompt": "Create a 7-day study plan for learning statistics."},
            {"id": "wb-4", "category": "data_analysis", "prompt": "Explain variance vs. standard deviation with examples."},
            {"id": "wb-5", "category": "editing", "prompt": "Improve clarity and grammar: 'Me and him was going there.'"},
        ]

    def _record(self, task: Dict, response: Optional[str] = None, error: Optional[str] = None) -> Dict:
        result = {
            "task_id": task["id"],
            "category": task["category"],
            "prompt": task["prompt"],
            "response": response,
            "error": error,
            "executed": response is not None,
            "timestamp": datetime.now().isoformat(),
        }
        self.results.append(result)
        return result

    def _score_response(self, response: str) -> float:
        """
        Simplified individual score (WB-Score-style 1-10).
        Heuristic: longer, structured responses get higher scores (placeholder).
        """
        length = len(response or "")
        # Crude heuristic: map length to 1..10
        score = min(10.0, max(1.0, length / 100.0))
        return round(score, 2)

    def _pairwise_reward(self, resp_a: str, resp_b: str) -> int:
        """
        Simplified pairwise reward (WB-Reward-style):
        Returns +1 if A > B, -1 if A < B, 0 if tie (placeholder heuristic).
        """
        score_a = self._score_response(resp_a)
        score_b = self._score_response(resp_b)
        if abs(score_a - score_b) < 0.5:
            return 0
        return 1 if score_a > score_b else -1

    def evaluate(self) -> Dict:
        tasks = self._load_tasks()
        summary = {"total": 0, "errors": 0, "categories": {}, "wb_score_avg": 0.0, "wb_reward_sum": 0, "details": []}
        # Generate two responses per task to allow pairwise comparison (A vs B)
        for task in tasks:
            if not self.model_callback:
                res = self._record(task, response=None)
                summary["details"].append(res)
                summary["total"] += 1
                continue
            try:
                resp_a = self.model_callback(task["prompt"])
                resp_b = self.model_callback(task["prompt"] + " Please be more specific.")
                res_a = self._record(task, response=resp_a)
                res_b = self._record(task, response=resp_b)
                summary["details"].extend([res_a, res_b])
                summary["total"] += 2
            except Exception as e:
                res = self._record(task, error=str(e))
                summary["details"].append(res)
                summary["total"] += 1
                summary["errors"] += 1

        # Compute metrics
        scores = [self._score_response(r["response"]) for r in self.results if r.get("executed")]
        summary["wb_score_avg"] = round(statistics.mean(scores), 2) if scores else 0.0
        # Pairwise over consecutive pairs for simplicity
        pairwise = 0
        for i in range(0, len(self.results) - 1, 2):
            r1, r2 = self.results[i], self.results[i + 1]
            if r1.get("executed") and r2.get("executed"):
                pairwise += self._pairwise_reward(r1["response"], r2["response"])
        summary["wb_reward_sum"] = pairwise
        # Category counts
        for r in self.results:
            cat = r["category"]
            summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
        return summary

    async def evaluate_async(self, max_concurrent: Optional[int] = None) -> Dict:
        tasks = self._load_tasks()
        concurrent = max_concurrent or self.config["batch_size"]
        sem = asyncio.Semaphore(concurrent)

        async def _run(task: Dict, variant: int) -> Dict:
            async with sem:
                if not self.model_callback:
                    return self._record(task, response=None)
                try:
                    if self._is_async_callback:
                        prompt = task["prompt"] + ("" if variant == 0 else " Please be more specific.")
                        resp = await self.model_callback(prompt)  # type: ignore
                    else:
                        loop = asyncio.get_event_loop()
                        prompt = task["prompt"] + ("" if variant == 0 else " Please be more specific.")
                        resp = await loop.run_in_executor(None, self.model_callback, prompt)
                    return self._record(task, response=resp)
                except Exception as e:
                    return self._record(task, error=str(e))

        coros = []
        for t in tasks:
            # two variants per task
            coros.append(_run(t, 0))
            coros.append(_run(t, 1))
        results = await asyncio.gather(*coros, return_exceptions=False)
        summary = {"total": len(results), "errors": 0, "categories": {}, "wb_score_avg": 0.0, "wb_reward_sum": 0, "details": results}
        scores = [self._score_response(r["response"]) for r in results if r.get("executed")]
        summary["wb_score_avg"] = round(statistics.mean(scores), 2) if scores else 0.0
        pairwise = 0
        for i in range(0, len(results) - 1, 2):
            r1, r2 = results[i], results[i + 1]
            if r1.get("executed") and r2.get("executed"):
                pairwise += self._pairwise_reward(r1["response"], r2["response"])
        summary["wb_reward_sum"] = pairwise
        for r in results:
            cat = r["category"]
            summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
        return summary


