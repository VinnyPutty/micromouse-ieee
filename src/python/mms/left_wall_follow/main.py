import API
import sys


LOGGING_ON = False


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


def update_position(direction_marker, current_position) -> (int, int):
    if not direction_marker:
        return current_position[0], current_position[1] + 1
    elif direction_marker == 1:
        return current_position[0] + 1, current_position[1]
    elif direction_marker == 2:
        return current_position[0], current_position[1] - 1
    elif direction_marker == 3:
        return current_position[0] - 1, current_position[1]


def main():
    goal = [(7, 7), (7, 8), (8, 7), (8, 8)]
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
        API.setColor(*current_position, "B")
        if API.wallFront():
            API.setWall(*current_position, direction[direction_marker])
        if API.wallLeft():
            API.setWall(*current_position, direction[update_direction(direction_marker, turn='left')])
        if API.wallRight():
            API.setWall(*current_position, direction[update_direction(direction_marker, turn='right')])
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
        current_position = update_position(direction_marker, current_position)



if __name__ == "__main__":
    main()
