import json


def scrapper_service_url():
    with open('environment/runtime.json') as runtime:
        runtime_json = json.load(runtime)
        with open('environment/environment.json') as environments:
            data = json.load(environments)
            url = data[runtime_json['run']]['scrapper_config_service']
            return url


def margin_saver_service_url():
    with open('environment/runtime.json') as runtime:
        runtime_json = json.load(runtime)
        with open('environment/environment.json') as environments:
            data = json.load(environments)
            url = data[runtime_json['run']]['margin_saver_service']
            return url
