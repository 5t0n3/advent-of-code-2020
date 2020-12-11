import copy
from functools import partial

# Clockwise from upright
SEAT_OFFSETS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1),
                (-1, -1)]


def seat_within_arrangement(arrangement, row, col):
    """
    Returns True if the seat is within `arrangement`.
    """
    return 0 <= row <= len(arrangement) - 1 and 0 <= col <= len(
        arrangement[0]) - 1


def seat_at_offset(arrangement, row, col, offset, max_distance=None):
    """
    Returns the first seat (empty/occupied) at the given offset relative to that
    at row `row` and column `col` within `arrangement`, at most `max_distance`
    away. Otherwise returns a floor tile (".").
    """

    # Start at first seat away
    distance = 1
    row_offset, col_offset = offset
    current_row, current_col = row + row_offset, col + col_offset

    while seat_within_arrangement(arrangement, current_row, current_col):
        # Stop if far enough away
        if max_distance is not None and distance > max_distance:
            break
        seat = arrangement[current_row][current_col]

        # Return seat if occupied/empty
        if seat in "#L":
            return seat

        current_row += row_offset
        current_col += col_offset
        distance += 1

    # Default case (floor tile)
    return "."


def step_seat_arrangement(arrangement, part):
    """
    Steps the seat arrangement by the given rules. Returns a new arrangement
    without modifying the old one.
    """
    # max_distance should be 1 in part 1 and ignored in part 1
    # occupied seat tolerance is also higher in part 2
    if part == 1:
        max_distance = 1
        occupied_tolerance = 4
    else:
        max_distance = None
        occupied_tolerance = 5

    new_arrangement = copy.deepcopy(arrangement)

    for row_num, row in enumerate(arrangement):
        for col_num, seat in enumerate(row):
            neighbors = list(
                map(
                    partial(seat_at_offset,
                            arrangement,
                            row_num,
                            col_num,
                            max_distance=max_distance), SEAT_OFFSETS))

            # Seat is empty and no occupied neighbors, become occupied
            if seat == "L" and neighbors.count("#") == 0:
                new_arrangement[row_num][col_num] = "#"

            # Seat is occupied and >=4 occupied neighbors, become empty
            elif seat == "#" and neighbors.count("#") >= occupied_tolerance:
                new_arrangement[row_num][col_num] = "L"

    return new_arrangement


def count_stable_occupied_seats(arrangement, part):
    """
    Returns the number of occupied seats after the arrangement stabilizes.
    """
    new_arrangement = None
    previous_state = arrangement
    stable = False

    while not stable:
        new_arrangement = step_seat_arrangement(previous_state, part=part)
        stable = previous_state == new_arrangement
        previous_state = new_arrangement

    return sum(map(partial(lambda row: row.count("#")), new_arrangement))


if __name__ == "__main__":
    with open("input/day11.txt", "r") as f:
        raw_input = [[c for c in row] for row in f.read().strip().split("\n")]

    # Part 1 (occupied seats while stabilized)
    stable_occupied_seats_part1 = count_stable_occupied_seats(raw_input,
                                                              part=1)
    print(
        f"Part 1 result (occupied seats after stabilizing): {stable_occupied_seats_part1}"
    )
    assert stable_occupied_seats_part1 == 2113, f"Unexpected part 1 result: {stable_occupied_seats_part1}"

    # Part 2 (seats at any distance away; # occupied after stabilizing)
    stable_occupied_seats_part2 = count_stable_occupied_seats(raw_input,
                                                              part=2)

    print(
        f"Part 2 result (extended vision; stable occupied seats): {stable_occupied_seats_part2}"
    )
    assert stable_occupied_seats_part2 == 1865, f"Unexpected part 2 result: {stable_occupied_seats_part2}"
