from os import path

map_path = 'treasure-map.layout'

def loadLayout(layout_path):
    """ Load treasure hunt layout map

    Args:
        layout_path (string): layout file path

    Raises:
        FileNotFoundError: file not found

    Returns:
        array: treasure hunt layout in array of string
    """
    layout = []

    if path.exists(layout_path):
        with open(layout_path, 'r') as f:
            layout = [ line.rstrip() for line in f ]
    else:
        raise FileNotFoundError('Please run script in project root folder')

    return layout

def calculateLocation(layout):
    """ Calculate the posibility location treasure

    Args:
        layout (array): treasure hunt layout in array of string

    Returns:
        array: treasure location in array of tuple (x, y)
    """
    if len(layout) == 0:
        # layout is empty list
        print('Treasure Map layout is empty')
        return []

    # get player position
    position = None
    for i, row in enumerate(layout):
        if 'X' in row:
            position = (row.index('X'), i)
            break

    if position is None:
        # player not found
        print('No player position detected')
        return []

    # search treasure
    location = []
    x, y = position
    # start with go to north
    moveNorth(layout, (x, y - 1), location)

    return location

def baseRule(layout, position):
    """ Return current path is posible or dead end

    Args:
        layout (array): treasure hunt layout in array of string
        position (tuple): player location

    Returns:
        boolean: posible path
    """
    x, y = position
    if x < 0 or x >= len(layout[y]) or y < 0 or y >= len(layout):
        # index out of bound
        return True

    if layout[y][x] == '#':
        # obsacle
        return True

    return False

def moveNorth(layout, position, location):
    """ First order move north

    Args:
        layout (array): treasure hunt layout in array of string
        position (tuple): player location
        location (array): treasure location in array of tuple (x, y)
    """
    if position in location:
        # player was moving here
        return

    if baseRule(layout, position):
        return

    x, y = position
    if layout[y][x] == '.':
        # go further to north
        moveNorth(layout, (x, y - 1), location)
        # go to east
        moveEast(layout, (x + 1, y), location)

def moveEast(layout, position, location):
    """ Second order move east

    Args:
        layout (array): treasure hunt layout in array of string
        position (tuple): player location
        location (array): treasure location in array of tuple (x, y)
    """
    if position in location:
        # player was moving here
        return

    if baseRule(layout, position):
        return

    x, y = position
    if layout[y][x] == '.':
        # go further to east
        moveEast(layout, (x + 1, y), location)
        # go to south
        moveSouth(layout, (x, y + 1), location)

def moveSouth(layout, position, location):
    """ Last order move south

    Args:
        layout (array): treasure hunt layout in array of string
        position (tuple): player location
        location (array): treasure location in array of tuple (x, y)
    """
    if position in location:
        # player was moving here
        return

    if baseRule(layout, position):
        return

    x, y = position
    if layout[y][x] == '.':
        # got treasure
        location.append((x, y))
        # go further to south
        moveSouth(layout, (x, y + 1), location)

def run():
    """ Display gthe grid with all probable treasure locations
    """
    # load treasure map layout
    layout = loadLayout(map_path)

    # count location posibility
    locations = calculateLocation(layout)

    for x, y in locations:
        temp = list(layout[y])
        temp[x] = '$'
        layout[y] = ''.join(temp)
    [ print(row) for row in layout ]
    print('Total posibility =', len(locations))
