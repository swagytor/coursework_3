import json


def get_data_from_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def sort_data(operations_data):
    executed_data = [data for data in operations_data if data.get('state') == 'EXECUTED'][-5:]
    latest_data = sorted(executed_data, key=lambda x: x['date'], reverse=True)
    return latest_data




