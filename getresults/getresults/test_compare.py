import unittest
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
    {'file': 'three/dir/levels',
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
    {'file': 'f2', 'line': 1},  # found another issue on the same line, should not count toward total
    {'file': 'g1', 'line': 1},  # found non-issue (false positive)
    {'file': 'f2', 'line': 2},  # found issue not in data set
    {'file': 'f3', 'line': 3},  # found issue not in data set
    {'file': 'dir/levels', 'line': 1},  # found issue with filename matching only two path levels
    {'file': 'flast', 'line': 999},  # found issue (true positive)
]

found_issues = [
    {'file': 'f1', 'line': 2, 'type': 'A', 'subtype': '2'},
    {'file': 'f2', 'line': 1, 'type': 'A', 'subtype': '3'},
    {'file': 'three/dir/levels', 'line': 1, 'type': 'C', 'subtype': '1'},
    {'file': 'flast', 'line': 999, 'type': 'C', 'subtype': '1'},
]


def _benchmark_object_factory():
    return benchmark.Benchmark(sample_errors, sample_nonerrors)


class TestDefectTypes(unittest.TestCase):
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


class TestFoundIssues(unittest.TestCase):
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


class TestResultsByCategory(unittest.TestCase):
    def setup_method(self, _):
        self._sample = _benchmark_object_factory()

    def test_results(self):
        """
        Given Sample data
        When Calling Compare.results_by_category
        Then Result contains expected result stats
        """
        c = compare.Compare(self._sample, sample_results)
        results = c.results_by_category
        assert results['A']['expected'] == 3
        assert results['A']['found'] == 2
        self.assertAlmostEqual(results['A']['detection_rate'], 2/3, places=3)

        assert results['B']['expected'] == 1
        assert results['B']['found'] == 0
        self.assertAlmostEqual(results['B']['detection_rate'], 0, places=3)

        assert results['C']['expected'] == 3
        assert results['C']['found'] == 2
        self.assertAlmostEqual(results['C']['detection_rate'], 2/3, places=3)

        assert results['X']['expected'] == 0
        assert results['X']['found'] == 0
        self.assertAlmostEqual(results['X']['detection_rate'], 1, places=3)

        assert results['Y']['expected'] == 0
        assert results['Y']['found'] == 0
        self.assertAlmostEqual(results['Y']['detection_rate'], 1, places=3)

        assert results['Z']['expected'] == 0
        assert results['Z']['found'] == 0
        self.assertAlmostEqual(results['Z']['detection_rate'], 1, places=3)

        assert results['total']['expected'] == 7
        assert results['total']['found'] == 4
        self.assertAlmostEqual(results['total']['detection_rate'], 4/7, places=3)
