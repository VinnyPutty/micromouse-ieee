import time
from typing import List, Tuple

import API
import sys

DEBUG_MODE = True
LOGGING_ON = True
GOAL_CONDITION = False
direction = ['n', 'e', 's', 'w']
MAZE_WIDTH = 16
MAZE_HEIGHT = 16
binary_state_representation = {
    'NNNN': 0,
    'NNNW': 1,
    'NNWN': 2,
    'NNWW': 3,
    'NWNN': 4,
    'NWNW': 5,
    'NWWN': 6,
    'NWWW': 7,
    'WNNN': 8,
    'WNNW': 9,
    'WNWN': 10,
    'WNWW': 11,
    'WWNN': 12,
    'WWNW': 13,
    'WWWN': 14,
    'XXXX': 15
}
binary_state_representation_lookup = {
    0: 'NNNN',
    1: 'NNNW',
    2: 'NNWN',
    3: 'NNWW',
    4: 'NWNN',
    5: 'NWNW',
    6: 'NWWN',
    7: 'NWWW',
    8: 'WNNN',
    9: 'WNNW',
    10: 'WNWN',
    11: 'WNWW',
    12: 'WWNN',
    13: 'WWNW',
    14: 'WWWN',
    15: 'XXXX'
}


def log(string):
    if LOGGING_ON:
        sys.stderr.write("{}\n".format(string))
        sys.stderr.flush()


def update_direction(direction_marker=0, turn='left') -> int:
    if turn == 'left':
        direction_marker = direction_marker - 1 if (direction_marker - 1) >= 0 else 3
    elif turn == 'right':
        direction_marker = (direction_marker + 1) % 4
    return direction_marker


def update_position(current_position, direction_marker) -> (int, int):
    if not direction_marker:
        return current_position[0], current_position[1] + 1
    elif direction_marker == 1:
        return current_position[0] + 1, current_position[1]
    elif direction_marker == 2:
        return current_position[0], current_position[1] - 1
    elif direction_marker == 3:
        return current_position[0] - 1, current_position[1]


# FIXME handling of zero wall cells (use example maze 1 for testing)
# FIXME handling of endless loop of explores due to:
#   - an explore that returns to the starting cell of that explore
#   - any other reason for and endless loop of explores
# TODO implement "return to start" when below conditions are met:
#   - every cell representation is known
#   - every cell representation but the goal cells is known
#   - unvisited list is empty
#   - unvisited list only contains goal cells
# TODO implement "target largest unvisited regions"
# TODO implement "target exploration of particular cell"
#   - this might require a known path to a cell adjacent to that particular cell
# a depth-first exploration of the maze
def explore(current_position, direction_marker, maze_state=None, unvisited_list: list = None, explore_depth=0):
    explore_depth += 1
    log('Explore depth: {}'.format(explore_depth))
    log('Current direction: {}, Focus Cell Representation: {}'.format(direction[direction_marker], ignore_wall(
        wall_direction_marker=direction_marker, cell=maze_state[convert_position_to_map_position(current_position)[0]][
            convert_position_to_map_position(current_position)[1]], opposite_wall=True)))
    # while unvisited_list or (15 not in maze_state):
    current_cell = update_cell_representation(current_position, direction_marker, maze_state)[-1]
    # if maze_state: print_maze_state(maze_state)
    branch_list: List[Tuple[Tuple[int, int], int]] = \
        [(current_position, branch_direction) for branch_direction in
         [no_wall for no_wall, ch in enumerate(ignore_wall(wall_direction_marker=direction_marker,
                                                           cell=current_cell, opposite_wall=True)) if ch == 'N'] if
         maze_state[convert_position_to_map_position(update_position(current_position, branch_direction))[0]]
         [convert_position_to_map_position(update_position(current_position, branch_direction))[1]] == 15]
    return_path_list: List[List[Tuple[int, int]]] = []
    return_path: List[Tuple[int, int]] = []

    log('Branch List: {}'.format(branch_list))
    for starting_position, starting_direction in branch_list:
        if current_position != starting_position:
            log('Current position/starting position mismatch: Curr is {}; Start is {}'.format(current_position,
                                                                                              starting_position))
        return_path.append(current_position)
        direction_marker = turn_to_direction(starting_direction, direction_marker)
        current_position = update_position(current_position, direction_marker)
        API.moveForward()
        current_cell = update_cell_representation(current_position, direction_marker, maze_state)[-1]
        # log(current_cell)
        focus_current_cell = ignore_wall(wall_direction_marker=direction_marker, cell=current_cell, opposite_wall=True)
        while focus_current_cell.count('N') == 1:
            return_path.append(current_position)
            direction_marker = turn_to_direction(focus_current_cell.index('N'), direction_marker)
            current_position = update_position(current_position, direction_marker)
            API.moveForward()
            current_cell = update_cell_representation(current_position, direction_marker, maze_state)[-1]
            # log(current_cell)
            focus_current_cell = ignore_wall(wall_direction_marker=direction_marker, cell=current_cell,
                                             opposite_wall=True)
        log('Current position: {}, Direction: {}, Maze State: \n'.format(current_position, direction[direction_marker]))
        # print_maze_state(maze_state)
        current_position, direction_marker, *_ = explore(current_position, direction_marker, maze_state, unvisited_list, explore_depth)

        return_path.append(current_position)
        return_path.reverse()
        current_position, direction_marker = constructed_path_follow(return_path, direction_marker)

    return current_position, direction_marker, maze_state


def explore_():
    pass


def ignore_wall(wall_direction=None, wall_direction_marker=None, cell=None, cell_representation=None,
                opposite_wall: bool = False):
    if cell:
        cell_representation = binary_state_representation_lookup[cell]
        # if not cell_representation:
        log('Cell: {}'.format(cell))
        log('Cell representation: {}'.format(cell_representation))
    if wall_direction:
        wall_direction_marker = direction.index(wall_direction)
    if opposite_wall:
        wall_direction_marker = (wall_direction_marker + 2) % 4

    focus_current_cell = cell_representation[:wall_direction_marker] + 'I' + cell_representation[
                                                                             wall_direction_marker + 1:]

    return focus_current_cell


def turn_to_direction(target_direction_marker=None, direction_marker=None, target_direction=None,
                      current_direction=None):
    if target_direction and current_direction:
        target_direction_marker, direction_marker = direction.index(target_direction), \
                                                    direction.index(current_direction)

    while direction_marker != target_direction_marker:
        direction_marker = update_direction(direction_marker, turn='left')
        API.turnLeft()

    return direction_marker


def constructed_path_follow(path: List[Tuple], direction_marker, maze_state=None) -> Tuple[Tuple[int, int], int]:
    # Perform the necessary MMS commands to follow the path specified by the list of coordinates in param `path`
    log('Following constructed path: {}'.format(path))
    current_position = path.pop(0)
    while len(path) > 0:
        if maze_state:
            update_cell_representation(current_position, direction_marker, maze_state)
            # print_maze_state(maze_state)
        log('Current position: {}, Current direction: {}'.format(current_position, direction[direction_marker]))
        next_position = path.pop(0)

        direction_to_move = next_position[0] - current_position[0], next_position[1] - current_position[1]
        target_direction_marker = 0
        if direction_to_move[0] == 1:
            target_direction_marker = 1  # east
        elif direction_to_move[0] == -1:
            target_direction_marker = 3  # west
        elif direction_to_move[1] == 1:
            target_direction_marker = 0  # north
        elif direction_to_move[1] == -1:
            target_direction_marker = 2  # south
        log('Next position: {}, Target direction: {}'.format(next_position, direction[target_direction_marker]))

        direction_marker = turn_to_direction(target_direction_marker, direction_marker)

        temp_position = update_position(current_position, direction_marker)
        try:
            if temp_position != next_position:
                raise UserWarning
        except UserWarning:
            log('Incorrect planned movement. Expected next position: {}; '
                'Actual next position: {}'.format(next_position, current_position))
            return temp_position, direction_marker
        else:
            current_position = temp_position
            API.moveForward()

    if maze_state:
        update_cell_representation(current_position, direction_marker, maze_state)
        print_maze_state(maze_state)

    return current_position, direction_marker


def update_cell_representation(current_position, direction_marker, maze_state):
    API.setColor(*current_position, 'B')
    map_position = convert_position_to_map_position(current_position)
    if binary_state_representation_lookup[maze_state[map_position[0]][map_position[1]]] == 'XXXX':
        API.setColor(*current_position, "B")
        current_cell = 'NNNN'
        if API.wallFront():
            API.setWall(*current_position, direction[direction_marker])
            current_cell = add_wall(current_cell, direction_marker)
        if API.wallLeft():
            API.setWall(*current_position, direction[update_direction(direction_marker, turn='left')])
            current_cell = add_wall(current_cell, update_direction(direction_marker, turn='left'))
        if API.wallRight():
            API.setWall(*current_position, direction[update_direction(direction_marker, turn='right')])
            current_cell = add_wall(current_cell, update_direction(direction_marker, turn='right'))

        maze_state[map_position[0]][map_position[1]] = binary_state_representation[current_cell]

    return maze_state, maze_state[map_position[0]][map_position[1]]


def add_wall(cell, direction_marker):
    cell = cell[:direction_marker] + 'W' + cell[direction_marker + 1:]  # TODO: inefficient
    return cell


def print_maze_state(maze_state):
    [print(x) for x in maze_state]
    [log(x) for x in maze_state]


def convert_position_to_map_position(current_position):
    return MAZE_HEIGHT - 1 - current_position[1], current_position[0]


def main():
    if GOAL_CONDITION:
        goal = [(7, 7), (7, 8), (8, 7), (8, 8)]
    else:
        goal = []
    unvisited_list = []
    maze_state = [[15 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    # print_maze_state(maze_state)
    # exit(0)
    for i in range(16):
        for j in range(16):
            unvisited_list.append((i, j))
    # unvisited_list = unvisited_list[1:]
    for position in goal:
        API.setColor(*position, "G")
        API.setText(*position, 'END')
    direction_marker = 0
    current_position = (0, 0)
    log("Running...")
    # API.setColor(0, 0, "G")
    # API.setText(0, 0, "abc")
    # while current_position not in goal:
    #     (current_position, direction_marker, maze_state) = move(current_position, direction_marker, maze_state,
    #                                                             unvisited_list=unvisited_list)
    #     print_maze_state(maze_state)
    test_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (6, 5),
                 (6, 6), (6, 7), (7, 7), (8, 7), (8, 8), (8, 9), (9, 9), (9, 10), (10, 10), (11, 10), (11, 11), ]
    example_maze_5_solution_path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7),
                                    (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (5, 4),
                                    (6, 4), (6, 3), (7, 3), (7, 4), (7, 5), (6, 5), (6, 6), (6, 7), (5, 7), (5, 6),
                                    (5, 5), (4, 5), (4, 6), (4, 7), (3, 7), (3, 8), (2, 8), (1, 8), (0, 8), (0, 9),
                                    (0, 10), (1, 10), (1, 9), (2, 9), (2, 10), (3, 10), (4, 10), (5, 10), (5, 11),
                                    (4, 11), (3, 11), (2, 11), (1, 11), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
                                    (1, 15), (2, 15), (2, 14), (2, 13), (2, 12), (3, 12), (4, 12), (4, 13), (5, 13),
                                    (5, 12), (6, 12), (6, 13), (7, 13), (7, 12), (7, 11), (6, 11), (6, 10), (6, 9),
                                    (7, 9), (7, 10), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (9, 15),
                                    (10, 15), (11, 15), (12, 15), (12, 14), (12, 13), (12, 12), (12, 11), (11, 11),
                                    (10, 11), (10, 12), (9, 12), (9, 11), (9, 10), (9, 9), (8, 9), (8, 8), ]
    # constructed_path_follow(example_maze_5_solution_path, direction_marker, maze_state)
    explore(current_position, direction_marker, maze_state)


if __name__ == "__main__":
    main()
