from functools import reduce

def count_trees(col_change, row_change, input_map):
    """
    Counts trees encountered on route to bottom by moving `row_change` rows down
    and `col_change` columns right on every iteration.
    """
    # Map dimensions
    total_rows = len(input_map)
    total_cols = len(input_map[0])

    # Count/position variables
    current_row = 0
    current_col = 0
    tree_total = 0

    # Iterate until bottom is reached
    while current_row < total_rows:
        # Check if current position is a tree (i.e. "#")
        # if so, increment tree_total
        tree_total += int(input_map[current_row][current_col] == "#")

        # Move 3 spaces right, one space down
        current_row += row_change
        current_col += col_change

        # Wrap column around if necessary
        current_col %= total_cols

    return tree_total


if __name__ == "__main__":
    with open("input/day3.txt", "r") as f:
        input_map = list(map(str.strip, f.readlines()))

    # Part 1 (3 over, 1 down tree total)
    part1_result = count_trees(3, 1, input_map)
    print(f"Part 1 result: {part1_result}")
    assert part1_result == 148, f"Unexpected part 1 result: {part1_result}"

    # Part 2 (multiple different increment amounts)
    step_amounts = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    part2_result = reduce(lambda acc, step: acc * count_trees(*step, input_map), step_amounts, 1)
    print(f"Part 2 result: {part2_result}")
    assert part2_result == 727923200, f"Unexpected part 2 result: {part2_result}"