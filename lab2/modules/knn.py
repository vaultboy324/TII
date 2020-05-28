import sys
import random
import numpy
import pandas

from lab2.constants import fields

from lab2.modules.file_parser import FileParser


class KNN:
    _fields = ()
    _old_data = []
    _k = 0
    _seed = 2
    _new_data = []
    _report = {}
    _is_weighted = False

    @staticmethod
    def _clear():
        KNN._fields = ()
        KNN._old_data = []
        KNN._k = 0
        KNN._new_data = []
        KNN._report = {}
        KNN._is_weighted = False

    @staticmethod
    def _init(dataset, fields, is_weighted, k):
        KNN._clear()

        KNN._split_dataset(dataset)

        KNN._fields = fields
        KNN._is_weighted = is_weighted
        # KNN._old_data = KNN._get_dataset()
        KNN._k = k

    @staticmethod
    def _find_equals():
        result = []
        for learn_row in KNN._old_data:
            for test_row in KNN._new_data:
                if learn_row == test_row and learn_row not in result:
                    result.append(learn_row)

        return result

    @staticmethod
    def _split_dataset(dataset: list):
        random.seed(KNN._seed)

        temp_dataset = dataset.copy()
        dataset_len = len(temp_dataset)

        random.shuffle(temp_dataset)

        KNN._old_data = temp_dataset[: int(0.8 * dataset_len)]
        KNN._new_data = temp_dataset[int(0.8 * dataset_len):]

    @staticmethod
    def _get_distance(old_element: dict, new_element: dict):
        result = 0
        for field in KNN._fields:
            if field == fields.NAME:
                continue
            result += (old_element[field] - new_element[field]) ** 2

        result = numpy.sqrt(result)

        return result

    @staticmethod
    def _get_k_closest(distances: list):
        result = []

        temp_distances = distances.copy()
        # temp_distances = sorted(temp_distances)

        for i in range(0, KNN._k):
            min_distance_index = temp_distances.index(min(temp_distances))

            row = KNN._old_data[min_distance_index].copy()
            row[fields.DISTANCE] = temp_distances[min_distance_index]
            result.append(row)

            temp_distances[min_distance_index] = float('inf')

        return result

    @staticmethod
    def _get_class(closest: list):
        if KNN._is_weighted:
            classes_by_distance = {}
            for element in closest:
                current_value = 1 / ((element[fields.DISTANCE] + 1) ** 2)
                if classes_by_distance.get(element[fields.NAME]):
                    classes_by_distance[element[fields.NAME]] += current_value
                else:
                    classes_by_distance[element[fields.NAME]] = current_value

            result = ''
            max_value = 0
            for current_class in classes_by_distance:
                if classes_by_distance[current_class] > max_value:
                    max_value = classes_by_distance[current_class]
                    result = current_class

            return result
        classes = [neighbor[fields.NAME] for neighbor in closest]
        return max(set(classes), key=classes.count)

    @staticmethod
    def _get_accuracy(recognize_list):
        all_recognize_count = len(recognize_list)
        right_recognize_count = 0

        for index in range(0, all_recognize_count):
            if recognize_list[index] == KNN._new_data[index][fields.NAME]:
                right_recognize_count += 1

        return right_recognize_count / all_recognize_count

    @staticmethod
    def _create_report(accuracy):
        KNN._report = {
            fields.RESULT_TABLE: pandas.DataFrame(KNN._new_data),
            fields.ACCURACY: accuracy * 100
        }

    @staticmethod
    def get_result(dataset: list, field_list, is_weighted, k):
        result = []
        recognize_list = []

        KNN._init(dataset, field_list, is_weighted, k)

        for research_row in KNN._new_data:
            distances_for_row = []

            for data_row in KNN._old_data:
                distances_for_row.append(KNN._get_distance(data_row, research_row))

            closest = KNN._get_k_closest(distances_for_row)
            current_recognize = KNN._get_class(closest)
            recognize_list.append(current_recognize)
            research_row[fields.RECOGNIZE] = current_recognize

        accuracy = KNN._get_accuracy(recognize_list)
        KNN._create_report(accuracy)

        result = KNN._report

        return result
