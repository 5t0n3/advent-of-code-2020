import copy
from functools import partial


def surrounding_seats(arrangement, row, col):
    """
    Returns a list of the states of the seats surrounding that in `arrangement`
    at row `row` and column `col`.
    """

    # Top row
    if row == 0:
        # Top right corner
        if col == len(arrangement[0]) - 1:
            return [
                arrangement[row][col - 1],
                *arrangement[row + 1][col - 1:col + 1]
            ]

        # Top left corner
        elif col == 0:
            return [
                arrangement[row][col + 1], *arrangement[row + 1][col:col + 2]
            ]

        # Neither corner
        else:
            return [
                arrangement[row][col - 1], arrangement[row][col + 1],
                *arrangement[row + 1][col - 1:col + 2]
            ]

    # Bottom row
    elif row == len(arrangement) - 1:
        # Bottom right corner
        if col == len(arrangement[0]) - 1:
            return [
                *arrangement[row - 1][col - 1:col + 1],
                arrangement[row][col - 1]
            ]

        # Bottom left corner
        elif col == 0:
            return [
                *arrangement[row - 1][col:col + 2], arrangement[row][col + 1]
            ]

        # Neither corner
        else:
            return [
                *arrangement[row - 1][col - 1:col + 2],
                arrangement[row][col - 1], arrangement[row][col + 1]
            ]

    # Don't need to check for corners on left/right, as they're already checked above

    # Left edge
    elif col == 0:
        return [
            *arrangement[row - 1][col:col + 2], arrangement[row][col + 1],
            *arrangement[row + 1][col:col + 2]
        ]

    # Right edge
    elif col == len(arrangement[0]) - 1:
        return [
            *arrangement[row - 1][col - 1:col + 1], arrangement[row][col - 1],
            *arrangement[row + 1][col - 1:col + 1]
        ]

    # Anywhere in the middle
    else:
        return [
            *arrangement[row - 1][col - 1:col + 2], arrangement[row][col - 1],
            arrangement[row][col + 1], *arrangement[row + 1][col - 1:col + 2]
        ]


def step_seat_arrangement_part1(arrangement):
    """
    Steps the seat arrangement by the given rules. Returns a new arrangement
    without modifying the old one.
    """
    new_arrangement = copy.deepcopy(arrangement)

    for row_num, row in enumerate(arrangement):
        for col_num, seat in enumerate(row):
            neighbors = surrounding_seats(arrangement, row_num, col_num)

            # Seat is empty and no occupied neighbors, become occupied
            if seat == "L" and neighbors.count("#") == 0:
                new_arrangement[row_num][col_num] = "#"

            # Seat is occupied and >=4 occupied neighbors, become empty
            elif seat == "#" and neighbors.count("#") >= 4:
                new_arrangement[row_num][col_num] = "L"

    return new_arrangement


if __name__ == "__main__":
    with open("input/day11.txt", "r") as f:
        raw_input = [[c for c in row] for row in f.read().strip().split("\n")]

    # Part 1 (occupied seats while stabilized)
    new_arrangement = None
    previous_state = raw_input
    stable = False

    while not stable:
        new_arrangement = step_seat_arrangement_part1(previous_state)
        stable = previous_state == new_arrangement
        previous_state = new_arrangement

    stable_occupied_seats = sum(
        map(partial(lambda row: row.count("#")), new_arrangement))

    print(f"Part 1 result (occupied seats after stabilizing): {stable_occupied_seats}")
    assert stable_occupied_seats == 2113, f"Unexpected part 1 result: {stable_occupied_seats}"