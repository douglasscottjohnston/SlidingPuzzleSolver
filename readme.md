# Sliding Puzzle Solver
Solves 2x2, 3x3, or 4x4 sliding puzzles

## Description
I made this for a class project. It uses depth first search, breadth first search, greedy best first search, or A* to find the sequence of moves to solve a provided sliding puzzle.

## How to run
To run the program, run Tester.py with three arguments in this order:
1. Size: 2 for a 2x2 board, 3 for a 3x3 board, or 4 for a 4x4 board. Sizes greater than 4 aren't supported
2. Initial State: A string representing the initial "unsolved" state of the board. The state is represented in hex values (numbers 1-9 then A, B, C, D, E, F to represent 10, 11, 12, 13, 14, and 15 respectively) and a space for the empty square in the puzzle
3. Search Method: BFS for breadth first search, DFS for depth first search, GBFS for greedy best first search, or ASTAR for A*

Here are a few example commands to run the program:
- for a 2x2 board: python Tester.py 2 "2 31" BFS
- for a 3x3 board: python Tester.py 3 "2 1456378" DFS
- for a 4x4 board: python Tester.py 4 "3 2145E6FB7C8D9A" GBFS
- for A*: python Tester.py 2 "3 21" ASTAR

Once the program finishes, it will print the solution sequence to the terminal and write a report into Readme.txt
