import sys
import random
import numpy
import pandas

from lab3.constants import fields
from lab3.constants import functions_enum

from lab3.modules.file_parser import FileParser


class KNN:
    _fields = ()
    _old_data = []
    _k = 0
    _seed = 5
    _new_data = []
    _report = {}
    _is_weighted = False
    _function = functions_enum.NOT

    @staticmethod
    def _clear():
        KNN._fields = ()
        # KNN._old_data = []
        KNN._k = 0
        # KNN._new_data = []
        KNN._report = {}
        KNN._is_weighted = False
        KNN._function = functions_enum.NOT

    @staticmethod
    def _init(dataset, fields, is_weighted, k, function):
        KNN._clear()

        KNN._split_dataset(dataset)

        KNN._fields = fields
        KNN._is_weighted = is_weighted
        KNN._function = function
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

        if not KNN._old_data:
            KNN._old_data = temp_dataset[: int(0.8 * dataset_len)]
        if not KNN._new_data:
            KNN._new_data = temp_dataset[int(0.8 * dataset_len):]

        #
        # learn_block_len = int(0.8 * dataset_len)
        # research_block_len = int(0.2 * dataset_len)
        #
        # research_data = []
        # learn_data = []
        #
        # for i in range(0, learn_block_len):
        #     element_index = random.randint(0, dataset_len - 1)
        #     research_data.append(temp_dataset[element_index].copy())
        #
        #     temp_dataset.remove(temp_dataset[element_index])
        #     dataset_len -= 1
        #
        # for i in range(0, research_block_len):
        #     element_index = random.randint(0, dataset_len - 1)
        #     learn_data.append(temp_dataset[element_index].copy())
        #
        #     temp_dataset.remove(temp_dataset[element_index])
        #     dataset_len -= 1
        #
        # KNN._old_data = research_data
        # KNN._new_data = learn_data

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
    def _simple_function(distance):
        return 1 / ((distance + 1) ** 2)

    @staticmethod
    def _epanechnikov(r):
        if abs(r) <= 1:
            return 3 / 4 * (1 - r ** 2)
        else:
            return 0

    @staticmethod
    def _quart(r):
        if abs(r) <= 1:
            return 15 / 16 * (1 - r ** 2) ** 2
        else:
            return 0

    @staticmethod
    def _triweight(r):
        if abs(r) <= 1:
            return 35 / 32 * (1 - r ** 2) ** 3
        else:
            return 0

    @staticmethod
    def _gauss(r):
        if abs(r) <= 1:
            return ((2 * numpy.pi) ** (- 0.5)) * numpy.exp(- 0.5 * r ** 2)
        else:
            return 0

    @staticmethod
    def _get_class(closest: list):
        if KNN._is_weighted:
            classes_by_distance = {}
            h = closest[-1][fields.DISTANCE]
            for element in closest:
                r = element[fields.DISTANCE] / h
                if KNN._function == functions_enum.EPANECHNIKOV:
                    current_value = KNN._epanechnikov(r)
                elif KNN._function == functions_enum.QUART:
                    current_value = KNN._quart(r)
                elif KNN._function == functions_enum.TRIWEIGHT:
                    current_value = KNN._triweight(r)
                elif KNN._function == functions_enum.GAUSS:
                    current_value = KNN._gauss(r)
                else:
                    current_value = KNN._simple_function(element[fields.DISTANCE])
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
    def get_result(dataset: list, field_list, is_weighted, k, function):
        recognize_list = []

        KNN._init(dataset, field_list, is_weighted, k, function)

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
