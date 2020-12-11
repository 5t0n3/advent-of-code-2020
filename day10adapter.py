def charger_combos(joltages):
    """
    Calculates the number of valid charger combinations more efficiently?
    """
    pair_paths = {}
    device_rating = joltages[-1]  # Already includes device rating; sorted

    for rating in reversed(joltages):
        # Get possible ratings after current
        direct_children = list(filter(lambda j: 1 <= j - rating <= 3,
                                      joltages))

        # Update direct (and some indirect) paths
        for child in direct_children:
            intermediary_children = list(
                filter(lambda c: c in range(rating, child), direct_children))

            pair_paths[(rating, child)] = 1 + len(intermediary_children)

        end_paths = pair_paths.get((rating, device_rating))
        child_total_paths = sum(
            map(lambda c: pair_paths[(c, device_rating)], direct_children))

        if end_paths is None:
            pair_paths[(rating, device_rating)] = child_total_paths

        else:
            pair_paths[(rating, device_rating)] += child_total_paths

    return pair_paths[(0, device_rating)]


if __name__ == "__main__":
    with open("input/day10.txt", "r") as f:
        raw_input = map(int, f.read().strip().split("\n"))

    sorted_joltages = [0] + list(sorted(raw_input))

    # Add device joltage
    sorted_joltages.append(sorted_joltages[-1] + 3)

    # Part 1 (1-jolt * 3-jolt differences)
    previous_joltage = sorted_joltages[0]  # Outlet
    one_jolt_differences = 0
    three_jolt_differences = 0

    for rating in sorted_joltages:
        joltage_difference = rating - previous_joltage

        one_jolt_differences += joltage_difference == 1
        three_jolt_differences += joltage_difference == 3

        previous_joltage = rating

    part1_result = one_jolt_differences * three_jolt_differences
    print(f"Part 1 result (1-jolt * 3-jolt differences): {part1_result}")
    assert part1_result == 2400, f"Unexpected part 1 result: {part1_result}"

    # Part 2 (# of valid charger permutations)
    # print(alternative_charger_combos(sorted_joltages))

    part2_result = charger_combos(sorted_joltages)
    print(f"Part 2 result (charger combinations): {part2_result}")
    assert part2_result == 338510590509056, f"Unexpected part 2 result: {part2_result}"
