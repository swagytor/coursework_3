from src.utils import get_data_from_json, sort_data, show_info


def main() -> None:
    """Основное тело программы"""

    # получаем список данных об банковских операциях
    operations_data = get_data_from_json()

    # получаем список N выполненных операций и сортируем по недавним операциям
    sorted_data = sort_data(operations_data)

    for data in sorted_data:
        print(show_info(data))


if __name__ == '__main__':
    main()
