from functools import reduce


# Part 1 functions
def parse_policy_part1(password_combo):
    """
    Parses a password/policy combo from a single line of input.
    """
    # Split at spaces (separate password/policy)
    split_combo = password_combo.split()

    # Parse policy range into actual range
    range_bounds = split_combo[0].split("-")
    char_range = range(int(range_bounds[0]), int(range_bounds[1]) + 1)

    # Return range, character, and password itself
    return char_range, split_combo[1][0], split_combo[2]


def parse_policies_part1(filepath):
    """
    Parses passwords and their corresponding policies from a given file given by
    `filepath`.
    """
    with open(filepath, "r") as f:
        file_lines = map(str.strip, f.readlines())

    # Split policy/password, then parse policy
    fully_parsed_policies = map(parse_policy_part1, file_lines)
    return fully_parsed_policies


def password_meets_policy_part1(combo):
    """
    Returns True if the given password satisfies its corresponding policy.
    """
    # combo[2] -> password, combo[1] -> character, combo[0] -> range
    return combo[2].count(combo[1]) in combo[0]


# Part 2 functions
def parse_policy_part2(password_combo):
    """
    Parses a password/policy combo from a single line of input.
    """
    # Split at spaces (separate password/policy)
    split_combo = password_combo.split()

    first_idx, second_idx = split_combo[0].split("-")

    # Return range, character, and password itself
    # Note that the indexes are 1-based rather than 0-based
    return (int(first_idx) - 1,
            int(second_idx) - 1), split_combo[1][0], split_combo[2]


def parse_policies_part2(filepath):
    """
    Parses password policies in the way described in part 2.
    """
    with open(filepath, "r") as f:
        file_lines = map(str.strip, f.readlines())

    # Split policies/passwords & parse policy
    fully_parsed_policies = map(parse_policy_part2, file_lines)
    return fully_parsed_policies


def password_meets_policy_part2(combo):
    """
    Returns True if the given password satisfies its corresponding policy, in
    line with part 2.
    """
    first_idx, second_idx = combo[0]

    # combo[2] -> password
    return (combo[2][first_idx] == combo[1]) != (combo[2][second_idx]
                                                 == combo[1])


# General functions
def verify_passwords(parsed_policies, predicate):
    """
    Verifies if passwords match their corresponding policies. Returns the number
    of passwords that meet this requirement.

    Note: `predicate` should return a boolean.
    """
    return reduce(lambda acc, c: acc + int(predicate(c)), parsed_policies, 0)


if __name__ == "__main__":
    # Passwords that meet their policies (part 1)
    part1_count = verify_passwords(parse_policies_part1("input/day02.txt"),
                                   password_meets_policy_part1)
    print(f"Part 1 count: {part1_count}")

    assert part1_count == 640, f"Unexpected part 1 result: {part1_count}"

    # Passwords that meet their policies (part 2)
    part2_count = verify_passwords(parse_policies_part2("input/day02.txt"),
                                   password_meets_policy_part2)
    print(f"Part 2 count: {part2_count}")

    assert part2_count == 472, f"Unexpected part 2 result: {part2_count}"
