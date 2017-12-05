assignments = []
rows = 'ABCDEFGHI'
columns = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for i in A for j in B]

boxes = cross(rows,columns)
row_units = [cross(r,columns) for r in rows]
column_units = [cross(rows, c) for c in columns]
square_units = [cross(r,c) for c in ('123','456','789') for r in ('ABC','DEF','GHI')]
# creating the lists of boxes that are in the diagonal
diagonal_units = [[r+c for r,c in zip(rows,columns)],[r+c for r,c in zip(rows,columns[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((b, [u for u in unitlist if b in u]) for b in boxes)
peers = dict((b, set(sum(units[b],[]))-set([b])) for b in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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
        # getting all possible twins as tuples
        possibletwintuples = [(b, values[b]) for b in unit if len(values[b]) == 2]
        temp_dict = {}
        for t in possibletwintuples:
            if t[1] not in temp_dict.keys():
                temp_dict[t[1]] = [t[0]]
            else:
                temp_dict[t[1]].append(t[0])
        # getting the list of all twins
        twin_dict = {k:v for k,v in temp_dict.items() if len(v)>1}
        for dValue,twin_boxes in twin_dict.items():
            # getting the list of common peers to the twin boxes
            common_peers = set(peers[twin_boxes[0]]).intersection(peers[twin_boxes[1]])
            # getting the list of boxes that have either or both the twin values
            boxes_to_update = [b for b in common_peers if((dValue[0] in values[b] or dValue[1] in values[b]) and (dValue != values[b]))]
            for bu in boxes_to_update:
                # removing the twin values from the common peers
                assign_value(values, bu, values[bu].replace(dValue[0], '').replace(dValue[1],''))
    return values


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
    updated_grid_values = []
    for grid_value in grid:
        if grid_value == '.':
            updated_grid_values.append('123456789')
        else:
            updated_grid_values.append(grid_value)
    return dict(zip(boxes, updated_grid_values))


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
                      for c in columns))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key,value in values.items():
        if(len(value) == 1):
            for peer in peers[key]:
                    assign_value(values, peer, values[peer].replace(value,""))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            sBox = [box for box in unit if digit in values[box]]
            if(len(sBox)==1):
                assign_value(values, sBox[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Using the naked twins strategy
        values = naked_twins(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values) 
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if(values == False):
        return False
    if all(len(values[box])==1 for box in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,us = min((len(values[box]),box) for box in boxes if len(values[box])>1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[us]:
        new_sudoku = values.copy()
        new_sudoku[us] = digit
        solved = search(new_sudoku)
        if solved:
            return solved

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solved = search(values)
    if solved:
        return solved
    else:
        return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
