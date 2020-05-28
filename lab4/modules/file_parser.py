import os


from lab4.constants import words
from lab4.constants import fields


class FileParser:
    _path = ''
    _data_table = []

    @staticmethod
    def _init(fixed_part, file_name):
        FileParser._path = (os.getcwd() + chr(92)
                            + fixed_part + chr(92)
                            + file_name)

    @staticmethod
    def _create_data_table(data_from_file: list):
        data_from_file.remove(data_from_file[0])

        result = {
            fields.X: [],
            fields.Y: []
        }

        for row in data_from_file:
            parsed_row = row.split('\t')
            row_len = len(parsed_row)
            parsed_row[row_len - 1] = parsed_row[row_len - 1].replace('\n', '')

            x_row = [1]

            for index in range(0, row_len):
                if index == row_len - 1:
                    if parsed_row[index] == words.NOT:
                        result[fields.Y].append(0)
                    else:
                        result[fields.Y].append(1)
                else:
                    if parsed_row[index] == words.FEMALE or parsed_row[index] == words.NOT:
                        x_row.append(0)
                    elif parsed_row[index] == words.MALE or parsed_row[index] == words.YES:
                        x_row.append(1)
                    else:
                        x_row.append(float(parsed_row[index]))

            result[fields.X].append(x_row)

        FileParser._data_table = result

    @staticmethod
    def get_content(fixed_part, file_name):
        FileParser._init(fixed_part, file_name)
        content = open(FileParser._path, 'r').readlines()
        FileParser._create_data_table(content)
        return FileParser._data_table
