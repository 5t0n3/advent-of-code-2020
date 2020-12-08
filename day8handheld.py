from copy import deepcopy
from functools import partial


def execute_handheld_code(instructions, visited, cursor, acc):
    """
    Executes the supplied instructions, returning the final value of `acc`.

    If the instructions terminated normally (i.e. reached the end of the input),
    `True` will be returned along with the value of `acc`; otherwise, `False` will
    be returned
    """
    # Check if at end of instructions
    if cursor == len(instructions):
        return acc, True

    # Check if current instruction has been executed before
    if cursor in visited:
        return acc, False
    else:
        visited.add(cursor)

    # Get current instruction
    op, value = instructions[cursor]

    # Increment accumulator
    if op == "acc":
        return execute_handheld_code(instructions, visited, cursor + 1,
                                     acc + int(value))
    # Jump to instruction based on offset
    elif op == "jmp":
        return execute_handheld_code(instructions, visited,
                                     cursor + int(value), acc)

    # Noop
    elif op == "nop":
        return execute_handheld_code(instructions, visited, cursor + 1, acc)


def swap_instruction(instruction_list, idx):
    """
    Swaps a `jmp` instruction with a `nop` or vice versa.
    """
    instructions_copy = deepcopy(instruction_list)

    current_instruction, _ = instructions_copy[idx]

    if current_instruction == "jmp":
        instructions_copy[idx][0] = "nop"
    elif current_instruction == "nop":
        instructions_copy[idx][0] = "jmp"

    return instructions_copy


if __name__ == "__main__":
    with open("input/day8.txt", "r") as f:
        raw_input = f.read().split("\n")

    instruction_pairs = list(map(lambda line: line.split(" "), raw_input))

    # Part 1 (accumulator before repeating)
    acc_before_repeat, _ = execute_handheld_code(instruction_pairs, set(), 0,
                                                 0)

    print(f"Part 1 result (accumulator before repeating): {acc_before_repeat}")
    assert acc_before_repeat == 1816, f"Unexpected part 1 result: {acc_before_repeat}"

    # Part 2 (accumulator after exiting normally)

    # Replacing `nop` with `jmp`
    nop_lines = filter(lambda line: line[0] == "nop", instruction_pairs)
    nop_indices = map(instruction_pairs.index, nop_lines)
    nop_swap_results = map(
        lambda updated: execute_handheld_code(updated, set(), 0, 0),
        map(partial(swap_instruction, instruction_pairs), nop_indices))
    possible_result = list(filter(lambda res: res[1], nop_swap_results))

    # Replacing `jmp` with `nop`, if necessary
    if not possible_result:
        jmp_lines = filter(lambda line: line[0] == "jmp", instruction_pairs)
        jmp_indices = map(instruction_pairs.index, jmp_lines)
        jmp_swap_results = map(
            lambda updated: execute_handheld_code(updated, set(), 0, 0),
            map(partial(swap_instruction, instruction_pairs), jmp_indices))
        possible_result = list(filter(lambda res: res[1], jmp_swap_results))

    final_acc, _ = possible_result[0]
    print(f"Part 2 result (accumulator after normal exit): {final_acc}")
    assert final_acc == 1149, f"Unexpected part 2 result: {final_acc}"