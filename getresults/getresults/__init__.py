import argparse

from . import benchmark_parse
__version__ = "0.0.1.dev1"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("testbench_dir", help="file or directory to search for expected errors")
    arguments = parser.parse_args(args=argv[1:])

    e = benchmark_parse.parse_benchmarks(arguments.testbench_dir)
    defect_types = set()
    for error in e.errors:
        defect_types.add(error["type"])
    for defect_type in defect_types:
        print("{0} -- {1}".format(defect_type, sum(error["type"] == defect_type for error in e.errors)))
    print(len(e.errors))
