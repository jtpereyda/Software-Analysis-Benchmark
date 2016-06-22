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
    def defect_types(self) -> List[str]:
        """
        Return list of finding types in the expected_benchmark.

        Returns: List of finding types in the expected_benchmark.
        """
        defect_types = set()
        for error in itertools.chain(self._expected_benchmark.errors, self._expected_benchmark.nonerrors):
            defect_types.add(error["type"])
        return defect_types

    @property
    def issues_found(self) -> List[Dict[str, Any]]:
        """
        Return list of expected issues actually found in actual_results.

        Returns: List of found issues.
        """
        issues_found = []
        for expected_issue in self._expected_benchmark.errors:
            for actual_issue in self._actual_results:
                if actual_issue["file"] == expected_issue["file"] and actual_issue["line"] == expected_issue["line"]:
                    issues_found.append(expected_issue)
        return issues_found

    @property
    def results_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Return result stats by finding type.

        Returns: Dictionary mapping finding tpes to stats for that type. There is also a 'total' type with stats for
        all types.
        """
        pass
