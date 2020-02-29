import time

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


def move(current_position, direction_marker, maze_state, unvisited_list: list = None):
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

    if unvisited_list and len(unvisited_list) > 0:
        if not API.wallFront() and update_position(current_position, direction_marker) in unvisited_list:
            API.moveForward()
            log('Moving forward UL.')
        elif not API.wallLeft() and update_position(current_position,
                                                    update_direction(direction_marker, turn='left')) in unvisited_list:
            direction_marker = update_direction(direction_marker, turn='left')
            API.turnLeft()
            log('Turning left UL.')
            API.moveForward()
            log('Moving forward UL.')
        elif not API.wallRight() and update_position(current_position,
                                                     update_direction(direction_marker,
                                                                      turn='right')) in unvisited_list:
            direction_marker = update_direction(direction_marker, turn='right')
            API.turnRight()
            log('Turning right UL.')
            API.moveForward()
            log('Moving forward UL.')
        else:
            direction_marker = left_wall_follow(direction_marker)
    else:
        direction_marker = left_wall_follow(direction_marker)
    current_position = update_position(current_position, direction_marker)
    if unvisited_list and current_position in unvisited_list:
        unvisited_list.remove(current_position)
    return current_position, direction_marker, maze_state


def left_wall_follow(direction_marker):
    if not API.wallLeft():
        API.turnLeft()
        log('Turning left.')
        direction_marker = update_direction(direction_marker, turn='left')
    while API.wallFront():
        API.turnRight()
        log('Turning right.')
        direction_marker = update_direction(direction_marker, turn='right')
    API.moveForward()
    log('Moving forward.')
    return direction_marker


def add_wall(cell, direction_marker):
    cell = cell[:direction_marker] + 'W' + cell[direction_marker + 1:]  # TODO: inefficient
    return cell


def print_maze_state(maze_state):
    [print(x) for x in maze_state]


def convert_position_to_map_position(current_position):
    return MAZE_HEIGHT - 1 - current_position[1], current_position[0]


def main():
    if GOAL_CONDITION:
        goal = [(7, 7), (7, 8), (8, 7), (8, 8)]
    else:
        goal = []
    unvisited_list = []
    maze_state = [[15 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    print_maze_state(maze_state)
    # exit(0)
    for i in range(16):
        for j in range(16):
            unvisited_list.append((i, j))
    unvisited_list = unvisited_list[1:]
    for position in goal:
        API.setColor(*position, "G")
        API.setText(*position, 'END')
    direction_marker = 0
    current_position = (0, 0)
    log("Running...")
    # API.setColor(0, 0, "G")
    # API.setText(0, 0, "abc")
    while current_position not in goal:
        (current_position, direction_marker, maze_state) = move(current_position, direction_marker, maze_state,
                                                                unvisited_list=unvisited_list)
        print_maze_state(maze_state)


if __name__ == "__main__":
    main()
