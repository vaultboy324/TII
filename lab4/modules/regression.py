import random

import numpy
from sklearn.model_selection import train_test_split

from lab4.constants import fields
from lab4.constants import regression_enum


class Regression:
    _learn = {
        fields.X: [],
        fields.Y: []
    }
    _test = {
        fields.X: [],
        fields.Y: []
    }
    _type = 0
    _seed = 5
    _w = []

    @staticmethod
    def _clear():
        Regression._learn = {
            fields.X: [],
            fields.Y: []
        }
        Regression._test = {
            fields.X: [],
            fields.Y: []
        }
        Regression._w = []
        Regression._type = 0

    @staticmethod
    def _init(dataset):
        Regression._clear()

        temp_dataset = dataset.copy()

        Regression._learn[fields.X], Regression._test[fields.X], \
        Regression._learn[fields.Y], Regression._test[fields.Y] = train_test_split(temp_dataset[fields.X],
                                                                                   temp_dataset[fields.Y],
                                                                                   test_size=0.1,
                                                                                   random_state=Regression._seed)

    @staticmethod
    def _activation_function(value):
        if value >= 0.5:
            return 1
        else:
            return 0

    @staticmethod
    def _get_accuracy():
        test_len = len(Regression._test[fields.Y])
        successful = 0
        for i in range(0, test_len):
            prediction = numpy.dot(Regression._test[fields.X][i], Regression._w)
            if Regression._activation_function(prediction) == Regression._test[fields.Y][i]:
                successful += 1
        return successful / test_len

    @staticmethod
    def _linear_regression():
        a_transpose = numpy.transpose(Regression._learn[fields.X])
        back_matrix = numpy.linalg.inv(numpy.dot(a_transpose, Regression._learn[fields.X]))
        left_part = numpy.dot(back_matrix, a_transpose)
        return numpy.dot(left_part, Regression._learn[fields.Y])

    @staticmethod
    def _polynominal_regression():
        powers = [i ** 0.01 for i in range(len(Regression._learn[fields.X][0]))]
        a = []
        for current_x in Regression._learn[fields.X]:
            row = []
            for index in range(0, len(current_x)):
                row.append(current_x[index] ** powers[index])
            a.append(row)

        a_transpose = numpy.transpose(a)
        back_matrix = numpy.linalg.inv(numpy.dot(a_transpose, a))
        left_part = numpy.dot(back_matrix, a_transpose)
        return numpy.dot(left_part, Regression._learn[fields.Y])

    @staticmethod
    def _distance(a, b):
        result = 0

        for i in range(0, len(a)):
            result += (a[i] - b[i]) ** 2

        return numpy.sqrt(result)

    @staticmethod
    def _logistic_regression():
        b = [0 for i in range(0, len(Regression._learn[fields.X][0]))]
        b[0] = numpy.log10(numpy.mean(Regression._learn[fields.Y]) / (1 - numpy.mean(Regression._learn[fields.Y])))
        b = numpy.transpose(b)

        while True:
            z = numpy.dot(Regression._learn[fields.X], b)
            p = 1 / (1 + numpy.exp(-z))
            w = p * (1 - p)
            u = z + (Regression._learn[fields.Y] - p) / w

            b_old = b

            a_transpose = numpy.transpose(Regression._learn[fields.X])
            weights = numpy.diag(w)
            left_part = numpy.dot(a_transpose, weights)
            left_part = numpy.linalg.inv(numpy.dot(left_part, Regression._learn[fields.X]))
            left_part = numpy.dot(left_part, a_transpose)
            left_part = numpy.dot(left_part, weights)
            b = numpy.dot(left_part, u)

            if Regression._distance(b, b_old) < 0.01:
                break
        return b

    @staticmethod
    def get_result(dataset, regression_type):
        Regression._init(dataset)

        if regression_type == regression_enum.LINEAR_REGRESSION:
            w_linear = Regression._linear_regression()
            Regression._w = w_linear
            accuracy = Regression._get_accuracy()
        if regression_type == regression_enum.POLYNOMINAL_REGRESSION:
            w_polynominal = Regression._polynominal_regression()
            Regression._w = w_polynominal
            accuracy = Regression._get_accuracy()
        if regression_type == regression_enum.LOGISTIC_REGRESSION:
            w_logistic = Regression._logistic_regression()
            Regression._w = w_logistic
            accuracy = Regression._get_accuracy()

        return {
            fields.accuracy: accuracy,
            fields.w: Regression._w
        }
