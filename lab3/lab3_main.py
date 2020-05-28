import matplotlib.pyplot as plt

from lab3.constants import file_names
from lab3.constants import fields
from lab3.constants import values
from lab3.constants import functions_enum

from lab3.modules.file_parser import FileParser
from lab3.modules.parzens_window import ParzensWindow


def multi_plot(figure, title, pos, report):
    # pos = []
    #
    # for index in range(0, len(report)):
    #     pos.append([index, int(report.at[index, fields.NAME])])

    ax = figure.add_subplot(2, 2, pos, projection='3d')
    ax.set_xlabel(fields.TOTAL_PHENOLS)
    ax.set_ylabel(fields.FLAVANOIDS)
    ax.set_zlabel(fields.NONFLAVANOID_PHENOLS)
    ax.set_title(title)

    for index in range(0, len(report)):
        x = report.at[index, fields.TOTAL_PHENOLS]
        y = report.at[index, fields.FLAVANOIDS]
        z = report.at[index, fields.NONFLAVANOID_PHENOLS]

        wine_class = int(report.at[index, fields.RECOGNIZE])
        if wine_class == 1:
            color = 'r'
        elif wine_class == 2:
            color = 'b'
        else:
            color = 'g'
        ax.scatter(x, y, z, c=color, marker='o')


if __name__ == '__main__':
    fig = plt.figure(figsize=plt.figaspect(0.5))

    dataset = FileParser.get_content(file_names.FIXED_ADDRESS_PART, file_names.FULL_DATA)
    result = ParzensWindow.get_result(dataset, fields.ORDER_FIELD_LIST, True, functions_enum.EPANECHNIKOV)
    print(result)
    multi_plot(fig, 'Ядро Епаненичникова', 1, result[fields.RESULT_TABLE])

    result = ParzensWindow.get_result(dataset, fields.ORDER_FIELD_LIST, True, functions_enum.QUART)
    print(result)
    multi_plot(fig, 'Квартическое ядро', 2, result[fields.RESULT_TABLE])

    result = ParzensWindow.get_result(dataset, fields.ORDER_FIELD_LIST, True, functions_enum.TRIWEIGHT)
    print(result)
    multi_plot(fig, 'Триквадратное ядро', 3, result[fields.RESULT_TABLE])

    result = ParzensWindow.get_result(dataset, fields.ORDER_FIELD_LIST, True, functions_enum.GAUSS)
    print(result)
    multi_plot(fig, 'Ядро Гаусса', 4, result[fields.RESULT_TABLE])
    # report = KNN.get_result(dataset, fields.ORDER_FIELD_LIST, values.BASE_WEIGHTS, 3)

    # print(report)
    plt.show()
