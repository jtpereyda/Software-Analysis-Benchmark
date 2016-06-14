import argparse

import itertools
import tabulate

from . import benchmark_parse
__version__ = "0.0.1.dev1"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("testbench_dir", help="file or directory to search for expected errors")
    arguments = parser.parse_args(args=argv[1:])

    expected = benchmark_parse.parse_benchmarks(arguments.testbench_dir)
    defect_types = set()
    for error in itertools.chain(expected.errors, expected.nonerrors):
        defect_types.add(error["type"])

    print(
        tabulate.tabulate(
            (
                defect_type,
                sum(error["type"] == defect_type for error in expected.errors),
                sum(nonerror["type"] == defect_type for nonerror in expected.nonerrors)
            ) for defect_type in defect_types))

    print(len(expected.errors))
    print(len(expected.nonerrors))
