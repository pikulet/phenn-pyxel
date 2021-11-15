from app import Pomenohenn
import rsc
import pyxel
import math


class PomenohennApp:
    def __init__(
        self,
        dictionary,
        width=180,
        height=100,
        min_word_length=6,
        max_word_length=12,
        max_tries=3,
        max_questions=10,
    ):

        self.phenn = Pomenohenn(dictionary, min_word_length, max_word_length)

        # try counter
        self.max_tries: int = max_tries
        self.tries_remaining: int = max_tries
        # ui selector
        self.current_guess: list[str] = None
        self.is_selected: bool = False
        self.current_select: int = 0
        self.max_select: int = 0
        # scoring
        self.max_questions: int = max_questions
        self.total_questions: int = 0
        self.correct_questions: int = 0

        self.width = width
        self.height = height

        pyxel.init(self.width, self.height, caption="Pomenohenn")
        pyxel.load("rsc.pyxres")
        pyxel.run(self.update, self.draw)

    def new_question(self) -> None:
        if self.total_questions == self.max_questions:
            self.phenn.reset()
            return

        self.phenn.generate_question()
        # reset state
        self.tries_remaining = self.max_tries
        self.current_guess = list(self.phenn.question)
        self.is_selected = False
        self.current_select = 0
        self.max_select = len(self.current_guess)
        self.total_questions += 1

    def update(self) -> None:
        if not self.phenn.is_started():
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.new_question()
            return

        if pyxel.btnp(pyxel.KEY_ENTER):
            # make guess
            if "".join(self.current_guess) == self.phenn.answer:
                self.correct_questions += 1
                self.new_question()
                return
            # wrong answer
            self.tries_remaining -= 1
            if self.tries_remaining == 0:
                self.new_question()
                return

        if pyxel.btnp(pyxel.KEY_Z):
            # skip all tries
            self.new_question()
            return

        if pyxel.btnp(pyxel.KEY_SPACE):
            # activate selector
            self.is_selected = not self.is_selected
            return

        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.current_select == 0:
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
            print(self.get_state_str())
            return

    def draw(self) -> None:
        if self.phenn.question is None:
            self.draw_intro()
            return

        # pyxel.text(55, 41, self.get_state_str(), pyxel.frame_count % 16)
        # draw decorators
        # draw question at top
        # draw current guess
        # draw selector

    def draw_intro(self):
        pyxel.cls(0)

        # title

        # enter
        self.draw_blt(
            rsc.btn_enter,
            self.get_moving_position(self.width // 2, 5),
            3 * self.height // 4,
        )

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

    def get_moving_position(self, pos, drift):
        return pos

if __name__ == "__main__":
    dictionary = "https://www.mit.edu/~ecprice/wordlist.10000"
    engine = PomenohennApp(dictionary)
    engine.run()
