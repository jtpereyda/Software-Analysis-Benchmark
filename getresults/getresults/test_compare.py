from . import compare
from . import benchmark

sample_errors = [
    {'file': 'f1',
     'line': 1,
     'subtype': '1',
     'type': 'A'},
    {'file': 'f1',
     'line': 2,
     'subtype': '2',
     'type': 'A'},
    {'file': 'f2',
     'line': 1,
     'subtype': '3',
     'type': 'A'},
    {'file': 'f3',
     'line': 1,
     'subtype': '1',
     'type': 'B'},
    {'file': 'f4',
     'line': 1,
     'subtype': '1',
     'type': 'C'},
    {'file': 'flast',
     'line': 999,
     'subtype': '1',
     'type': 'C'},
]

sample_nonerrors = [
    {'file': 'g1',
     'line': 1,
     'subtype': '1',
     'type': 'A'},
    {'file': 'g1',
     'line': 2,
     'subtype': '2',
     'type': 'A'},
    {'file': 'g2',
     'line': 1,
     'subtype': '3',
     'type': 'Z'},
    {'file': 'g3',
     'line': 1,
     'subtype': '1',
     'type': 'Y'},
    {'file': 'g4',
     'line': 1,
     'subtype': '1',
     'type': 'X'},
]

sample_results = [
    {'file': 'f1', 'line': 2},  # found issue (true positive)
    {'file': 'f2', 'line': 1},  # found issue (true positive)
    {'file': 'g1', 'line': 1},  # found non-issue (false positive)
    {'file': 'f2', 'line': 2},  # found issue not in data set
    {'file': 'f3', 'line': 3},  # found issue not in data set
    {'file': 'flast', 'line': 999},  # found issue (true positive)
]

found_issues = [
    {'file': 'f1', 'line': 2, 'type': 'A', 'subtype': '2'},
    {'file': 'f2', 'line': 1, 'type': 'A', 'subtype': '3'},
    {'file': 'flast', 'line': 999, 'type': 'C', 'subtype': '1'},
]


def _benchmark_object_factory():
    return benchmark.Benchmark(sample_errors, sample_nonerrors)


class TestDefectTypes:
    def setup_method(self, _):
        self._sample = _benchmark_object_factory()

    def test_result(self):
        """
        Given Sample data
        When Calling Compare.defect_types
        Then Result contains defect types from sample data's errors and nonerrors
        """
        c = compare.Compare(self._sample, [])
        assert c.defect_types == {'A', 'B', 'C', 'X', 'Y', 'Z'}


class TestFoundIssues:
    def setup_method(self, _):
        self._sample = _benchmark_object_factory()

    def test_results(self):
        """
        Given Sample data
        When Calling Compare.issues_found
        Then Result contains exactly those findings which are in the expected and actual data sets
        """
        c = compare.Compare(self._sample, sample_results)
        for expected_issue in found_issues:
            assert any(actual_issue == expected_issue for actual_issue in c.issues_found), \
                "expected_issue {0} not found in c.issues_found {1}".format(expected_issue, c.issues_found)
