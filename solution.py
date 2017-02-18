import re
assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for box in unit:
            box_len = len(values[box])
            box_copy = [bx for bx in (set(unit) - {box}) if values[bx] == values[box]]
            if box_len == 2 and box_copy:
                bad_chars = values[box]
                rgx = re.compile('[%s]' % bad_chars)
                for other_boxes in set(unit) - {box, box_copy[0]}:
                    values[other_boxes] = rgx.sub('', values[other_boxes])
    return values


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [x+y for x in A for y in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    return {k: v for k, v in
           zip(boxes,
               [g if g != '.' else '123456789' for g in grid]
              )
           } # dict(zip(boxes, grid))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(sudoku_dict):
    """If a box has single digit then eliminate that digit choice from all the peers"""
    for box in sudoku_dict.keys():
        if len(sudoku_dict[box]) == 1: # digits
            for peer in peers[box]: # all peers for the box
                sudoku_dict[peer] = sudoku_dict[peer].replace(sudoku_dict[box], "") # remove digit and replace in dict
    return sudoku_dict


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for num in '123456789':
            choices = [box for box in unit if num in values[box]]
            if len(choices) == 1:
                values[choices[0]] = num
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Use naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, try all possible values."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    # min function compares first elements of passed lists and outputs a list with minimum 1st element
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]: # recursively explore every option untill we find a solution
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))


def board(diagonal=True):
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]


    unitlist = row_units + column_units + square_units

    if diagonal:
        diagonal_unit_1 = [row_units[a][b] for a, b in zip(range(0, 9), range(0, 9))]
        diagonal_unit_2 = [row_units[::-1][a][b] for a, b in zip(range(0, 9), range(0, 9))]
        diagonal_units = [diagonal_unit_1, diagonal_unit_2]
        unitlist = unitlist + diagonal_units

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)  # {} - set literal, executes x2 faster than set()

    return rows, cols, units, peers, unitlist, boxes


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]


unitlist = row_units + column_units + square_units

diagonal = True
if diagonal:
    diagonal_unit_1 = [row_units[a][b] for a, b in zip(range(0, 9), range(0, 9))]
    diagonal_unit_2 = [row_units[::-1][a][b] for a, b in zip(range(0, 9), range(0, 9))]
    diagonal_units = [diagonal_unit_1, diagonal_unit_2]
    unitlist = unitlist + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)  # {} - set literal, executes x2 faster than set()

if __name__ == '__main__':

    rows, cols, units, peers, unitlist, boxes = board()

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
