import argparse

import tabulate

from . import benchmark_parse
from . import sonarqube
from . import compare
__version__ = "0.0.1.dev1"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("testbench_dir", help="file or directory to search for expected errors")
    arguments = parser.parse_args(args=argv[1:])

    expected = benchmark_parse.parse_benchmarks(arguments.testbench_dir)

    qube_results = sonarqube.get_sonarqube_data(
        "http://sonarqube.ad.selinc.com/api/issues/search?projectKeys=org.sonarqube:seceng-toyota-software-analysis-benchmarks")

    comparison = compare.Compare(expected, qube_results)

    import pprint
    pprint.pprint(comparison.results_by_category)

    print(
        tabulate.tabulate(
            (
                defect_type,
                sum(error["type"] == defect_type for error in expected.errors),
                # comparison.results_by_category[defect_type],
                sum(nonerror["type"] == defect_type for nonerror in expected.nonerrors)
            ) for defect_type in comparison.defect_types))

    print(len(expected.errors))
    print(len(expected.nonerrors))

    # import pprint
    # pprint.pprint(expected.errors)
    # pprint.pprint(qube_results)
