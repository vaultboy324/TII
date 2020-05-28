# -*- coding: utf8 -*-

from lab4.constants import file_names
from lab4.constants import regression_enum
from lab4.constants import fields
from lab4.modules.file_parser import FileParser
from lab4.modules.regression import Regression

if __name__ == '__main__':
    dataset = FileParser.get_content(file_names.FIXED_ADDRESS_PART, file_names.FULL_DATA)
    linear_regression_results = Regression.get_result(dataset, regression_enum.LINEAR_REGRESSION)
    print(f'Точность линейной модели: {linear_regression_results[fields.accuracy] * 100}%\n',
          f'w = {linear_regression_results[fields.w]}\n')

    polynominal_regression_results = Regression.get_result(dataset, regression_enum.POLYNOMINAL_REGRESSION)
    print(f'Точность полиномиальной модели: {polynominal_regression_results[fields.accuracy] * 100}%\n',
          f'w = {polynominal_regression_results[fields.w]}\n')

    logistic_regression_results = Regression.get_result(dataset, regression_enum.LOGISTIC_REGRESSION)
    print(f'Точность логистической модели: {logistic_regression_results[fields.accuracy] * 100}%\n',
          f'w = {logistic_regression_results[fields.w]}\n')