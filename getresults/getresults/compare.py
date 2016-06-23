import functools
import itertools
import os

from .benchmark import Benchmark
from typing import List, Dict, Any
from cached_property import cached_property


class Compare:
    def __init__(self, expected_benchmark: Benchmark, actual_results: List[Dict[str, Any]]):
        """

        Args:
            expected_benchmark: Benchmark data.
            actual_results (list): Actual findings.
        """
        self._expected_benchmark = expected_benchmark
        self._actual_results = actual_results

    @cached_property
    def defect_types(self) -> List[str]:
        """
        Return list of finding types in the expected_benchmark.

        Returns: List of finding types in the expected_benchmark.
        """
        defect_types = set()
        for error in itertools.chain(self._expected_benchmark.errors, self._expected_benchmark.nonerrors):
            defect_types.add(error["type"])
        return defect_types

    @cached_property
    def issues_found(self) -> List[Dict[str, Any]]:
        """
        Return list of expected issues actually found in actual_results.

        Returns: List of found issues.
        """
        issues_found = []
        for expected_issue in self._expected_benchmark.errors:
            for actual_issue in self._actual_results:
                if self._match_filenames(actual_issue["file"], expected_issue["file"]) and actual_issue["line"] == expected_issue["line"]:
                    issues_found.append(expected_issue)
                    break
        return issues_found

    @functools.lru_cache(maxsize=10000)
    def _match_filenames(self, l, r) -> bool:
        """
        Loose match on two filenames. Matches only the file and its immediate parent directory.

        Note: This implementation uses os.path.split, which is somewhat slow when called many times. Caching is used
        to help mitigate this slowness.

        Args:
            l: filename
            r: filename

        Returns: True if the filenames appear to match, False otherwise.
        """
        l_dir, l_file = os.path.split(l)
        _, l_immediate_dir = os.path.split(l_dir)
        r_dir, r_file = os.path.split(r)
        _, r_immediate_dir = os.path.split(r_dir)
        return l_file == r_file and l_immediate_dir == r_immediate_dir

    @cached_property
    def results_by_category(self) -> Dict[str, Dict[str, Any]]:
        """
        Return result stats by finding type.

        Returns: Dictionary mapping finding tpes to stats for that type. There is also a 'total' type with stats for
        all types.
        """
        results = {}
        for defect_type in self.defect_types:
            expected = sum(1 for issue in self._expected_benchmark.errors if issue['type'] == defect_type)
            found = sum(1 for issue in self.issues_found if issue['type'] == defect_type)
            results[defect_type] = {'expected': expected, 'found': found, 'detection_rate': self._detection_rate(
                expected, found)}
        return results

    def _detection_rate(self, expected, found):
        try:
            return found / expected
        except ZeroDivisionError:
            return 1
