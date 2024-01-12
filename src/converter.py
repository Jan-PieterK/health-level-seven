import re


def is_valid_csv_format(submitted_text):
    pattern_semi_colon = r"^[A-Za-z0-9]{3};\d+(\.\d+){0,2};[^;]*$"
    pattern_comma = r"^[A-Za-z0-9]{3},\d+(\.\d+){0,2},[^,]*$"

    submitted_text = submitted_text.split("\n")
    submitted_text = list(filter(None, submitted_text))
    for line in submitted_text:
        if not re.match(pattern_comma, line) and not re.match(
            pattern_semi_colon, line
        ):
            return False
    return True
