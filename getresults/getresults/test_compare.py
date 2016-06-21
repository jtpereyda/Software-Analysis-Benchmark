from . import compare
from . import benchmark

sample_errors = [{'file': 'f1',
                  'line': 1,
                  'subtype': '1',
                  'type': 'A'},
                 {'file': 'f2',
                  'line': 22,
                  'subtype': '2',
                  'type': 'A'},
                 {'file': 'f3',
                  'line': 22,
                  'subtype': '3',
                  'type': 'A'},
                 {'file': 'f4',
                  'line': 22,
                  'subtype': '1',
                  'type': 'B'},
                 {'file': 'f5',
                  'line': 22,
                  'subtype': '1',
                  'type': 'C'},
                 ]

sample_nonerrors = [{'file': 'f1',
                     'line': 1,
                     'subtype': '1',
                     'type': 'A'},
                    {'file': 'f2',
                     'line': 22,
                     'subtype': '2',
                     'type': 'A'},
                    {'file': 'f6',
                     'line': 22,
                     'subtype': '3',
                     'type': 'Z'},
                    {'file': 'Y',
                     'line': 22,
                     'subtype': '1',
                     'type': 'Y'},
                    {'file': 'f5',
                     'line': 22,
                     'subtype': '1',
                     'type': 'X'},
                    ]


class TestDefectTypes:
    def test_result(self):
        """
        Given Sample data
        When Calling Compare.defect_types
        Then Result contains defect types from sample data's errors and nonerrors.
        """
        sample = benchmark.Benchmark(sample_errors, sample_nonerrors)
        c = compare.Compare(sample, None)
        assert c.defect_types == {'A', 'B', 'C', 'X', 'Y', 'Z'}
