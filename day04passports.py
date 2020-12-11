from functools import reduce, partial
from os import kill
import re


def parse_passport(split_fields):
    """
    Parses a passport after its fields have been split.
    Returns a map representing the passport.
    """
    field_pairs = map(lambda field: field.split(":"), split_fields)
    return dict(field_pairs)


def pass_valid_part1(req_fields, pass_map):
    """
    Returns True if the supplied passport map has all fields.
    Treats the `cid` field as optional.
    """
    return reduce(lambda acc, field: field in pass_map and acc, req_fields,
                  True)


def fields_valid(predicate_dict, pass_map):
    """
    Validates a password based on the supplied predicate-field map.
    """
    pass_valid = True

    for field in predicate_dict:
        if pass_map.get(field) is None:
            return False

        pass_valid = predicate_dict[field](pass_map[field]) and pass_valid

    return pass_valid


def height_predicate(height):
    """
    Verifies if height is valid based on units.
    """
    # Return false if height is too short (<=2 chars long)
    if len(height) <= 2:
        return False

    # Inches
    if height[-2:] == "in":
        return 59 <= int(height[:-2]) <= 76

    # Centimeters
    else:
        return 150 <= int(height[:-2]) <= 193


if __name__ == "__main__":
    with open("input/day04.txt", "r") as f:
        raw_input = f.read()

    # Split on blank lines (2 newlines)
    passport_list = raw_input.split("\n\n")

    # Split on whitespace to separate fields and parse passports into maps
    parsed_passports = map(lambda raw_pass: parse_passport(raw_pass.split()),
                           passport_list)

    # All fields
    all_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]

    # For part 1, ignore "cid" field
    part1_fields = all_fields[:-1]
    part1_valid_passports = list(
        filter(partial(pass_valid_part1, part1_fields), parsed_passports))

    print(f"Valid passports in part 1: {len(part1_valid_passports)}")
    assert len(
        part1_valid_passports
    ) == 230, f"Unexpected part 1 result: {len(part1_valid_passports)}"

    # Part 2 has value requirements for the fields
    part2_fields_preds = dict(
        zip(
            part1_fields,
            [
                lambda byr: 1920 <= int(byr) <= 2002,
                lambda iyr: 2010 <= int(iyr) <= 2020,
                lambda eyr: 2020 <= int(eyr) <= 2030,
                height_predicate,
                partial(re.match, r"#[a-f0-9]{6}"),  # hcl/hair color
                lambda ecl: ecl in
                ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
                partial(re.match, r"^\d{9}$")
            ]))  # pid/passport id

    # Filter based on part 1 passwords (missing fields are invalid in both parts)
    part2_valid_passports = list(
        filter(partial(fields_valid, part2_fields_preds),
               part1_valid_passports))

    print(f"Valid passports in part 2: {len(part2_valid_passports)}")
    assert len(
        part2_valid_passports
    ) == 156, f"Unexpected part 2 result: {len(part2_valid_passports)}"
