import os.path
import utils

PATH_TO_DATA = os.path.abspath('data')
PATH_TO_JSON_DATA = os.path.join(PATH_TO_DATA, 'operations.json')

operations_data = utils.get_data_from_json(PATH_TO_JSON_DATA)


def main():
    pass


if __name__ == '__main__':
    main()
