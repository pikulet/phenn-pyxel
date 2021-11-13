from app import Pomenohenn
import pyxel

class PomenohennApp:

    def __init__(self, dictionary, min_word_length=6, max_word_length=12, max_tries=3, max_questions=10):
        self.phenn = Pomenohenn(dictionary, min_word_length, max_word_length)
        # try counter
        self.max_tries = max_tries
        self.tries = 0
        # ui selector
        self.current_guess = None
        self.is_selected = False
        self.current_select = 0
        self.max_select = 0
        # scoring
        self.max_questions = max_questions
        self.total_questions = 0
        self.correct_questions = 0

        pyxel.init(160, 120, caption="Pomenohenn")
        pyxel.run(self.update, self.draw)

    def new_question(self):
        if self.total_questions == self.max_questions:
            self.phenn.reset()
            return

        self.phenn.generate_question()
        # reset state
        self.tries = 0
        self.current_guess = list(self.phenn.question)
        self.is_selected = False
        self.current_select = 0
        self.max_select = len(self.current_guess)
        self.total_questions += 1

    def update(self):
        if not self.phenn.is_started():
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.new_question()
                print(self.get_state_str())
            return
        
        if pyxel.btnp(pyxel.KEY_ENTER):
            # make guess
            if ''.join(self.current_guess) == self.phenn.answer:
                self.correct_questions += 1
                self.new_question()
                print(self.get_state_str())
                return
            # wrong answer
            self.tries += 1
            if self.tries == self.max_tries:
                self.new_question()
                print(self.get_state_str())
                return
            print(self.get_state_str())

        if pyxel.btnp(pyxel.KEY_Z):
            # skip all tries
            self.new_question()
            print(self.get_state_str())
            return

        if pyxel.btnp(pyxel.KEY_SPACE):
            # activate selector
            self.is_selected = not self.is_selected
            print(self.get_state_str())
            return

        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.current_select == 0:
                print(self.get_state_str())
                return
            if self.is_selected:
                self.current_guess[self.current_select], self.current_guess[self.current_select - 1] = self.current_guess[self.current_select - 1], self.current_guess[self.current_select]
            self.current_select -= 1
            print(self.get_state_str())
            return

        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.current_select == self.max_select:
                print(self.get_state_str())
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
        pass

    def get_state_str(self):
        selector = f"tries:{self.tries},current_guess:{self.current_guess},is_selected:{self.is_selected},current_select:{self.current_select}"
        questions = f"total_questions:{self.total_questions},correct_questions:{self.correct_questions}"
        phenn = f"qn:{self.phenn.question},ans:{self.phenn.answer}"
        return selector + questions + phenn

if __name__ == "__main__":
    dictionary = "https://www.mit.edu/~ecprice/wordlist.10000"
    engine = PomenohennApp(dictionary)
    engine.run()
