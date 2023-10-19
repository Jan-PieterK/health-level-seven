import re


def is_valid_csv_format(submitted_text):
    pattern = r'^(?!.*;.*;.*;)[A-Za-z]{3};\d+(\.\d+){0,2};[^;]*$'

    submitted_text = submitted_text.split('\n')
    print(submitted_text)
    for line in submitted_text:
        print(line)
        if not re.match(pattern, line):
            return False
    return True
