from . import sonarqube
import pkg_resources
import json


class TestFormatSonarqubeData:
    def setup_method(self, _):
        resource_package = __name__
        json_data = pkg_resources.resource_string(resource_package, 'sample_sonarqube.json').decode('utf-8')
        self.results = sonarqube.format_sonarqube_data(json.loads(json_data))

    def test_sonarqube_sample_issue_1(self):
        assert {'file': '01.w_Defects/data_lost.c', 'line': 12} in self.results

    def test_sonarqube_sample_issue_2(self):
        assert {'file': '01.w_Defects/data_overflow.c', 'line': 13} in self.results

    def test_sonarqube_sample_issue_last(self):
        assert {'file': '02.wo_Defects/func_pointer.c', 'line': 234} in self.results
