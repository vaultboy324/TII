import os
import re
from lab1.constants import fields


class FileParser:
    _path = ''
    _trash = {
        fields.EMPTY_SYMBOLS: {''},
        fields.PREPOSITIONS: {'в', 'без', 'до', 'из', 'к', 'на', 'по',
                              'о', 'от', 'перед', 'при', 'через', 'с',
                              'у', 'за', 'над', 'об', 'под', 'про', 'для'},
        fields.PRONOUNS: {'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они', 'себя', 'мой', 'твой', 'свой', 'ваш', 'наш',
                          'его', 'её', 'их',
                          'кто', 'что', 'какой', 'который', 'чей', 'сколько', 'каковой', 'каков', 'зачем', 'когда',
                          'тот', 'этот', 'столько', 'такой', 'таков',
                          'всякий', 'каждый', 'сам', 'самый', 'любой', 'иной', 'другой', 'весь'},
        fields.NUMBERS: {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
        fields.INTERJECTIONS: {'а', 'но'},
        fields.SPECIAL_SYMBOLS: (chr(134), chr(72), chr(73), chr(77), chr(54), chr(41), chr(42), chr(55), chr(56), chr(205), chr(253), chr(273))
    }

    @staticmethod
    def __have_numbers(word: str):
        for symbol in word:
            if symbol in FileParser._trash[fields.NUMBERS]:
                return True

        return False

    @staticmethod
    def __remove_special_symbols(word: str):
        result = ''
        for letter in word:
            if letter.isalpha():
                result += letter
        return result
        # temp = word
        # r = re.compile("[а-яА-Я]")
        # for special_symbol in FileParser._trash[fields.SPECIAL_SYMBOLS]:
        #     temp = temp.replace(special_symbol, '')
        # return temp

    @staticmethod
    def _init(fixed_part, directory, filename):
        FileParser._path = os.getcwd() + chr(92) + fixed_part
        if len(directory) != 0:
            FileParser._path += chr(92) + directory
        FileParser._path += chr(92) + filename

    @staticmethod
    def _remove_trash(content):
        result = {}
        for word in content:
            word = word.lower()
            if word in FileParser._trash[fields.EMPTY_SYMBOLS]:
                continue
            if word in FileParser._trash[fields.PREPOSITIONS]:
                continue
            if word in FileParser._trash[fields.PRONOUNS]:
                continue
            if word in FileParser._trash[fields.INTERJECTIONS]:
                continue
            if FileParser.__have_numbers(word):
                continue
            word = FileParser.__remove_special_symbols(word)
            if word in FileParser._trash[fields.EMPTY_SYMBOLS]:
                continue
            if len(word) <= 3:
                continue
            # word.translate()
            if result.get(word):
                result[word] += 1
            else:
                result[word] = 1
        return result

    @staticmethod
    def get_content(fixed_part, directory, filename):
        FileParser._init(fixed_part, directory, filename)
        content = open(FileParser._path, 'r').read()
        if len(directory) != 0:
            rows = content.split('\n')
            for row in rows:
                if len(row) > 40:
                    content = content.replace(row, '')

        content = content.replace('\n', ' ').replace('\t', ' ').split(' ')
        return FileParser._remove_trash(content)
