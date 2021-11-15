class PyxelImg:
    def __init__(self, u, v, w, h):
        self.u = u
        self.v = v
        self.w = w
        self.h = h


btn_enter = PyxelImg(0, 0, 29, 10)
btn_skip = PyxelImg(0, 16, 33, 10)
btn_move = PyxelImg(0, 32, 42, 10)
btn_select = PyxelImg(0, 48, 46, 10)

# ui
selector = PyxelImg(0, 64, 16, 4)

# letters for fast lookup
ltrs = {
    "a": PyxelImg(0, 72, 16, 16),
    "b": PyxelImg(16, 72, 16, 16),
    "c": PyxelImg(32, 72, 16, 16),
    "d": PyxelImg(48, 72, 16, 16),
    "e": PyxelImg(64, 72, 16, 16),
    "f": PyxelImg(80, 72, 16, 16),
    "g": PyxelImg(96, 72, 16, 16),
    "h": PyxelImg(0, 88, 16, 16),
    "i": PyxelImg(16, 88, 16, 16),
    "j": PyxelImg(32, 88, 16, 16),
    "k": PyxelImg(48, 88, 16, 16),
    "l": PyxelImg(64, 88, 16, 16),
    "m": PyxelImg(80, 88, 16, 16),
    "n": PyxelImg(96, 88, 16, 16),
    "o": PyxelImg(0, 104, 16, 16),
    "p": PyxelImg(16, 104, 16, 16),
    "q": PyxelImg(32, 104, 16, 16),
    "r": PyxelImg(48, 104, 16, 16),
    "s": PyxelImg(64, 104, 16, 16),
    "t": PyxelImg(80, 104, 16, 16),
    "u": PyxelImg(96, 104, 16, 16),
    "v": PyxelImg(0, 120, 16, 16),
    "w": PyxelImg(16, 120, 16, 16),
    "x": PyxelImg(32, 120, 16, 16),
    "y": PyxelImg(64, 120, 16, 16),
    "z": PyxelImg(80, 120, 16, 16),
}

# qn no.
qns = {
    1: PyxelImg(0, 136, 16, 16),
    2: PyxelImg(16, 136, 16, 16),
    3: PyxelImg(32, 136, 16, 16),
    4: PyxelImg(48, 136, 16, 16),
    5: PyxelImg(64, 136, 16, 16),
    6: PyxelImg(0, 152, 16, 16),
    7: PyxelImg(16, 152, 16, 16),
    8: PyxelImg(32, 152, 16, 16),
    9: PyxelImg(48, 152, 16, 16),
    10: PyxelImg(64, 152, 16, 16),
}

mark_neutral = PyxelImg(0, 168, 4, 4)
mark_success = PyxelImg(4, 168, 4, 4)
mark_fail = PyxelImg(8, 168, 4, 4)

life_full = PyxelImg(16, 168, 14, 12)
life_empty = PyxelImg(32, 168, 14, 12)
