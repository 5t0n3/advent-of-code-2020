def two_entry_2020_sum(entries):
    """
    Returns the pair of numbers in `entries` that sum to 2020.
    """
    # Take the first, as the list will have 2 tuples (one the reverse of the other)
    return [(e1, 2020 - e1) for e1 in entries if (2020 - e1) in entries][0]

def three_entry_2020_sum(entries):
    """
    Returns triplet of entries that sum to 2020.
    """
    # Iterate over all possible values of e1
    for e1 in entries:
        # e2 has to be less than what it would be in the 2-entry case (complement
        # relative to 2020)
        possible_triplets = [(e1, e2, 2020 - e1 - e2) for e2 in entries if (2020 - e1 - e2) in entries]

        # Return triplet if solution exists
        if possible_triplets:
            # All entries in list are duplicates
            return possible_triplets[0]

if __name__ == "__main__":
    with open("input/day1.txt", "r") as f:
        raw_input = f.readlines()

    # Strip newlines & convert to numbers
    entry_input = list(map(lambda s: int(s.rstrip()), raw_input))

    # Part 1 (product of 2 entries that sum to 2020)
    entry1, entry2 = two_entry_2020_sum(entry_input)
    result_part1 = entry1 * entry2
    print("Part 1 product (2 entries):", result_part1)

    # Verify part 1 solution
    assert result_part1 == 974304, f"Unexpected part 2 result: {result_part1}"

    entry1, entry2, entry3 = three_entry_2020_sum(entry_input)
    result_part2 = entry1 * entry2 * entry3
    print("Part 2 product (3 entries):", result_part2)

    # Verify part 2 solution
    assert result_part2 == 236430480, f"Unexpected part 2 result: {result_part2}"