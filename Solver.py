import numpy as np
from heapdict import heapdict

import Solver
import queue
from Board import Board


def solve(board, search_method):
    _handle_output(*(getattr(Solver, '_' + search_method.lower())(board)))


def _handle_output(path, size, initial_state, goal_state, search_method, depth, num_created, num_expanded, max_fringe):
    print(f"SOLUTION PATH:\n{path}")
    f = open("Readme.txt", "a")
    f.write(
        f"\nSIZE: {size}\nINITIAL STATE:\n{initial_state}\nGOAL STATE:\n{goal_state}\nSEARCH METHOD:\n{search_method}\nDEPTH: {depth}, NUM CREATED: {num_created}, NUM EXPANDED: {num_expanded}, MAX FRINGE: {max_fringe}")


def _backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def _simple_search(board, q, search_method):
    depth = 0
    num_created = 0
    num_expanded = 0
    max_fringe = 0
    q.put(board)
    parent = {}
    possible_moves: list
    goal_state = board.get_goal_state_board()
    visited = set()
    board.depth = 0
    visited.add(board)

    while not q.empty():
        if q.qsize() > max_fringe:
            max_fringe = q.qsize()
        vertex = q.get()
        if vertex.depth < depth:
            depth = vertex.depth
        if vertex == goal_state:
            backtrace = _backtrace(parent, board, goal_state)
            return backtrace, board.get_size(), board, goal_state, search_method, depth, num_created, num_expanded, max_fringe
        num_expanded += 1
        if vertex.is_solvable():
            possible_moves = vertex.get_possible_moves()
            num_created += len(possible_moves)
            depth += 1
            for move in possible_moves:
                if move not in visited:
                    move.depth = depth
                    visited.add(move)
                    parent[move] = vertex
                    q.put(move)
    if vertex == goal_state:
        backtrace = _backtrace(parent, board, goal_state)
        return backtrace, board.get_size(), board, goal_state, search_method, depth, num_created, num_expanded, max_fringe
    return 'GOAL STATE NOT FOUND', board.get_size(), board, goal_state, search_method, -1, 0, 0, 0


def _bfs(board):
    return _simple_search(board, queue.Queue(), "bfs")


def _dfs(board):
    print("solving using dfs")
    return _simple_search(board, queue.LifoQueue(), "dfs")


def _gbfs(board):
    return _simple_search(board, queue.PriorityQueue(), "gbfs")


def _astar(board):
    depth = 0
    num_created = 0
    num_expanded = 0
    max_fringe = 0
    board.depth = 0
    open_set = heapdict()
    open_set[board] = board.get_manhattan_distance()
    parent = {}
    goal_state = board.get_goal_state_board()

    g_score = {}
    g_score[board] = 0

    f_score = {}
    f_score[board] = board.get_manhattan_distance()

    while len(open_set.items()) > 0:
        if len(open_set.items()) > max_fringe:
            max_fringe = len(open_set.items())
        current = open_set.popitem()[0]
        if current.depth < depth:
            depth = current.depth
        if current == goal_state:
            backtrace = _backtrace(parent, board, goal_state)
            return backtrace, current.get_size(), board, goal_state, 'a*', depth, num_created, num_expanded, max_fringe
        num_expanded += 1
        if current.is_solvable():
            depth += 1
            for move in current.get_possible_moves():
                num_created += 1
                tentative_g_score = g_score.get(current, np.Inf) + depth
                if tentative_g_score < g_score.get(move, np.Inf):
                    move.depth = depth
                    parent[move] = current
                    g_score[move] = tentative_g_score
                    f_score[move] = tentative_g_score + move.get_manhattan_distance()
                    if move not in open_set:
                        open_set[move] = f_score[move]
    if current == goal_state:
        backtrace = _backtrace(parent, board, goal_state)
        return backtrace, current.get_size(), board, goal_state, 'A*', depth, num_created, num_expanded, max_fringe
    return 'GOAL STATE NOT FOUND', board.get_size(), board, goal_state, 'A*', -1, 0, 0, 0

# class Solver:
#     pass
