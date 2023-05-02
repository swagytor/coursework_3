import os.path
import utils

PATH_TO_DATA = os.path.abspath('data')
PATH_TO_JSON_DATA = os.path.join(PATH_TO_DATA, 'operations.json')


def main():
    operations_data = utils.get_data_from_json(PATH_TO_JSON_DATA)
    sorted_data = utils.sort_data(operations_data)
    for data in sorted_data:
        print(data)


if __name__ == '__main__':
    main()
