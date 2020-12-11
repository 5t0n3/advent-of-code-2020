from functools import reduce


def update_range(old_range, update_char):
    """
    Narrows the supplied range using `update_char` ("F", "B", "R", or "L").
    """
    begin, end = old_range
    split_point = (begin + end) // 2

    if update_char == "F" or update_char == "L":
        return (begin, split_point)
    if update_char == "B" or update_char == "R":
        return (split_point + 1, end)


def find_seat_id(boarding_pass):
    """
    Finds the ID of a given boarding pass' seat given the pass itself.
    """
    # Find row and column
    row_num = reduce(update_range, boarding_pass[0:7], (0, 127))[0]
    col_num = reduce(update_range, boarding_pass[7:], (0, 7))[0]

    return row_num * 8 + col_num


if __name__ == "__main__":
    with open("input/day05.txt", "r") as f:
        boarding_passes = map(str.strip, f.readlines())

    # Part 1 (greatest seat ID)
    # Note that seat_ids is converted to a list, as otherwise the map iterator
    # is consumed by the `max` function
    seat_ids = list(map(find_seat_id, boarding_passes))
    max_seat_id = max(seat_ids)

    print(f"Part 1 result (max seat ID): {max_seat_id}")
    assert max_seat_id == 953, f"Unexpected part 1 result: {max_seat_id}"

    # Part 2 (my/missing seat ID)
    # Since the IDs around my seat are supposed to exist (but not the seat
    # itself), I can filter that way
    prev_seat_id = list(
        filter(lambda id: id + 1 not in seat_ids and id + 2 in seat_ids,
               seat_ids))[0]
    my_seat_id = prev_seat_id + 1

    print(f"Part 2 result (my seat ID): {my_seat_id}")
    assert my_seat_id == 615, f"Unexpected part 2 result: {my_seat_id}"
