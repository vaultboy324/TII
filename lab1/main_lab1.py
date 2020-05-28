from lab1.config.config import *
from lab1.modules.bayes_classifier import BayesClassifier
from lab1.modules.mongo.documents.poets.poet_document import PoetDocument

if __name__ == "__main__":
    BayesClassifier.learn()
    BayesClassifier.research()
