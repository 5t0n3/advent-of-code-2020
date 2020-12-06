from functools import reduce


def group_answer_sets(raw_group):
    """
    Returns a list of sets of the questions every person in `raw_group` answered
    yes to.
    """
    individual_answers = map(set, raw_group.split())

    # Set intersection of all rows (individual answer sets)
    return reduce(set.intersection, individual_answers)


if __name__ == "__main__":
    with open("input/day6.txt", "r") as f:
        # Split on empty line (2 newlines)
        raw_input = f.read().split("\n\n")

    # Part 1 (sum of "yes" answers)

    # Remove newlines and convert strings to sets
    question_sets = map(
        lambda questions: set(filter(lambda c: not c.isspace(), questions)),
        raw_input)
    yes_answers = reduce(lambda acc, qset: acc + len(qset), question_sets, 0)

    print(f"Part 1 result (sum of yes answers): {yes_answers}")
    assert yes_answers == 7120, f"Unexpected part 1 answer: {yes_answers}"

    # Part 2 (sum of group-wide "yes" answers)

    # Remove blank lines (only "\n")
    common_group_answers = map(group_answer_sets, raw_input)
    common_yes_answers = reduce(lambda acc, qset: acc + len(qset),
                                common_group_answers, 0)

    print(
        f"Part 2 result (sum of group-wide yes answers: {common_yes_answers}")
    assert common_yes_answers == 3570, f"Unexpected part 2 answer: {common_yes_answers}"
