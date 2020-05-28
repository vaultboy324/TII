from lab3.constants import fields
from lab3.constants import functions_enum
from lab3.modules.knn import KNN


class ParzensWindow:
    _k = 0
    _report = {}

    @staticmethod
    def _init(dataset, field_list, weights, function):
        k = 1
        current_accuracy = 0
        report = KNN.get_result(dataset, field_list, weights, k, functions_enum.NOT)

        while current_accuracy <= report[fields.ACCURACY]:
            current_accuracy = report[fields.ACCURACY]
            k += 1
            report = KNN.get_result(dataset, field_list, weights, k, functions_enum.NOT)

        ParzensWindow._k = k

        ParzensWindow._report = KNN.get_result(dataset, field_list, weights, ParzensWindow._k, function)

    @staticmethod
    def get_result(dataset, field_list, weights, function):
        ParzensWindow._init(dataset, field_list, weights, function)
        return ParzensWindow._report
