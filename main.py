from typing import Iterator
from app import Pomenohenn
import rsc
import pyxel
from enum import Enum


class PomenohennApp:
    class State(Enum):
        Intro = 0
        Game = 1
        Ending = 2

    def __init__(
        self,
        dictionary,
        width=180,
        height=100,
        min_word_length=6,
        max_word_length=10,
        max_lives=3,
        max_questions=10,
    ):

        self.phenn = Pomenohenn(dictionary, min_word_length, max_word_length)

        # try counter
        self.max_lives: int = max_lives
        self.lives_remaining: int = max_lives
        # ui selector
        self.current_guess: list[str] = None
        self.is_selected: bool = False
        self.current_select: int = 1
        self.max_select: int = 0
        # scoring
        self.max_questions: int = max_questions
        self.total_questions: int = 0
        self.correct_questions: int = 0 # currently not used

        self.width: int = width
        self.height: int = height

        self.state: PomenohennApp.State = PomenohennApp.State.Intro

        pyxel.init(self.width, self.height, caption="Pomenohenn")
        pyxel.load("assets/rsc.pyxres")
        pyxel.run(self.update, self.draw)

    def new_question(self) -> None:
        if self.total_questions == self.max_questions:
            self.state = PomenohennApp.State.Ending
            return

        self.phenn.generate_question()
        # reset state
        self.current_guess = list(self.phenn.question)
        self.is_selected = False
        self.current_select = 1
        self.max_select = len(self.current_guess) - 2
        self.total_questions += 1

    def update(self) -> None:
        if self.state == PomenohennApp.State.Intro:
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.state = PomenohennApp.State.Game
                self.lives_remaining = self.max_lives
                self.total_questions = 0
                self.new_question()
            return
        elif self.state == PomenohennApp.State.Ending:
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.state = PomenohennApp.State.Intro
            return

        if pyxel.btnp(pyxel.KEY_ENTER):
            # make guess
            if "".join(self.current_guess) == self.phenn.answer:
                self.correct_questions += 1
                self.new_question()
                return
            # wrong answer
            self.lives_remaining -= 1
            if self.lives_remaining == 0:
                self.state = PomenohennApp.State.Ending
                return

        if pyxel.btnp(pyxel.KEY_Z):
            # skip question
            self.lives_remaining -= 1
            if self.lives_remaining == 0:
                self.state = PomenohennApp.State.Ending
                return
            self.new_question()
            return

        if pyxel.btnp(pyxel.KEY_SPACE):
            # activate selector
            self.is_selected = not self.is_selected
            return

        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.current_select == 1:
                return
            if self.is_selected:
                (
                    self.current_guess[self.current_select],
                    self.current_guess[self.current_select - 1],
                ) = (
                    self.current_guess[self.current_select - 1],
                    self.current_guess[self.current_select],
                )
            self.current_select -= 1
            return

        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.current_select == self.max_select:
                return
            if self.is_selected:
                (
                    self.current_guess[self.current_select],
                    self.current_guess[self.current_select + 1],
                ) = (
                    self.current_guess[self.current_select + 1],
                    self.current_guess[self.current_select],
                )
            self.current_select += 1
            return

    def draw(self) -> None:
        pyxel.cls(0)
        if self.state == PomenohennApp.State.Intro:
            self.draw_title("pomenohenn")
            self.draw_blt(
                rsc.btn_enter,
                self.get_moving_position(0.5 * self.width, drift=1),
                0.7 * self.height,
            )
            self.draw_blt(rsc.logo_gh, self.width - 30, self.height - 15)
            return
        elif self.state == PomenohennApp.State.Ending:
            if self.lives_remaining == 0:
                self.draw_title("failed")
            else:
                self.draw_title("success")
            return

        # qn number
        self.draw_blt(rsc.qns[self.total_questions], 15, 15)
        # lives
        self.draw_lives(0.9 * self.width, 15)

        # current guess
        self.draw_word(self.current_guess, 0.5 * self.width, 0.5 * self.height)
        # selector
        self.draw_blt(
            rsc.selector, self.get_selector_x(0.5 * self.width), 0.65 * self.height
        )

        # key hints
        self.draw_blt(rsc.btn_move, 0.5 * self.width - 58, 0.85 * self.height)
        self.draw_blt(rsc.btn_select, 0.5 * self.width - 11, 0.85 * self.height)
        self.draw_blt(rsc.btn_skip, 0.5 * self.width + 31, 0.85 * self.height)
        self.draw_blt(rsc.btn_enter, 0.5 * self.width + 65, 0.85 * self.height)


    def draw_title(self, txt: str):
        self.draw_word(txt, 0.5 * self.width, 0.45 * self.height, y_var=1)

    def draw_lives(self, x: int, y: int, spacing=2):
        life_width = rsc.life_full.w
        for _ in range(self.lives_remaining):
            self.draw_blt(rsc.life_full, x, y)
            x -= (life_width + spacing)

        for _ in range(self.max_lives - self.lives_remaining):
            self.draw_blt(rsc.life_empty, x, y)
            x -= (life_width + spacing)

    def draw_word(
        self,
        word: Iterator[str],
        x: int,
        y: int,
        x_var=0,
        y_var=0,
        spacing=0,
        x_drift=0,
        y_drift=0,
    ):
        letter_width = rsc.ltrs["a"].w
        total_width = len(word) * (letter_width + spacing) - spacing

        # first letter position
        current_x = x - total_width // 2 + letter_width // 2
        for i in range(len(word)):
            l = word[i]
            self.draw_blt(
                rsc.ltrs[l],
                self.get_moving_position(
                    self.get_drift_position(current_x, x_var, i), x_drift
                ),
                self.get_moving_position(
                    self.get_drift_position(y, y_var, i)
                    - letter_width
                    // 4
                    * (self.is_selected and i == self.current_select),
                    y_drift,
                ),
            )
            current_x += letter_width + spacing

    def draw_blt(self, sprite: rsc.PyxelImg, x: int, y: int) -> None:
        """
        Draws with x, y as the center instead of the upper left corner
        """
        pyxel.blt(
            x - sprite.w // 2,
            y - sprite.h // 2,
            0,
            sprite.u,
            sprite.v,
            sprite.w,
            sprite.h,
        )

    def get_moving_position(self, pos: int, drift: int, drift_spd: int = 8):
        return self.get_drift_position(pos, drift, pyxel.frame_count // drift_spd)

    def get_drift_position(self, pos: int, drift: int, move_index: int):
        if drift == 0:
            return pos

        total_drift = 4 * drift
        actual_drift = move_index % total_drift
        if actual_drift >= total_drift // 2:
            actual_drift = total_drift - actual_drift

        actual_drift -= drift
        return pos + actual_drift

    def get_selector_x(self, x, spacing=0):
        letter_width = rsc.ltrs["a"].w
        total_width = len(self.current_guess) * (letter_width + spacing) - spacing
        current_x = x - total_width // 2 + letter_width // 2
        return current_x + self.current_select * (letter_width + spacing)


if __name__ == "__main__":
    dictionary = "https://www.mit.edu/~ecprice/wordlist.10000"
    engine = PomenohennApp(dictionary)
    engine.run()
