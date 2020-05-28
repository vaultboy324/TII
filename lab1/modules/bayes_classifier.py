import numpy

from lab1.constants import fields
from lab1.config import config
from lab1.modules.file_parser import FileParser
from lab1.modules.mongo.documents.poets.poet_document import PoetDocument


class BayesClassifier:
    _numerators = []
    _denominator = 0
    _report = []

    @staticmethod
    def _remove_rare_words(poet):
        new_poet = {
            fields.NAME: poet[fields.NAME],
            fields.WORDS: {}
        }
        for word in poet[fields.WORDS]:
            if poet[fields.WORDS][word] > 10:
                new_poet[fields.WORDS][word] = poet[fields.WORDS][word]
        return new_poet

    @staticmethod
    def _get_conditional_probability_for_other_classes(poets, poet_number, words):
        result = 0

        for poet_index in range(0, len(poets)):
            if poet_index == poet_number:
                continue
            result += BayesClassifier._get_conditional_probability(words, None, poets[poet_index])

        return result

    @staticmethod
    def _word_in_all_classes(poets, word):
        for poet in poets:
            if not poet[fields.WORDS].get(word):
                return False
        return True

    @staticmethod
    def _remove_repeated_words(poets, all_words):
        for word in all_words:
            if BayesClassifier._word_in_all_classes(poets, word):
                for poet in poets:
                    poet[fields.WORDS].pop(word)

    @staticmethod
    def _add_count_words_for_poets(poets):
        for poet in poets:
            sum_words = BayesClassifier._get_count_words(poet[fields.WORDS])
            # for word in poet[fields.WORDS][word]:
            #     sum_words += poet[fields.WORDS][word]
            poet[fields.COUNT_WORDS] = sum_words

    @staticmethod
    def _get_count_words(words):
        result = 0
        for word in words:
            result += words[word]
        return result

    @staticmethod
    def _remove_weak_probabilities(poets, all_words):
        new_poets = []
        for poet in poets:
            new_poet = {
                fields.NAME: poet[fields.NAME],
                fields.WORDS: {},
                fields.COUNT_WORDS: 0
            }
            for word in poet[fields.WORDS]:
                if poet[fields.WORDS][word] >= 0.5:
                    new_poet[fields.WORDS][word] = poet[fields.WORDS][word]
                    new_poet[fields.COUNT_WORDS] += all_words[word] * poet[fields.WORDS][word]
            new_poets.append(new_poet)
        return new_poets

    @staticmethod
    def _recalc_count_words(old_words, new_words):
        for word in new_words:
            if old_words.get(word):
                old_words[word] += new_words[word]
            else:
                old_words[word] = new_words[word]

    @staticmethod
    def _calc_probabilities(all_words, poets):
        for word in all_words:
            for poet in poets:
                if poet[fields.WORDS].get(word):
                    poet[fields.WORDS][word] /= all_words[word]

    @staticmethod
    def _refresh_values():
        BayesClassifier._numerators = []
        BayesClassifier._denominator = 0

    @staticmethod
    def _get_conditional_probability(words, all_words_count, poet):
        result = 1
        for word in words:
            if poet[fields.WORDS].get(word):
                count = poet[fields.WORDS][word]
            else:
                count = 0
            probability = count / all_words_count
            if probability == 0:
                result *= 10e-10
            else:
                result *= 10e10 * probability
        return result

    @staticmethod
    def _remove_excess_words(words: dict, data: dict):
        result = {}
        for word in words:
            if data.get(word):
                result[word] = data[word]
        return result

    @staticmethod
    def _save_to_db(node):
        PoetDocument.remove()
        PoetDocument.post_one(node)

    @staticmethod
    def _read_from_db():
        return PoetDocument.get_info()

    @staticmethod
    def _remove_spam_words(all_words: dict, poets: list):
        for_remove = []
        for word in all_words:
            if all_words[word] > 45:
                for_remove.append(word)

        for word in for_remove:
            all_words.pop(word)
            for poet in poets:
                if poet[fields.WORDS].get(word):
                    poet[fields.WORDS].pop(word)

    @staticmethod
    def _create_classes(poets: list):
        current_poet = {
            fields.NAME: config.author,
            fields.WORDS: {},
            fields.COUNT_WORDS: 0
        }

        other_poets = {
            fields.NAME: config.others,
            fields.WORDS: {},
            fields.COUNT_WORDS: 0
        }

        for poet in poets:
            if poet[fields.NAME] == current_poet[fields.NAME]:
                current_poet[fields.WORDS] = poet[fields.WORDS]
                current_poet[fields.COUNT_WORDS] = poet[fields.COUNT_WORDS]
            else:
                for word in poet[fields.WORDS]:
                    if other_poets[fields.WORDS].get(word):
                        other_poets[fields.WORDS][word] += poet[fields.WORDS][word]
                    else:
                        other_poets[fields.WORDS][word] = poet[fields.WORDS][word]
                other_poets[fields.COUNT_WORDS] += poet[fields.COUNT_WORDS]

        return [current_poet, other_poets]

    @staticmethod
    def learn():
        poets = []
        all_words = {}

        for directory in config.directories:
            poet_info = {
                fields.NAME: directory[fields.NAME],
                fields.WORDS: {},
                fields.COUNT_WORDS: 0
            }

            for file in directory[fields.FILES]:
                current_words = FileParser.get_content(config.fixed_address_part_learn, directory[fields.NAME], file)
                BayesClassifier._recalc_count_words(poet_info[fields.WORDS], current_words)

            poet_info[fields.COUNT_WORDS] = BayesClassifier._get_count_words(poet_info[fields.WORDS])
            BayesClassifier._recalc_count_words(all_words, poet_info[fields.WORDS])
            poets.append(poet_info)

        classes = BayesClassifier._create_classes(poets)

        result = {
            fields.POETS: poets,
            fields.WORDS: all_words,
            fields.COUNT_WORDS: classes[0][fields.COUNT_WORDS] + classes[1][fields.COUNT_WORDS]
        }
        BayesClassifier._save_to_db(result)

    @staticmethod
    def research():
        data = BayesClassifier._read_from_db()
        full_count_words = data[fields.COUNT_WORDS]
        for file_number in range(0, len(config.test_files)):
            current_words = FileParser.get_content(config.fixed_address_part_test, '', config.test_files[file_number])
            current_words = BayesClassifier._remove_excess_words(current_words, data[fields.WORDS])
            BayesClassifier._refresh_values()

            for poet in data[fields.POETS]:
                priory_probability = poet[fields.COUNT_WORDS] / data[fields.COUNT_WORDS]
                numerator = priory_probability * BayesClassifier._get_conditional_probability(current_words, data[fields.COUNT_WORDS], poet)
                BayesClassifier._numerators.append(numerator)
                BayesClassifier._denominator += numerator

            print(BayesClassifier._numerators.index(max(BayesClassifier._numerators)))
            # print(BayesClassifier._numerators)


        # data = BayesClassifier._read_from_db()
        # print(data)

