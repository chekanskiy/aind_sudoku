from solution import *
import numpy as np


def square_num(coord_str):
    """Input string containing coordinates of a box i.e.  "45" Otputs square that the box belongs to"""
    if np.ceil((int(coord_str[0]) + 0.1) / 3) == 1:
        if np.ceil((int(coord_str[1]) + 0.1) / 3) == 1:
            return 0
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 2:
            return 1
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 3:
            return 2
    elif np.ceil((int(coord_str[0]) + 0.1) / 3) == 2:
        if np.ceil((int(coord_str[1]) + 0.1) / 3) == 1:
            return 3
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 2:
            return 4
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 3:
            return 5
    elif np.ceil((int(coord_str[0]) + 0.1) / 3) == 3:
        if np.ceil((int(coord_str[1]) + 0.1) / 3) == 1:
            return 6
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 2:
            return 7
        elif np.ceil((int(coord_str[1]) + 0.1) / 3) == 3:
            return 8
    else:
        return False


def generate_sudoku():
    """Generates sudoku puzzle as a np array and returns it as a string"""

    digits = '123456789'
    indices = '012345678'
    board = np.zeros([9, 9])
    box_indices = [[int(x), int(y)] for x in indices for y in indices]
    squares = [[[int(x[0]), int(x[1])] for x in cross(rs, cs)] for rs in ('012', '345', '678') for cs in
               ('012', '345', '678')]

    def random_value(board):
        """Fills a random box with a random value and checks if it satisfies sudoku rules (except for diagonal rule)"""
        board_ = board.copy()
        try:
            choice = np.random.choice(range(len(box_indices)))  # select random box
            ind = box_indices[choice]  # select random boxe's coordinates
            # TODO: Sometimes the generation takes a lot of time especially if the following line is uncommented
            # del box_indices[choice]  # remove that box as a possible choice for next iteration
            rand_digit = np.random.randint(int(digits[0]), int(len(digits) + 1))  # generate random value
            board_[ind[0], ind[1]] = rand_digit   # assign the value to the box
            # check that respective rows and columns have this value exactly once
            assert all([board_[ind[0], int(x)] != rand_digit for x in (set([int(y) for y in indices]) - {ind[1]})])
            assert all([board_[int(x), ind[1]] != rand_digit for x in (set([int(y) for y in indices]) - {ind[0]})])
            # check that square unit that the box belongs to has this value exactly once
            assert len(
                [x for x in squares[square_num("".join(str(k) for k in ind))] if board_[x[0], x[1]] == rand_digit]) == 1
            return True, board_
        except:
            # if any assertion failed start over
            return False, board

    # TODO: Sometimes it produces really hard puzzles. Make sure no unsolvable ones can be generated (so far its ok)

    unique_digit_check = 0
    while unique_digit_check < 10:  # Sudoku must contain minimum 9 different digits
        for i in range(18):  # Fill minimum 17 squares
            check = False
            while check is False:
                check, board = random_value(board)
                unique_digit_check = len(set(board.flatten()))
    # Returns board coded as a string
    return ''.join([str(int(x)).replace('0', '.') for x in board.flatten()])


def generate_solve(iterations):
    f = open('generated_and _solved_sudokus.txt', 'w')
    f.write('grid,time_to_solve' + '\n')
    f.close()
    from datetime import datetime
    for i in range(iterations):
        f = open('generated_and _solved_sudokus.txt', 'a')
        grid = generate_sudoku()
        f.write(grid + ',')
        f.close()
        t1 = datetime.now()
        solve(grid)
        time = datetime.now() - t1
        f = open('generated_and _solved_sudokus.txt', 'a')
        f.write(str(time.total_seconds()) + '\n')
        f.close()

if __name__ == '__main__':

    generate_solve(500)

