from itertools import combinations


def group_consecutives(num_consecutives, group_list):
    """
    Groups `num_consecutives` items in group list, incrementing the start index
    by 1 each time.
    """
    cursor = num_consecutives
    acc_list = []

    while cursor < len(group_list):
        acc_list.append(group_list[cursor - num_consecutives:cursor])
        cursor += 1

    return acc_list


if __name__ == "__main__":
    with open("input/day9.txt", "r") as f:
        raw_input = list(map(int, f.read().strip().split("\n")))

    # Part 1 (first number not sum of 2 from previous 25)
    pointer = 25
    first_invalid = None

    while pointer < len(raw_input):
        prev_25 = raw_input[pointer - 25:pointer]
        valid_sums = set(map(sum, combinations(prev_25, 2)))

        test_num = int(raw_input[pointer])

        if test_num not in valid_sums:
            first_invalid = test_num
            break

        pointer += 1

    print(f"Part 1 result (first not sum of previous 25): {first_invalid}")
    assert first_invalid == 85848519, f"Unexpected part 1 result: {first_invalid}"

    # Part 2 (contiguous set of numbers that sum to part 2 result)

    # Start with 2 addends and work up from there
    num_addends = 2
    sum_set = None

    while sum_set is None:
        consecutive_sets = group_consecutives(num_addends, raw_input)
        consecutive_sums = list(
            filter(lambda num_set: sum(num_set) == first_invalid,
                   consecutive_sets))

        if len(consecutive_sums) > 0:
            sum_set = consecutive_sums[0]
        else:
            num_addends += 1

    enc_weakness = min(sum_set) + max(sum_set)
    print(f"Part 2 result (encryption weakness): {enc_weakness}")
    assert enc_weakness == 13414198, f"Unexpected part 2 result: {enc_weakness}"
