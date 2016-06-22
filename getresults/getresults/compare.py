import itertools
from .benchmark import Benchmark
from typing import List, Dict, Any


class Compare:
    def __init__(self, expected_benchmark: Benchmark, actual_results: List[Dict[str, Any]]):
        """

        Args:
            expected_benchmark: Benchmark data.
            actual_results (list): Actual findings.
        """
        self._expected_benchmark = expected_benchmark
        self._actual_results = actual_results

    @property
    def defect_types(self):
        defect_types = set()
        for error in itertools.chain(self._expected_benchmark.errors, self._expected_benchmark.nonerrors):
            defect_types.add(error["type"])
        return defect_types

    @property
    def issues_found(self):
        issues_found = []
        for expected_issue in self._expected_benchmark.errors:
            for actual_issue in self._actual_results:
                if actual_issue["file"] == expected_issue["file"] and actual_issue["line"] == expected_issue["line"]:
                    issues_found.append(expected_issue)
        return issues_found
