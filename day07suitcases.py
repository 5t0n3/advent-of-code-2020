import re
from functools import partial, reduce


def parse_inner_colors(color_list):
    """
    Creates a dictionary representing the colors of suitcases that belong within
    another.
    """
    # Strip spaces from either side of each string
    spaces_removed = map(str.strip, color_list)

    # Separate amounts from colors
    amount_pairs = list(
        map(partial(str.split, sep=" ", maxsplit=1), spaces_removed))

    # Reverse color/amount pairs so colors are keys and turn into a dict
    return dict(map(reversed, amount_pairs))


def parse_suitcase_order(line):
    """
    Parses rules for which suitcase colors go inside others.
    Returns them as a dictionary, where the keys are the inner suitcase color(s)
    and the values the corresponding outer suitcase color.
    """
    # Remove all "bags" occurrences from line
    # Also truncates period from end of line
    removed_bags = re.sub("bags?", "", line[:-1])

    # Split outer/inner colors
    outer_color, inner_colors = removed_bags.split("contain")

    # Split at commas to separate inner colors
    inner_color_list = inner_colors.split(",")

    return outer_color.strip(), parse_inner_colors(inner_color_list)


def part1_starting_colors(color_rules, color_name):
    """
    Returns a list of the possible colors to start at in order to end up with a
    shiny gold suitcase on the inside.
    """
    # Colors to achieve
    valid_starting_colors = list(
        filter(lambda colors: color_name in colors[0], color_rules))

    # Only the outer suitcase colors are necessary
    outer_colors = list(map(lambda v: v[1], valid_starting_colors))

    # Direct + indirect parents (avoid duplication using set)
    return set(outer_colors).union(
        reduce(
            lambda acc, color: acc.union(
                part1_starting_colors(color_rules, color)), outer_colors,
            set()))


def repeated_suitcases(color_rules, parent_color, color_name):
    """
    Counts the number of suitcases, accounting for repeated suitcases (i.e.
    multiple of one color inside another).
    """
    repetitions = color_rules[parent_color][color_name]

    # Empty (no cases inside)
    if repetitions == "no":
        return 0

    repetitions = int(repetitions)

    return repetitions + repetitions * part2_inner_suitcases(
        color_rules, color_name)


def part2_inner_suitcases(color_rules, color_name):
    """
    Returns the number of suitcases contained within the `color_name` suitcase.
    """
    # Find child suitcases
    child_colors = color_rules.get(color_name)

    # Handle case where no suitcases inside `color_name`
    if child_colors is None:
        return 0

    else:
        return sum(
            map(partial(repeated_suitcases, color_rules, color_name),
                child_colors))


if __name__ == "__main__":
    with open("input/day07.txt", "r") as f:
        # Remove newlines from end of every line
        raw_input = map(str.strip, f.readlines())

    parsed_input = list(map(parse_suitcase_order, raw_input))

    # Part 1 (starting colors to get to shiny gold)

    # Amounts of inner suitcases don't matter
    ignored_amounts = list(
        map(lambda colors: (list(colors[1].keys()), colors[0]), parsed_input))
    possible_starting_colors = len(
        part1_starting_colors(ignored_amounts, "shiny gold"))

    print(
        f"Part 1 result (colors that lead to shiny gold): {possible_starting_colors}"
    )
    assert possible_starting_colors == 192, f"Unexpected part 1 result: {possible_starting_colors}"

    # Part 2 (suitcases inside shiny gold)
    inner_cases = part2_inner_suitcases(dict(parsed_input), "shiny gold")

    print(f"Part 2 result (# of cases inside shiny gold): {inner_cases}")
    assert inner_cases == 12128, f"Unexpected part 2 result: {inner_cases}"
