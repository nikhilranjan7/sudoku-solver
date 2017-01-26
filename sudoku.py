from utils import *
import copy

def solve(grid):
    """
    Solving the sudoku using function in utils.py
    Input: The sudoku in string format of 81 characters
    Output: None
    """
    #converting '.' to possible answers. Values is a dictionary that contains box as key
    #and its possible answers as its value.
    values = grid_values(grid)

    #solving the sudoku
    values = search(values)

    #displaying the answer
    display(values)

if __name__ == '__main__':
    grid = input('type sudoku as a long string of 81 characters with . as unsolved place\n')
    solve(grid)
