import pickle

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


def find_all_routes(maze_state, starting_position=None, starting_map_position=None, ending_position=None, ending_map_position=None):
    default_starting_position = 0, 0
    default_ending_positions = [(7, 7), (7, 8), (8, 7), (8, 8)]
    if starting_position:
        starting_map_position = convert_position_to_map_position(starting_position)
    elif not starting_map_position:
        starting_map_position = convert_position_to_map_position((0, 0))
    if ending_position:
        ending_map_position = convert_position_to_map_position(ending_position)
    elif not ending_map_position:
        default_ending_map_positions = [convert_position_to_map_position(position) for position in
                                        default_ending_positions]
        ending_map_position = [map_position for map_position in default_ending_map_positions if
                               maze_state[map_position[0]][map_position[1]].count('W') == 1][0]
    # TODO: implement depth-first search to find all routes between `starting_position` and `ending_position`


def find_all_routes_():
    pass


def convert_position_to_map_position(current_position, maze_height=None):
    return (maze_height if maze_height else MAZE_HEIGHT) - 1 - current_position[1], current_position[0]