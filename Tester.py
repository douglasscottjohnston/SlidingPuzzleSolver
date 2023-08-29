import sys
from Board import Board
import Solver


def main():
    size = int(sys.argv[1])
    initial_state = sys.argv[2]
    search_method = sys.argv[3]
    if search_method not in ["BFS", "DFS", "GBFS", "ASTAR"]:
        raise Exception("The search method must be one of the following: BFS, DFS, GBFS, ASTAR ")
    board = Board(size, size, initial_state)
    Solver.solve(board, search_method)


if __name__ == '__main__':
    main()
