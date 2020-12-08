def execute_stopping_at_dupe(instructions, visited, cursor, acc):
    """
    Executes instructions, stopping when the current instruction has been
    executed previously.

    Returns the value in the accumulator at this time.
    """
    # Check if current instruction has been executed before
    if cursor in visited:
        return acc
    else:
        visited.add(cursor)

    # Get current instruction
    op, value = instructions[cursor]

    # Increment accumulator
    if op == "acc":
        return execute_stopping_at_dupe(instructions, visited, cursor + 1,
                                        acc + int(value))
    # Jump to instruction based on offset
    elif op == "jmp":
        return execute_stopping_at_dupe(instructions, visited,
                                        cursor + int(value), acc)

    # Noop
    elif op == "nop":
        return execute_stopping_at_dupe(instructions, visited, cursor + 1, acc)


if __name__ == "__main__":
    with open("input/day8.txt", "r") as f:
        raw_input = f.read().split("\n")

    instruction_pairs = list(map(lambda line: line.split(" "), raw_input))
    acc_before_repeat = execute_stopping_at_dupe(instruction_pairs, set(), 0,
                                                 0)

    print(f"Part 1 result (accumulator before repeating): {acc_before_repeat}")
    assert acc_before_repeat == 1816, f"Unexpected part 1 result: {acc_before_repeat}"