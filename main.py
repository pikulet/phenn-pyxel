from app import Pomenohenn
import pyxel

class PomenohennApp:

    def __init__(self, dictionary, min_word_length=6, max_word_length=12, max_tries=3, max_questions=10):
        self.phenn = Pomenohenn(dictionary, min_word_length, max_word_length)
        # try counter
        self.max_tries = max_tries
        self.tries_remaining = max_tries
        # ui selector
        self.current_guess = None
        self.is_selected = False
        self.current_select = 0
        self.max_select = 0
        # scoring
        self.max_questions = max_questions
        self.total_questions = 0
        self.correct_questions = 0

        pyxel.init(180, 100, caption="Pomenohenn")
        pyxel.load("rsc.pyxres")
        pyxel.run(self.update, self.draw)

    def new_question(self):
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

    def update(self):
        if not self.phenn.is_started():
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.new_question()
            return
        
        if pyxel.btnp(pyxel.KEY_ENTER):
            # make guess
            if ''.join(self.current_guess) == self.phenn.answer:
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
                self.current_guess[self.current_select], self.current_guess[self.current_select - 1] = self.current_guess[self.current_select - 1], self.current_guess[self.current_select]
            self.current_select -= 1
            return

        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.current_select == self.max_select:
                return
            if self.is_selected:
                self.current_guess[self.current_select], self.current_guess[self.current_select + 1] = self.current_guess[self.current_select + 1], self.current_guess[self.current_select]  
            self.current_select += 1
            print(self.get_state_str())
            return

    def draw(self):
        if self.phenn.question is None:
            self.draw_intro()
            return

        #pyxel.text(55, 41, self.get_state_str(), pyxel.frame_count % 16)
        # draw decorators
        # draw question at top
        # draw current guess
        # draw selector

    def draw_intro(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 30, 30, 21, 10)

if __name__ == "__main__":
    dictionary = "https://www.mit.edu/~ecprice/wordlist.10000"
    engine = PomenohennApp(dictionary)
    engine.run()
