from enum import Enum

import numpy as np


# Author: Douglas Johnston
# The Board of the sliding puzzle problem
def _is_even(n):
    return n % 2 == 0


def _get_row_column_dictionary(row, column):
    return {"row": row, "column": column}


def _manhattan_distance(point1, point2):
    return np.sum(np.abs(point1 - point2))


class Board:
    _state = [[]]
    depth = 0;

    def __init__(self, rows, columns, initial_state):
        if len(initial_state) / rows != columns:
            raise Exception(f"An initial state of length {len(initial_state)} is invalid for a {rows}x{columns} board")
        self._rows = rows
        self._columns = columns
        self._initial_state = initial_state
        self._space_index = (0, 0)
        self._initialize_board()
        self._is_solvable = self._test_if_solvable()

    def __repr__(self):
        return '\n' + str(self)

    def __str__(self):
        return str(np.matrix(self._state))

    def __eq__(self, other):
        return self._state == other.get_state()

    def __lt__(self, other):
        return self.get_manhattan_distance() < other.get_manhattan_distance()

    def __le__(self, other):
        return self.get_manhattan_distance() <= other.get_manhattan_distance()

    def __gt__(self, other):
        return self.get_manhattan_distance() > other.get_manhattan_distance()

    def __hash__(self):
        return hash(self.get_state_string())

    def _initialize_board(self):
        self._state = [[0] * self._rows for i in range(self._columns)]
        i, j = 0, 0
        for c in self._initial_state:
            self._state[i][j] = c
            if c == ' ':
                self._space_index = (i, j)
            j += 1
            if j == self._columns:
                i += 1
                j = 0

    def _test_if_solvable(self):
        inversions = self._count_inversions()
        if _is_even(self._rows):
            return not _is_even(inversions + self._space_index[0]) or inversions == 0
        else:
            return _is_even(inversions)

    def _count_inversions(self):
        inversions = 0
        for i in range(self._rows):
            for j in range(i + 1, self._columns):
                if self._initial_state[i] != ' ' and self._initial_state[j] != ' ' and self._initial_state[i] > \
                        self._initial_state[j]:
                    inversions += 1
        return inversions

    def _generate_goal_state_string(self):
        state = ''
        for i in range(1, self.get_size() * self.get_size() + 1):
            if i < 10:
                state = state + chr(i + ord('0'))
            elif i == self.get_size() * self.get_size():
                state = state + ' '
            else:
                state = state + chr(i + 55)
        return state

    def is_solvable(self):
        return self._is_solvable

    def get(self, row, column):
        return self._state[row][column]

    def get_size(self):
        return self._rows

    def get_state(self):
        return self._state

    def get_surrounding_indices(self, row, column):
        indices = {
            "top_left": _get_row_column_dictionary(row - 1, column - 1),
            "top": _get_row_column_dictionary(row - 1, column),
            "top_right": _get_row_column_dictionary(row - 1, column + 1),
            "middle_left": _get_row_column_dictionary(row, column - 1),
            "middle_right": _get_row_column_dictionary(row, column + 1),
            "bottom_left": _get_row_column_dictionary(row + 1, column - 1),
            "bottom_middle": _get_row_column_dictionary(row + 1, column),
            "bottom_right": _get_row_column_dictionary(row + 1, column + 1),
        }

        for item in indices.items():
            if item[1]["row"] < 0 or item[1]["column"] < 0 or item[1]["row"] >= self._rows or item[1][
                "column"] >= self._columns:
                indices[item[0]] = False

        return indices

    def get_possible_moves(self):
        possible_moves = []

        for move in Move:
            board = Board(self._rows, self._columns, self.get_state_string())
            if board.move(move):
                possible_moves.append(board)
        return possible_moves

    def move(self, move):
        space_indices = self.get_surrounding_indices(self.get_space_index()[0], self.get_space_index()[1])
        if not space_indices[move.value]:
            return False
        temp = self._state[space_indices[move.value]['row']][space_indices[move.value]['column']]
        self._state[space_indices[move.value]['row']][space_indices[move.value]['column']] = ' '
        self._state[self.get_space_index()[0]][self.get_space_index()[1]] = temp
        return True

    def get_state_string(self) -> str:
        state_string = ''

        for i in range(self._rows):
            for j in range(self._columns):
                state_string = state_string + self._state[i][j]
        return state_string

    def get_space_index(self):
        return self._space_index

    def get_goal_state_board(self):
        if self.get_size() == 2:
            return Board(self.get_size(), self.get_size(), '213 ')
        elif self.get_size() == 3:
            return Board(self.get_size(), self.get_size(), ' 12345678')
        elif self.get_size() == 4:
            return Board(self.get_size(), self.get_size(), '123456789ABCDEF ')
        else:
            return Board(self.get_size(), self.get_size(), self._generate_goal_state_string())

    def get_manhattan_distance(self):
        distance = 0
        for i in range(self._rows):
            for j in range(self._columns):
                distance += _manhattan_distance(np.array([i, j]),
                                                np.argwhere(
                                                    np.array(self.get_goal_state_board().get_state()) ==
                                                    self._state[i][j]))
        return distance

    def print(self):
        print(np.matrix(self._state))


class Move(Enum):
    UP = 'top'
    DOWN = 'bottom_middle'
    LEFT = 'middle_left'
    RIGHT = 'middle_right'
