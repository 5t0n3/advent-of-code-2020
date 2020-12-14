from math import ceil
from functools import reduce
import operator

if __name__ == "__main__":
    with open("input/day13.txt", "r") as f:
        raw_input = f.read().strip().split("\n")

    earliest_estimate = int(raw_input[0])
    bus_lines = list(raw_input[1].split(","))

    # Part 1 (earliest actual departure)
    known_bus_lines = list(map(int, filter(lambda l: l != "x", bus_lines)))

    # Get next timestamp for each line and find wait time from it
    wait_times = map(
        lambda l: (ceil(earliest_estimate / l) * l - earliest_estimate, l),
        known_bus_lines)

    # Find the shortest wait time
    shortest_pair = min(wait_times, key=lambda l: l[0])
    part1_result = reduce(operator.mul, shortest_pair)

    print(f"Part 1 result (shortest wait time to departure): {part1_result}")
    assert part1_result == 2947, f"Unexpected part 1 result: {part1_result}"
