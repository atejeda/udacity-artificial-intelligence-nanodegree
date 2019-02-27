assignments = []

# these ones can be enable, disabled from solution_test.py
debug = False
interactive = False

def dbg(*args, i=True, d=True):
    """
    Simple function to be used as a debugger, relies
    on module variables: debug and interactive
    """
    print(*args) if debug and d else None
    input("press enter to continue...") if interactive and i else None

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
    """
    Eliminate values using the naked twins strategy.
    
    This method doesn't consider the square units, reason is the twins
    might not be in the same square unit.
    
    The elimination only considers the current unit being processed
    (rows, columns, diagonals) and if the twins are in the same square,
    then the square is included to be checked to see if there's a box with
    the any of the twins values.

    If the debug variable is set to True, a valid elimination would be logged as:

    units     = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], candidates = ['C1', 'C4']
    register  = {'23': {'C1', 'C4'}}
    squares   = {'A1', 'A4'}
    process   = ['C2', 'C3', 'C5', 'C6', 'C7', 'C8', 'C9']
    processed = ['C6 for 2', 'C5 for 3', 'C6 for 3']

    The constraint propagation is being applied as each affected unit is being processed,
    the order of processing is row, columns and diagonals, each one consider the square
    if both twins are in the same square.

    This algorithm could be also be processed several times until there's no
    more valid twins or no changes in the sudoku grid, I'll leave that up
    to the developer using this function.

    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the values dictionary with the naked twins values eliminated from peers.
    """
    dbg(None, i=False)

    units = _units_row + _units_colum + _unit_diagonals

    for unit in units:
        # select all the pair candidates in each unit (row, column and diagonal)
        # the array candidate will contain only pairs of possible twins
        candidates = [k for k in unit if len(values[k]) == 2]
        candidates = candidates if len(candidates) > 1 else []

        # register all the repetition ocurrences for values dict({str:set([])})
        # e.g.: {'57': {'F6', 'B2'}}, 57 is at F6 and B2 (same unit)
        register = {}
        for x in candidates:
            for y in candidates:
                if values[x] == values[y]:
                    key = values[y]
                    val = register.get(key)
                    register.update({key: (val if not val.add(y) else val) if val else set([y])})
        
        # filter out occurrences like {'17': {'I1'}, '35': {'C7'}} with one occurrence
        register = {k:register[k] for k in register if len(register[k]) == 2} # > 1 also

        # debug
        if len(register):
            dbg("\nunits     = %s, candidates = %s" % (unit, candidates), i=False)
            dbg("register  = %s" % register, i=False)

        # process all twins found
        for r in register:
            # find the block units for each register, e.g.: {'F6', 'B2'}

            # create a helper map for the square units
            # first box of the unit, maps to its unit
            squares = {s[0]:s for s in _units_square}

            # a set to validate if both twins are in the same block unit
            squareset = set()

            # get the square unit in which each register[r] belongs to
            # and register this in a set, e.g.: register = {'27': {'A7', 'B7'}}
            # TODO: improve this double for loop
            for v in register[r]:
                for s in squares:
                    if v in squares[s]:
                        squareset.add(s)

            dbg("squares   = %s" % squareset, i=False)

            # the boxes to replace the twin values
            # create new array, otherwise it will modified the actual unit
            # if we use bind/reference unit, e.g.: process = unit
            process = list(unit)
            
            # if both twins are in the same square set, include
            # the square unit (mapped) to the list of boxes
            # to cleanup the twins values
            if len(squareset) == 1:
                dbg("include   = %s" % squareset, i=False)
                process += squares[squareset.pop()]
                
            # clean up the process list, remove the register values from the list
            process = [u for u in process if u not in register[r]]

            # twin values
            # e.g.: register = {'23': {'I3', 'I1'}}, r would be 17
            twinval = [v for v in r]

            dbg("process   = %s" % process, i=False)

            # for debugging purposes
            processed = []

            for v in twinval:
                for p in process:
                    if v in values[p] and len(values[p]) > 1:
                        # don't replace values with just one digit 
                        processed.append("%s for %s" % (p,v))
                        assign_value(values, p, values[p].replace(v, ''))

            dbg("processed = %s" % processed, i=False)

        del candidates
        del register
    
    dbg(None, i=False)
    return values

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    Args:
        A(list): a list of strings
        B(list): a list of strings
    Returns:
        each value from A concatenated with each value of B
    """
    return [a+b for a in A for b in B]

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
    return { k: _columns if v == '.' else v for k,v in zip(_boxes, grid) }

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print()
    width = 1+max(len(values[s]) for s in _boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in _rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in _columns))
        if r in 'CF': print(line)
    print()
    return

def eliminate(values):
    """
    Eliminate the already filled values from its peers
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the values dictionary with the already filled value eliminated from peers.
    """
    # get all the filled values, length = 1
    filled = [k for k in values if len(values[k]) == 1]

    # remove each filled values from its peers
    for k in filled:
        for peer in _peers[k]:
            assign_value(values, peer, values[peer].replace(values[k], ''))

    return values

def only_choice(values):
    """
    Select the only choice option by iterating over the units
    and checking if a single digit, e.g.: 1, exist only in one
    bucket, if so, replace that bucket with the digit.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the grid sudoku with only choice applied to all his units
    """
    digits = _columns
    for unit in _units_all:
        for digit in digits:
            boxes = [u for u in unit if digit in values[u]]
            if len(boxes) == 1:
                # print(unit, digit, boxes, values[boxes[0]]) if len(values[u]) > 1 else None
                assign_value(values, boxes[0], digit)
    return values

def reduce_puzzle(values):
    """
    Constraing propagation by using eliminate, only choice
    and naked twins strategy
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the grid sudoku with eliminate, only choice and naked twins
        strategies applied
    """
    stalled = False
    before = None
    after = None
    while not stalled:
        before = len([k for k in values if len(values[k]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        after = len([k for k in values if len(values[k]) == 1])
        stalled = before == after
        # because of elimination, is possible to have boxes with
        # len  == 0 or no values
        if len([k for k in values if len(values[k]) == 0]):
            return False
    return values

def search(values):
    """
    Try to reduce the puzzle first, if can't
    by DFS recursively try to reduce the puzzle again
    for each possibility, e.g.: [23], wil expand a tree
    of possibles solution by setting the box to 2 and 3
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        A solved sudoku
    """

    values = reduce_puzzle(values)

    if values is False:
        return False # not solved
    if all(len(values[k]) == 1 for k in values):
        return values # solved

    v,k = min((len(values[k]), k) for k in values if len(values[k]) > 1)

    for d in values[k]:
        result = search(assign_value(values.copy(), k, d))
        if result:
            return result

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

# initialize global helper variables, the sudoku grid in a dictionary form

_rows = 'ABCDEFGHI'
_columns = '123456789'
_boxes = cross(_rows, _columns)

_units_row = [cross(r, _columns) for r in _rows]
_units_colum = [cross(_rows, c) for c in _columns]
_units_square = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

_unit_diagonal_left = [r+c for r,c in zip(_rows, _columns)]
_unit_diagonal_right = [r+c for r,c in zip(_rows, _columns[::-1])]
_unit_diagonals = [_unit_diagonal_left] + [_unit_diagonal_right]

_units_all = _units_row + _units_colum + _units_square + _unit_diagonals
_units = {k: [ u for u in _units_all if k in u] for k in _boxes}

_peers = {k: set(sum(_units[k],[])) - set([k]) for k in _boxes}

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        pass # print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
