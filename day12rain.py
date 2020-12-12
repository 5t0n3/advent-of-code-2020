from functools import reduce

CLOCKWISE_DIRECTIONS = ["N", "E", "S", "W"]


def navigate_no_waypoint(current_info, instruction):
    """
    Executes `instruction` on `current_info`, which contains information about
    vertical/horizontal position and heading.
    """
    # Unpack position info/instruction
    (horizontal, vertical), heading = current_info
    action, argument = instruction[0], instruction[1:]
    heading_idx = CLOCKWISE_DIRECTIONS.index(heading)

    # Move forward along heading
    if action == "F":
        action = heading

    # North
    if action == "N":
        return (horizontal, vertical + int(argument)), heading

    # South
    elif action == "S":
        return (horizontal, vertical - int(argument)), heading

    # East
    elif action == "E":
        return (horizontal + int(argument), vertical), heading

    # West
    elif action == "W":
        return (horizontal - int(argument), vertical), heading

    # Turn left (counterclockwise)
    elif action == "L":
        return (horizontal, vertical
                ), CLOCKWISE_DIRECTIONS[(heading_idx - int(argument) // 90) %
                                        len(CLOCKWISE_DIRECTIONS)]

    # Turn right (clockwise)
    elif action == "R":
        return (horizontal, vertical
                ), CLOCKWISE_DIRECTIONS[(heading_idx + int(argument) // 90) %
                                        len(CLOCKWISE_DIRECTIONS)]


def rotate_waypoint(x, y, angle):
    """
    Rotates the waypoint relative to the ship, where positive angles are counterclockwise.
    """

    # Check cardinal angles
    if angle == 90:
        return (-y, x)

    elif angle == 180:
        return (-x, -y)

    elif angle == 270:
        return (y, -x)

    else:
        raise ValueError(f"Invalid angle: {angle}")


def navigate_with_waypoint(current_info, instruction):
    """
    Executes `instruction` on `current_info`, which contains information about
    vertical/horizontal position of the waypoint/ship.
    """
    # Unpack position info/instruction
    ship_pos, (way_x, way_y) = current_info
    action, argument = instruction[0], instruction[1:]

    # North
    if action == "N":
        return ship_pos, (way_x, way_y + int(argument))

    # South
    elif action == "S":
        return ship_pos, (way_x, way_y - int(argument))

    # East
    elif action == "E":
        return ship_pos, (way_x + int(argument), way_y)

    # West
    elif action == "W":
        return ship_pos, (way_x - int(argument), way_y)

    # Turn left (counterclockwise)
    elif action == "L":
        new_waypoint_coords = rotate_waypoint(way_x, way_y, int(argument))
        return ship_pos, new_waypoint_coords

    # Turn right (clockwise)
    elif action == "R":
        # Correct angle (since clockwise means negative angles)
        new_waypoint_coords = rotate_waypoint(way_x, way_y,
                                              360 - int(argument))
        return ship_pos, new_waypoint_coords

    # Move towards waypoint
    elif action == "F":
        ship_x, ship_y = ship_pos
        times = int(argument)

        return (ship_x + way_x * times, ship_y + way_y * times), (way_x, way_y)


if __name__ == "__main__":
    with open("input/day12.txt", "r") as f:
        raw_input = f.read().strip().split("\n")

    # Part 1 (execute navigation instructions as given initially)
    part1_pos_info = reduce(navigate_no_waypoint, raw_input, ((0, 0), "E"))
    part1_manhattan_distance = sum(map(abs, part1_pos_info[0]))
    print(
        f"Part 1 solution (initial requirements): {part1_manhattan_distance}")
    assert part1_manhattan_distance == 1631, f"Unexpected part 1 solution: {part1_manhattan_distance}"

    # Part 2 (revised navigation requirements)
    part2_pos_info = reduce(navigate_with_waypoint, raw_input,
                            ((0, 0), (10, 1)))
    part2_manhattan_distance = sum(map(abs, part2_pos_info[0]))
    print(
        f"Part 2 solution (revised requirements): {part2_manhattan_distance}")
    assert part2_manhattan_distance == 58606, f"Unexpected part 2 solution: {part2_manhattan_distance}"
