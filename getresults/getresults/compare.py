import itertools


class Compare:
    def __init__(self, expected_benchmark, actual_results):
        self._expected_benchmark = expected_benchmark
        self._actual_results = actual_results

    @property
    def defect_types(self):
        defect_types = set()
        for error in itertools.chain(self._expected_benchmark.errors, self._expected_benchmark.nonerrors):
            defect_types.add(error["type"])
        return defect_types
