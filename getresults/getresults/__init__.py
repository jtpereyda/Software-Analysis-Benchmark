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

    defect_types = comparison.defect_types
    defect_types.add('total')
    print(
        tabulate.tabulate(
            ((
                defect_type,
                comparison.results_by_category[defect_type]['expected'],
                comparison.results_by_category[defect_type]['found'],
                comparison.results_by_category[defect_type]['detection_rate'],
                sum(nonerror["type"] == defect_type for nonerror in expected.nonerrors)
            ) for defect_type in defect_types),
            headers=('Defect Type', 'Defect Variations', 'SonarQube', 'SonarQube DR', 'No-Defect Variations')
        )
    )

    print(len(expected.errors))
    print(len(expected.nonerrors))

    # import pprint
    # pprint.pprint(expected.errors)
    # pprint.pprint(qube_results)
