import pickle
import sys
import time
from typing import Tuple, List

import API

LOGGING_ON = True
MAZE_HEIGHT = 16
MAZE_WIDTH = 16
direction = ['n', 'e', 's', 'w']
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


def find_all_routes(maze_state, *, starting_position=None, starting_map_position=None, ending_position=None,
                    ending_map_position=None):
    log('Finding all routes...')
    default_starting_position = 0, 0
    default_ending_positions = [(7, 7), (7, 8), (8, 7), (8, 8)]
    if starting_position:
        starting_map_position = convert_position_to_map_position(starting_position)
    elif not starting_map_position:
        starting_map_position = convert_position_to_map_position(default_starting_position)
    if ending_position:
        ending_map_position = convert_position_to_map_position(ending_position)
    elif not ending_map_position:
        default_ending_map_positions = [convert_position_to_map_position(position) for position in
                                        default_ending_positions]
        ending_map_position = [map_position for map_position in default_ending_map_positions if
                               binary_state_representation_lookup[maze_state[map_position[0]][map_position[1]]
                                                                  ].count('W') == 1][0]
    valid_map_routes = []
    find_all_routes_(maze_state, current_map_position=starting_map_position, target_map_position=ending_map_position,
                     valid_routes=valid_map_routes)
    valid_routes = []
    for route in valid_map_routes:
        for i in range(len(route)):
            route[i] = convert_map_position_to_position(route[i])
        valid_routes.append(route)

    return valid_routes


def find_all_routes_(maze_state, current_map_position, target_map_position, valid_routes, current_route=[]):
    if len(valid_routes) > 100000: return
    if current_map_position[0] < 0 or current_map_position[0] > MAZE_HEIGHT - 1 or current_map_position[1] < 0 or \
            current_map_position[1] > MAZE_WIDTH - 1:
        return
    if current_map_position == target_map_position:
        current_route.append(current_map_position)
        valid_routes.append(current_route)
        return
    cell_representation = binary_state_representation_lookup[
        maze_state[current_map_position[0]][current_map_position[1]]]
    if cell_representation.count('N') == 1 and \
            update_map_position(current_map_position, cell_representation.index('N')) == current_route[-1]:
        return

    current_route.append(current_map_position)
    potential_next_cells = [update_map_position(current_map_position, i) for i, ch in
                            enumerate(cell_representation) if ch == 'N']
    next_cells = [cell for cell in potential_next_cells if cell not in current_route]
    if not len(next_cells):
        return
    # API.setColor(convert_map_position_to_position(current_map_position)[0],
    #              convert_map_position_to_position(current_map_position)[1], 'R')
    # time.sleep(.1)
    for cell in next_cells:
        find_all_routes_(maze_state, cell, target_map_position, valid_routes, current_route.copy())


def update_map_position(current_map_position, direction_marker) -> (int, int):
    if not direction_marker:
        return current_map_position[0] - 1, current_map_position[1]
    elif direction_marker == 1:
        return current_map_position[0], current_map_position[1] + 1
    elif direction_marker == 2:
        return current_map_position[0] + 1, current_map_position[1]
    elif direction_marker == 3:
        return current_map_position[0], current_map_position[1] - 1


def convert_position_to_map_position(current_position, maze_height=None):
    return (maze_height if maze_height else MAZE_HEIGHT) - 1 - current_position[1], current_position[0]


def convert_map_position_to_position(current_map_position, maze_height=None):
    return current_map_position[1], (maze_height if maze_height else MAZE_HEIGHT) - 1 - current_map_position[0]


def print_maze_state(maze_state):
    [print(x) for x in maze_state]
    [log(x) for x in maze_state]


if __name__ == '__main__':
    # print('Module not meant to be used as main.')
    example_maze_2 = [[13, 9, 10, 10, 10, 10, 10, 8, 10, 10, 12, 9, 8, 10, 8, 12],
                   [5, 5, 9, 12, 9, 8, 12, 3, 8, 12, 5, 5, 3, 12, 5, 5],
                   [5, 5, 5, 3, 6, 5, 1, 12, 5, 5, 5, 3, 12, 5, 5, 7],
                   [5, 5, 1, 12, 9, 6, 5, 3, 6, 5, 1, 10, 2, 6, 3, 12],
                   [1, 2, 6, 5, 3, 12, 3, 10, 12, 3, 2, 10, 10, 10, 10, 4],
                   [3, 10, 12, 3, 10, 2, 8, 12, 3, 10, 10, 12, 11, 10, 12, 5],
                   [9, 10, 6, 9, 10, 8, 6, 3, 10, 8, 12, 5, 9, 10, 6, 5],
                   [5, 9, 12, 1, 12, 3, 12, 9, 8, 6, 5, 5, 1, 10, 10, 6],
                   [5, 5, 3, 6, 5, 9, 6, 3, 6, 9, 6, 5, 3, 10, 8, 12],
                   [5, 5, 9, 12, 5, 5, 9, 10, 12, 3, 12, 5, 9, 10, 6, 5],
                   [5, 1, 6, 1, 6, 3, 6, 9, 2, 12, 1, 4, 1, 10, 10, 6],
                   [1, 6, 9, 6, 9, 10, 10, 2, 12, 3, 6, 5, 3, 10, 8, 12],
                   [1, 10, 6, 9, 6, 9, 10, 12, 3, 10, 12, 3, 10, 10, 6, 5],
                   [5, 9, 12, 5, 9, 6, 13, 5, 9, 12, 5, 9, 10, 10, 12, 5],
                   [3, 4, 3, 6, 5, 9, 2, 2, 6, 7, 5, 5, 9, 14, 5, 5],
                   [9, 2, 10, 10, 2, 2, 10, 10, 10, 10, 2, 6, 3, 10, 2, 6]]
    all_valid_routes = find_all_routes(example_maze_2)
    # print(len(all_valid_routes), all_valid_routes)
    log('Number of routes found: {}'.format(len(all_valid_routes)))
    # log(all_valid_routes)
    # route_lengths = ', '.join([str(len(valid_route)) for valid_route in all_valid_routes])
    # log(route_lengths)
    # longest_route = max(all_valid_routes, key=len)
    # log('Longest route length: {}'.format(len(longest_route)))
    shortest_route = min(all_valid_routes, key=len)
    log('Shortest route length: {}'.format(len(shortest_route)))
    for maze_cell in shortest_route:
        API.setColor(maze_cell[0], maze_cell[1], 'G')
        time.sleep(.2)

    pass
