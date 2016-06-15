
def format_sonarqube_data(json_object):
    components_by_key = {component['key']: component for component in json_object['components']}
    return [
        {'file': components_by_key[issue['component']]['path'],
         'line': issue['textRange']['startLine']}
        for issue in json_object['issues'] if 'textRange' in issue]
