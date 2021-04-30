# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from hunspell import Hunspell
import itertools

MAX_BOARD_SIZE = 12

verbose = False

class Cell:
    def __init__(self, i, j, c = ""):
        self.i = i
        self.j = j
        self.c = c
        self.cache = None
        self.dirty = []

    def save(self, dirty):
        self.dirty.append(dirty)
        if dirty:
            self.cache = self.c

    def restore(self):
        if self.cache is None:
            return
        if self.dirty.pop():
            self.c = self.cache
            self.cache = None

class Board:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        result = "=============================================\n"
        for row in self.content:
            for cell in row:
                result += cell.c.center(5)
            result += '\n'
        result += "=============================================\n"
        return result

class WordScapeSolver:
    def __init__(self):
        self.h = Hunspell("en_US", "en_US")

    def solve_wordscape_helper(self, valid_words, letters, length):
        p = set(itertools.permutations(letters, length))

        for raw_string in p:
            word = "".join(raw_string)
            if self.h.spell(word):
                valid_words.append(word)

    def try_fit(self, board, i, j, horizontal, word, length, valid_words):
        if horizontal:
            for k in range(length):
                if board.content[i][j + k].c == ".":
                    board.content[i][j + k].save(True)
                    board.content[i][j + k].c = word[k]
                elif board.content[i][j + k].c == word[k]:
                    board.content[i][j + k].save(False)
                else:
                    for l in range(k):
                        board.content[i][j + l].restore()
                    return False

            new_word_list = valid_words.copy()
            new_word_list.remove(word)
            if verbose:
                print(board)
            success = self.try_solve(board, i, j, new_word_list)
            if not success:
                for l in range(length):
                    board.content[i][j + l].restore()
                return False
            else:
                return True

        else:
            for k in range(length):
                if board.content[i + k][j].c == ".":
                    board.content[i + k][j].save(True)
                    board.content[i + k][j].c = word[k]
                elif board.content[i + k][j].c == word[k]:
                    board.content[i + k][j].save(False)
                else:
                    for l in range(k):
                        board.content[i + l][j].restore()
                    return False

            new_word_list = valid_words.copy()
            new_word_list.remove(word)
            if verbose:
                print(board)
            success = self.try_solve(board, i, j, new_word_list)
            if not success:
                for l in range(length):
                    board.content[i + l][j].restore()
                return False
            else:
                return True

    def find_unfilled_word(self, board, i, j, horizontal):
        empty_spot = False

        if horizontal:
            length = 0
            for k in range(j, MAX_BOARD_SIZE):
                if not empty_spot and board.content[i][k].c == ".":
                    empty_spot = True

                if board.content[i][k].c == "":
                    exist = empty_spot and length > 1
                    return exist, length
                length += 1
        else:
            length = 0
            for k in range(i, MAX_BOARD_SIZE):
                if not empty_spot and board.content[k][j].c == ".":
                    empty_spot = True

                if board.content[k][j].c == "":
                    exist = empty_spot and length > 1
                    return exist, length
                length += 1

        return False, 0

    def find_next_word(self, board, i, j):
        for p in range(MAX_BOARD_SIZE):
            if p < i:
                continue

            for q in range(MAX_BOARD_SIZE):
                if p == i and q < j:
                    continue
                exist, length = self.find_unfilled_word(board, p, q, True)
                if exist:
                    return False, p, q, True, length
                exist, length = self.find_unfilled_word(board, p, q, False)
                if exist:
                    return False, p, q, False, length
        return True, 0, 0, True, 0

    def try_solve(self, board, i, j, valid_words):
        finished, i, j, horizontal, length = self.find_next_word(board, i, j)

        if finished:
            return True

        candidates = []
        for word in valid_words:
            if len(word) == length:
                candidates.append(word)

        while len(candidates) > 0:
            if self.try_fit(board, i, j, horizontal, candidates.pop(), length, valid_words):
                return True

        return False

    def solve_board(self, valid_words, board):
        return self.try_solve(board, 0, 0, valid_words)

    def solve(self, letters, length, board=None):
        letters = letters.lower()
        valid_words = []
        for i in range(length, len(letters) + 1):
            self.solve_wordscape_helper(valid_words, letters, i)

        for word in valid_words:
            print(word)

        #valid_words =
        if not board is None:
            if self.solve_board(valid_words, board):
                print(board)
            else:
                print("No Solutions!")

def read_board_from_csv(filepath):
    board = []
    with open(filepath) as fp:
        i = 0
        for line in fp:
            board_row = []
            row = line.split(',')

            j = 0
            for cell in row:
                board_row.append(Cell(i, j, cell.lower()))
                j += 1

            for k in range(j, MAX_BOARD_SIZE):
                board_row.append(Cell(i, k))

            board.append(board_row)
            i += 1

        for k in range(i, MAX_BOARD_SIZE):
            board_row = []
            for l in range(MAX_BOARD_SIZE):
                board_row.append(Cell(k, l))
            board.append(board_row)

        return Board(board)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    w = WordScapeSolver()
    b = read_board_from_csv("board.csv")
    print(b)
    #w.solve("etivom", 3, b)
    w.solve("ohlesv", 3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
