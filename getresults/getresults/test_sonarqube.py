import copy

from . import sonarqube
import pkg_resources
import json

import unittest.mock as mock


def get_sample_file_contents():
        resource_package = __name__
        return pkg_resources.resource_string(resource_package, 'sample_sonarqube.json').decode('utf-8')


class TestFormatSonarqubeData:
    def setup_method(self, _):
        self.results = sonarqube.format_sonarqube_data(json.loads(get_sample_file_contents()))

    def test_sonarqube_sample_issue_1(self):
        assert {'file': '01.w_Defects/data_lost.c', 'line': 12} in self.results

    def test_sonarqube_sample_issue_2(self):
        assert {'file': '01.w_Defects/data_overflow.c', 'line': 13} in self.results

    def test_sonarqube_sample_issue_last(self):
        assert {'file': '02.wo_Defects/func_pointer.c', 'line': 234} in self.results


@mock.patch('getresults.sonarqube.requests')
class TestGetSonarQubeData:
    def setup_method(self, _):
        self.sonarqube_sample = json.loads(get_sample_file_contents())

    def test_requests_1_page(self, mock_requests):
        """
        Given Mock requests configured to return a data set with page info indicating one page
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 100
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_called_once_with(url='url')

    def test_requests_1_item(self, mock_requests):
        """
        Given Mock requests configured to return a data set with page info indicating a single entry
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 1
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_called_once_with(url='url')

    def test_requests_1_page_plus_1(self, mock_requests):
        """
        Given Mock requests configured to return a data set with paging info indicating one page plus one more item.
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 101
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_has_calls([mock.call(url='url'),
                                            mock.call(url='url', data={'p': 2})])

    def test_requests_2_pages(self, mock_requests):
        """
        Given Mock requests configured to return a data set with page info indicating two full pages, then return
            the second page
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 200
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_has_calls([mock.call(url='url'),
                                            mock.call(url='url', data={'p': 2})])

    def test_requests_3_pages(self, mock_requests):
        """
        Given Mock requests configured to return a data set with page info indicating three full pages, then return
            the second and third pages
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 300
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_has_calls([mock.call(url='url'),
                                            mock.call(url='url', data={'p': 2}),
                                            mock.call(url='url', data={'p': 3})])

    def test_requests_10_pages_plus_1(self, mock_requests):
        """
        Given Mock requests configured to return a data set with page info indicating three full pages, then return
            the second and third pages
        When Call get_sonarqube_data with a valid URL
        Then requests.get is called until the page number reaches the expected end.
        """
        json_one_page = copy.deepcopy(self.sonarqube_sample)
        json_one_page['ps'] = 100
        json_one_page['total'] = 1001
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': json.dumps(json_one_page)})})
        sonarqube.get_sonarqube_data('url')
        mock_requests.get.assert_has_calls(
            [mock.call(url='url')] + [mock.call(url='url', data={'p': i}) for i in range(2, 11)])
