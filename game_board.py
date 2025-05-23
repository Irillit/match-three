"""Logical representation of the board."""
import numpy as np


class GameBoard:
    """Logical representation of the board."""

    def __init__(self, width: int, heigh: int, max_val: int):
        self._width = width
        self._height = heigh
        self._max_val = max_val

        self._board = None
        self._changed = False
        self.regenerate_board()
        self._selected_item: tuple[int, int] | None = None
        self._score = 0

    def ensure_no_matches(self):
        """Ensure that no match-three lines or columns are available initially."""
        while True:
            self._changed = False
            self.detect_row(set_score=False)
            self.detect_column()

            if not self._changed:
                break

    @property
    def board(self):
        return self._board

    @property
    def selected_item(self):
        return self._selected_item

    @property
    def score(self):
        return self._score

    def select_item(self, position: tuple[int, int]):
        self._selected_item = position

    def remove_selection(self):
        self._selected_item = None

    def regenerate_board(self):
        """Fill board and reset the score."""
        self._board = np.random.randint(low=0, high=self._max_val, size=(self._width, self._height))
        self._score = 0
        self.ensure_no_matches()

    def are_swappable(self, pos1: tuple[int, int]) -> bool:
        """Check if two points are swappable."""

        # TODO: check color
        if not self._selected_item:
            return False

        pos2 = self._selected_item
        if pos1[0] == pos2[0]:
            if abs(pos1[1] - pos2[1]) == 1 or abs(pos2[1] - pos1[1]) == 1:
                return True
        elif pos1[1] == pos2[1]:
            if abs(pos1[0] - pos2[0]) == 1 or abs(pos2[0] - pos1[0]) == 1:
                return True

        return False

    def swap(self, pos1: tuple[int, int]):
        """Change positions of two neighbour elements."""
        y1, x1 = pos1
        y2, x2 = self._selected_item
        self._board[x1, y1], self._board[x2, y2] = self._board[x2, y2], self._board[x1, y1]

    def remove_and_shift_row(self, start: int, end: int, row: int, set_score: bool):
        """Move down and generate a new row on top."""
        self._changed = True

        if set_score:
            self._score += end - start + 1

        end = end + 1  # to use in slices
        for i in range(row, -1, -1):
            if i == 0:
                self._board[i, start:end] = np.random.randint(low=0,
                                                              high=self._max_val,
                                                              size=end-start)
                print("Regenerated after row deletion")
            else:
                self._board[i, start:end] = self._board[i-1, start:end]

    def remove_and_shift_column(self, start: int, end: int, column: int, set_score:bool):
        """Move down and generate a new column on top."""
        self._changed = True
        delta = end - start + 1

        if set_score:
            self._score += delta
        for i in range(start, -1, -1):
            self._board[i + delta][column] = self._board[i][column]

            if i == 0:
                for k in range(i, i + delta + 1):
                    self._board[k][column] = np.random.randint(0, self._max_val)

        print("Regenerated after row column deletion")

    def detect_row(self, set_score: bool = True):
        """Detects 3 or more elements in the row."""
        length = 0
        start = 0
        color = self._board[0, 0]

        for i in range(self._width):
            for j in range(self._height):
                current = self._board[i, j]
                if j == 0:
                    color = current
                    length = 0
                    start = 0

                if length > 2 and current != color:
                    print(f"Found row from {start} to {j - 1} at line {i} symbol: {color}")
                    self.remove_and_shift_row(start, j - 1, i, set_score)
                    length = 0
                    start = j
                    color = current

                if current == color:
                    length += 1
                else:
                    color = current
                    length = 1
                    start = j

            if length > 2:
                print(f"Found row from {start} to {self._width} at line {i} symbol: {color}")
                self.remove_and_shift_row(start, self._width - 1, i, set_score)

    def detect_column(self, set_score: bool = True):
        """Detects 3 or more elements in the column."""
        length = 0
        start = 0
        color = self._board[0, 0]

        for j in range(self._height):
            for i in range(self._width):
                current = self._board[i, j]
                if i == 0:
                    color = current
                    length = 0
                    start = 0

                if length > 2 and current != color:
                    print(f"Found column from {start} to {i - 1} at line {j} symbol: {color}")
                    self.remove_and_shift_column(start, i-1, j, set_score)
                    length = 0
                    start = i
                    color = current

                if current == color:
                    length += 1
                else:
                    color = current
                    length = 1
                    start = i

            if length > 2:
                print(f"Found column from {start} to {self._width} at line {j} symbol: {color}. Out the innner loop.")
                self.remove_and_shift_column(start, self._width-1, j, set_score)
