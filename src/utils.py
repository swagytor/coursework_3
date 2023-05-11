import json
from datetime import date
from pathlib import Path

PATH_TO_DATA = f"{Path(__file__).parent.parent}/data"
PATH_TO_JSON_DATA = f"{PATH_TO_DATA}/operations.json"

STARTING_INDEX_ENCRYPTED_SYMBOLS = 6
ENDING_INDEX_ENCRYPTED_SYMBOLS = 12
AMOUNT_OF_INFO = 5


def get_data_from_json(path: str = PATH_TO_JSON_DATA) -> list[dict]:
    """Возвращает список данных по банковских операциям"""
    # проверяем на наличие файла
    if Path(path).exists():
        with open(path) as json_file:
            json_data = json.load(json_file)
        return json_data
    else:
        raise FileNotFoundError


def sort_data(operations_data, amount: int = AMOUNT_OF_INFO) -> list[dict]:
    """
    Возвращает список N выполненных операций и сортируем по недавним операциям
    :param operations_data: данные по банковским операциями
    :param amount: количество возвращаемых данных
    :return: список N выполненных операций
    """
    executed_data = []

    for data in operations_data[::-1]:
        if data.get('state') == 'EXECUTED':
            executed_data.append(data)
            if len(executed_data) == amount:
                break

    # сортируем список по недавним успешным операциям
    latest_data = sorted(executed_data, key=lambda x: from_string_to_iso(x['date']), reverse=True)

    return latest_data


def from_string_to_iso(date_info: str) -> date:
    """
    Возвращает дату в ISO-формате
    :param date_info: дата и время в формате YYYY-MM-DDTHH:MM:SS
    :return: дату в ISO-формате YYYY-MM-DD
    """
    date_of_operation, time_of_operation = date_info.split('T')
    iso_date = date.fromisoformat(date_of_operation)
    return iso_date


def parse_date(date_info: str, date_pattern: str = '%d.%m.%Y') -> str:
    """
    Возвращает изменённый вид даты, согласно образцу даты
    :param date_info: дата и время в формате YYYY-MM-DDTHH:MM:SS
    :param date_pattern: образец даты
    :return: дату, согласно образцу даты
    """
    date_of_operation, time_of_operation = date_info.split('T')
    try:
        iso_date = date.fromisoformat(date_of_operation)
        modified_date = date.strftime(iso_date, date_pattern)
        return modified_date
    except ValueError:
        return 'Некорректный формат даты'


def parse_address(bank_info: dict) -> str:
    """
    Возвращает изменённый вид отправителя/получателя
    :param bank_info: информация об операции
    :return: информацию об отправителе/получателе в формате отправитель -> получатель
    """
    from_info = bank_info.get('from', 'Неизвестный отправитель')
    to_info = bank_info.get('to', 'Неизвестный получатель')

    if from_info != 'Неизвестный отправитель':
        from_info = parse_bank_info(from_info)
    if to_info != 'Неизвестный получатель':
        to_info = parse_bank_info(to_info)

    return f'{from_info} -> {to_info}'


def parse_bank_info(bank_info: str) -> str:
    """
    Возвращает засекреченную платежную информацию отправителя/пользователя
    :param bank_info: информация об операции
    :return: засекреченную платёжную информацию
    """
    *bank_name, bank_address = bank_info.split()
    bank_address = list(bank_address)

    if bank_name[0] == 'Счет':
        # маскируем платёжную информацию счёта согласно формату **XXXX
        bank_address = ['**'] + bank_address[-4:]

    # маскируем платёжную информацию банковской карты согласно формату XXXX XX** **** XXXX
    else:
        # заменяем числа в диапазоне от 6 до 12 на *
        bank_address[STARTING_INDEX_ENCRYPTED_SYMBOLS:ENDING_INDEX_ENCRYPTED_SYMBOLS] = ['*'] * 6

        # добавляем пробел в номер карты с шагом в 4 символа
        for index in range(-len(bank_address) + 4, 0, 4):
            bank_address.insert(index, ' ')

    return " ".join((*bank_name, ''.join(bank_address)))


def parse_amount(amount_data: dict) -> str:
    """
    Возвращает изменённый вид информации об отправленной сумме
    :param amount_data: данные об операции
    :return: изменённый вид информации об отправленной сумме
    """
    amount_info = amount_data['operationAmount']
    money_amount = amount_info['amount']
    money_course = amount_info['currency']['name']

    return f"{money_amount} {money_course}"


def show_info(info: dict) -> str:
    """Возвращает информацию об банковской операции"""
    parsed_date = parse_date(info['date'])
    parsed_address = parse_address(info)
    parsed_amount = parse_amount(info)

    return (
        f"{parsed_date} {info['description']}\n"
        f"{parsed_address}\n"
        f"{parsed_amount}\n"
    )
