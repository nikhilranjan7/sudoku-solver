import copy

rows = 'ABCDEFGHI'
cols = '123456789'

#For pygame visualizations
assignments = []
def assign_value(values, box, value):
    """
    function to update values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
#End pygame visualization

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    twins = [box for box in values.keys() if len(values[box]) == 2]
    naked_twin = []
    for box in twins:
        digit = values[box]
        for peer in peers[box]:
            if digit==values[peer] and peer != box:
                naked_twin.append((box,peer))

    if len(naked_twin) == 0:
        return values
    # Eliminate the naked twins as possibilities for their peers

    for m,n in naked_twin:
        if len(values[m]) != 2:
            return values
            
        first_digit = values[m][0]
        second_digit = values[m][1]

        # Row wise elimination
        if m[0]==n[0]:
            for row in row_units:
                if m in row:
                    for element in row:
                        if first_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(first_digit,'')
                        if second_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(second_digit,'')


        # Column wise elimination
        if m[1]==n[1]:
            for column in column_units:
                if m in column:
                    for element in column:
                        if first_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(first_digit,'')
                        if second_digit in values[element] and m != element and n != element:
                            values[element] = values[element].replace(second_digit,'')

        # Square wise elimination
        for square in square_units:
            if m in square and n in square:
                for element in square:
                    if first_digit in values[element] and m != element and n!= element:
                        values[element] = values[element].replace(first_digit,'')
                    if second_digit in values[element] and m != element and n!= element:
                        values[element] = values[element].replace(second_digit,'')
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # For pygame assigning
    #for key in values:

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Chose one of the unfilled square s with the fewest possibilities

    square = 'To find'
    possibilities = {}
    for box in boxes:
        possibilities[box] = len(values[box])

    for i in range(2,10):
        found = 0
        for key in possibilities:
            if (possibilities[key]==i):
                square = key
                found = 1
                break
        if found == 1 :
            break

    sudokus = []
    for j in range(len(values[square])):
        dict2 = copy.deepcopy(values)
        sudokus.append(dict2)

    count = 0

    for digit in values[square]:
        sudokus[count][square] = digit
        assign_value(values, square, digit)
        count = count + 1

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for sudoku in sudokus:
        new_sudoku = copy.deepcopy(sudoku)
        attempt = search(new_sudoku)
        if attempt:
            return attempt
