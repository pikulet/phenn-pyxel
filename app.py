import random
import requests
from typing import Optional


class Pomenohenn:
    def __init__(self, dictionary: str, min_word_length: int, max_word_length: int):
        self._all_words: set[int] = self.parse_dictionary(dictionary)
        self._min_word_length: int = min_word_length
        self._max_word_length: int = max_word_length
        self._question: str = None
        self._answer: str = None

    @property
    def question(self) -> str:
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def answer(self):
        return self._answer

    def generate_question(self) -> None:
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
