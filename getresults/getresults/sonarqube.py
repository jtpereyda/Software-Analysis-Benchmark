import json

import math
import requests


def get_sonarqube_data(url):
    return format_sonarqube_data(query_sonarqube_data(url=url))


def query_sonarqube_data(url):
    data = json.loads(requests.get(url=url).text)
    page_size = data['ps']
    total = data['total']
    total_pages = math.ceil(total/page_size)
    for i in range(2, total_pages+1):
        data.update(json.loads(requests.get(url=url, data={'p': i}).text))
    return data


def format_sonarqube_data(json_object):
    components_by_key = {component['key']: component for component in json_object['components']}
    return [
        {'file': components_by_key[issue['component']]['path'],
         'line': issue['textRange']['startLine']}
        for issue in json_object['issues'] if 'textRange' in issue]
