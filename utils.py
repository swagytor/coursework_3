import json
from datetime import date


def get_data_from_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def sort_data(operations_data):
    executed_data = [data for data in operations_data if data.get('state') == 'EXECUTED'][-7:]
    latest_data = sorted(executed_data, key=lambda x: x['date'], reverse=True)
    return latest_data


def parse_date(date_info, date_pattern='%d.%m.%Y'):
    date_of_operation, time_of_operation = date_info.split('T')
    iso_date = date.fromisoformat(date_of_operation)
    modified_date = date.strftime(iso_date, date_pattern)
    return modified_date


def parse_address(from_address, to_address):
    if to_address != 'Неизвестный получатель':
        to_address = parse_bank_info(to_address)
    if from_address != 'Неизвестный отправитель':
        from_address = parse_bank_info(from_address)
    return f'{from_address} -> {to_address}'


def parse_bank_info(bank_info):
    *bank_name, bank_address = bank_info.split()
    bank_address = list(bank_address)
    if bank_name[0] == 'Счет':
        bank_address = ['**'] + bank_address[-4:]
    else:
        bank_address[6:12] = ['*'] * 6
        [bank_address.insert(index, ' ') for index in range(-len(bank_address) + 4, 0, 4)]
    return " ".join((*bank_name, ''.join(bank_address)))


def parse_amount(amount_info):
    return f"{amount_info['amount']} {amount_info['currency']['name']}"


def show(info):
    from_info = info.get('from', 'Неизвестный отправитель')
    to_info = info.get('to', 'Неизвестный получатель')

    parsed_date = parse_date(info['date'])
    parsed_address = parse_address(from_info, to_info)
    parsed_amount = parse_amount(info['operationAmount'])

    print(parsed_date, info['description'])
    print(parsed_address)
    print(parsed_amount)
    print()



