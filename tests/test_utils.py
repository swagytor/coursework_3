import pytest

from src.utils import *


@pytest.fixture
def data():
    return [
        {
            "id": 179194306,
            "state": "EXECUTED",
            "date": "2019-05-19T12:51:49.023880",
            "operationAmount": {
                "amount": "6381.58",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "МИР 5211277418228469",
            "to": "Счет 58518872592028002662"
        },
        {
            "id": 27192367,
            "state": "CANCELED",
            "date": "2018-12-24T20:16:18.819037",
            "operationAmount": {
                "amount": "991.49",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 71687416928274675290",
            "to": "Счет 87448526688763159781"
        },
        {
            "id": 921286598,
            "state": "EXECUTED",
            "date": "2018-03-09T23:57:37.537412",
            "operationAmount": {
                "amount": "25780.71",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 26406253703545413262",
            "to": "Счет 20735820461482021315"
        },
        {
            "id": 207126257,
            "state": "EXECUTED",
            "date": "2019-07-15T11:47:40.496961",
            "operationAmount": {
                "amount": "92688.46",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 35737585785074382265"
        },
        {
            "id": 957763565,
            "state": "EXECUTED",
            "date": "2019-01-05T00:52:30.108534",
            "operationAmount": {
                "amount": "87941.37",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 46363668439560358409",
            "to": "Счет 18889008294666828266"
        },
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {
                "amount": "97853.86",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 1308795367077170",
            "to": "Счет 96527012349577388612"
        }
    ]


@pytest.fixture
def wrong_data():
    return [
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "999-07-13T18:51:29.313309",
            "operationAmount": {
                "amount": "97853.86",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на счет"
        }
    ]


def test_get_data_from_json():
    assert isinstance(get_data_from_json(), list)


def test_get_data_from_json__file_not_found_error():
    with pytest.raises(FileNotFoundError):
        get_data_from_json('NotExistingFile.json')


def test_sort_data(data):
    assert sort_data(data)[0]['date'] > sort_data(data)[-1]['date']


def test_parse_date():
    assert isinstance(parse_date('2023-04-30T00:00:00'), str)
    assert parse_date('2023-04-30T00:00:00') == '30.04.2023'
    assert parse_date('2023.12.13T00:00:00') == 'Некорректный формат даты'
    assert parse_date('1-04-30T00:00:00') == 'Некорректный формат даты'
    assert parse_date('2023-04-31T00:00:00') == 'Некорректный формат даты'


def test_parse_address(data, wrong_data):
    assert isinstance(parse_address(data[0]), str)
    assert parse_address(data[0]) == 'МИР 5211 27** **** 8469 -> Счет **2662'
    assert parse_address(wrong_data[0]) == 'Неизвестный отправитель -> Неизвестный получатель'


def test_parse_amount(data):
    assert isinstance(parse_amount(data[0]), str)
    assert parse_amount(data[0]) == '6381.58 USD'
    assert parse_amount(data[4]) == '87941.37 руб.'


def test_show_info(data):
    assert show_info(data[0]) == ('19.05.2019 Перевод организации\n'
                                  'МИР 5211 27** **** 8469 -> Счет **2662\n'
                                  '6381.58 USD\n')

