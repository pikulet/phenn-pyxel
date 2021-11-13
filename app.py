import random
import requests

class Pomenohenn:

    def __init__(self, dictionary, min_word_length, max_word_length):
        self._all_words = self.parse_dictionary(dictionary)
        self._min_word_length = min_word_length
        self._max_word_length = max_word_length
        self._question = None
        self._answer = None

    def is_started(self):
        return self._question is not None

    def reset(self):
        self._question = None
        self._answer = None

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def answer(self):
        return self._answer

    def generate_question(self):
        word_len = 0
        while word_len < self._min_word_length or word_len > self._max_word_length:
            self._answer = random.choice(self._all_words)
            word_len = len(self._answer)

        # found word
        to_move = list(self._answer[1:-1])
        random.shuffle(to_move)

        self._question = self._answer[0] + "".join(to_move) + self._answer[-1]

    def parse_dictionary(self, dictionary):
        resp = requests.get(dictionary)
        return resp.content.decode().splitlines()
