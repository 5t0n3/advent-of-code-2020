def charger_combos(joltages):
    """
    Calculates the number of valid charger combinations.
    """
    pair_paths = {}  # Number of paths between a pair of ratings
    device_rating = joltages[-1]  # Already includes device rating; sorted

    # Paths are built starting at the end, so iterate backwards
    for rating in reversed(joltages):
        # Get possible child ratings (greater joltages)
        direct_children = list(filter(lambda j: 1 <= j - rating <= 3,
                                      joltages))

        for child in direct_children:
            # Find children between current/child ratings, if applicable, as
            # they increase the number of paths between ratings
            intermediary_children = list(
                filter(lambda c: c in range(rating, child), direct_children))

            # Include direct path (1) as well as stopping at any intermediary ratings
            pair_paths[(rating, child)] = 1 + len(intermediary_children)

        # Check if number of paths to end has already been calculated
        end_paths = pair_paths.get((rating, device_rating))

        # Calculate the number of paths from all children to the end
        child_total_paths = sum(
            map(lambda c: pair_paths[(c, device_rating)], direct_children))

        # Increment it if it already exists
        if end_paths is not None:
            pair_paths[(rating, device_rating)] += child_total_paths

        # Otherwise set it
        else:
            pair_paths[(rating, device_rating)] = child_total_paths

    # Number of paths from outlet (0 jolts) to end
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

    # Count joltage jumps when using all adapters
    for rating in sorted_joltages:
        joltage_difference = rating - previous_joltage

        one_jolt_differences += joltage_difference == 1
        three_jolt_differences += joltage_difference == 3

        previous_joltage = rating

    part1_result = one_jolt_differences * three_jolt_differences
    print(f"Part 1 result (1-jolt * 3-jolt differences): {part1_result}")
    assert part1_result == 2400, f"Unexpected part 1 result: {part1_result}"

    # Part 2 (# of valid charger permutations)
    part2_result = charger_combos(sorted_joltages)

    print(f"Part 2 result (charger combinations): {part2_result}")
    assert part2_result == 338510590509056, f"Unexpected part 2 result: {part2_result}"
