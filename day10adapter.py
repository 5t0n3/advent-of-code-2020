from itertools import combinations
from functools import partial, reduce
import operator
import math


def has_nearby_items(lst, margin, upper_bound, item):
    """
    Returns True if there is at least one item in `lst` within +/- `margin` of
    `item`.
    """
    poss_items_above = list(filter(lambda v: item < v <= item + margin, lst))
    poss_items_below = list(filter(lambda v: item - margin <= v < item, lst))
    return (item == 1 or bool(len(poss_items_below))) and (
        item == upper_bound or bool(len(poss_items_above)))


def valid_charger_permutations(joltages):
    """
    Calculates the number of valid permutations of the chargers given their
    joltages.
    """

    # Algorithm idea: store possible next values for each rating and find combos
    # that way
    valid_permutations = 0

    # Theoretical shortest length -> make a 3-jolt jump every time
    theoretical_shortest_combo_length = math.ceil(len(joltages) / 3)

    for combo_len in range(theoretical_shortest_combo_length,
                           len(joltages) + 1):
        combos = combinations(joltages, combo_len)
        valid_combos = list(
            filter(
                lambda combo: all(
                    map(partial(has_nearby_items, combo, 3, max(joltages)),
                        combo)), combos))

        device_reaching_combos = list(
            filter(
                lambda combo: max(joltages) in combo and any(
                    map(lambda v: v in range(1, 4), combo)), valid_combos))
        valid_permutations += len(device_reaching_combos)

    return valid_permutations


def flatten_list(lst):
    """
    Splices all sublists of `lst` into a single list.
    """
    return reduce(operator.add, lst, [])


def generate_successors(joltages):
    """
    Returns a dictionary with the possible successors to each rating within 3
    jolts.
    """
    successors = {}

    for rating in joltages:
        possible_successors = list(
            filter(lambda j: 1 <= j - rating <= 3, joltages))
        successors[rating] = possible_successors

    # Add 0 case (outlet)
    successors[0] = list(range(1, 4))

    return successors


def alternative_charger_combos(joltages):
    """
    Calculates the number of valid combinations of chargers meeting specific
    criteria given their joltage ratings.
    """
    valid_combos = 0
    successors = generate_successors(joltages)
    final_rating = max(joltages)

    # Seed with first value
    current_combos = [[0]]

    while len(current_combos) > 0:
        tmp_combos = flatten_list(
            [[combo + [j] for j in successors[combo[-1]]]
             for combo in current_combos])

        terminated_combos = list(
            filter(lambda combo: final_rating in combo, tmp_combos))
        in_progress_combos = list(
            filter(lambda combo: final_rating not in combo, tmp_combos))

        valid_combos += len(terminated_combos)
        current_combos = in_progress_combos

    return valid_combos


if __name__ == "__main__":
    with open("input/day10.txt", "r") as f:
        raw_input = map(int, f.read().strip().split("\n"))

    sorted_joltages = list(sorted(raw_input))

    # Part 1 (1-jolt * 3-jolt differences)
    previous_joltage = 0  # Relative to outlet
    one_jolt_differences = 0
    three_jolt_differences = 1  # Include last adapter to device

    for rating in sorted_joltages:
        joltage_difference = rating - previous_joltage

        one_jolt_differences += joltage_difference == 1
        three_jolt_differences += joltage_difference == 3

        previous_joltage = rating

    part1_result = one_jolt_differences * three_jolt_differences
    print(f"Part 1 result (1-jolt * 3-jolt differences): {part1_result}")
    assert part1_result == 2400, f"Unexpected part 1 result: {part1_result}"

    # Part 2 (# of valid charger permutations)
    print(alternative_charger_combos(sorted_joltages))
