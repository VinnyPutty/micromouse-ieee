import API
import sys

LOGGING_ON = False
GOAL_CONDITION = True

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


def move(current_position, direction, direction_marker, unvisited_list: list = None):
    API.setColor(*current_position, "B")
    if API.wallFront():
        API.setWall(*current_position, direction[direction_marker])
    if API.wallLeft():
        API.setWall(*current_position, direction[update_direction(direction_marker, turn='left')])
    if API.wallRight():
        API.setWall(*current_position, direction[update_direction(direction_marker, turn='right')])

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
    return current_position, direction_marker


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


def main():
    if GOAL_CONDITION:
        goal = [(7, 7), (7, 8), (8, 7), (8, 8)]
    else:
        goal = []
    unvisited_list = []
    for i in range(16):
        for j in range(16):
            unvisited_list.append((i, j))
    unvisited_list = unvisited_list[1:]
    for position in goal:
        API.setColor(*position, "G")
        API.setText(*position, 'END')
    direction = ['n', 'e', 's', 'w']
    direction_marker = 0
    current_position = (0, 0)
    log("Running...")
    # API.setColor(0, 0, "G")
    # API.setText(0, 0, "abc")
    while current_position not in goal:
        (current_position, direction_marker) = move(current_position, direction, direction_marker,
                                                    unvisited_list=unvisited_list)


if __name__ == "__main__":
    main()
