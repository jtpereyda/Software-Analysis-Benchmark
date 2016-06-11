import re
import pprint

DEFECT_TYPE_REGEX = re.compile(r"\*\ Defect\ Type:\s*(.*)", flags=re.VERBOSE)
DEFECT_SUBTYPE_REGEX = re.compile(r"\*\ Defect\ Sub-type:\s*(.*)", flags=re.VERBOSE)
ERROR_MARKER_REGEX = re.compile(r"/\*\s*ERROR:.*\*/")


class SourceFileWithoutTypeHeaderError(Exception):
    pass


class SourceFileWithoutSubtypeHeaderError(Exception):
    pass


def main(argv):
    pprint.pprint(expected_errors())
    # compare(expected_errors, found_errors)


def expected_errors():
    return find_expected_errors_in_file('01.w_Defects/bit_shift.c')


def find_expected_errors_in_file(filename):
    expected = scan_for_expected_errors(get_file_contents(filename))
    for e in expected:
        e['file'] = filename
    return expected


def scan_for_expected_errors(file_contents):
    expected = get_expected_errors_from_file(file_contents)
    type = scan_for_type(file_contents)
    subtype = scan_for_subtype(file_contents)
    for e in expected:
        e['type'] = type
        e['subtype'] = subtype
    return expected


def get_expected_errors_from_file(file_contents):
    lines = file_contents.splitlines()
    expected = []
    for line_number, line in enumerate(lines, start=1):
        if line_is_expected_error(line):
            expected.append({'line': line_number})
    return expected


def scan_for_type(file_contents):
    m = DEFECT_TYPE_REGEX.search(file_contents)
    if m:
        return m.group(1)
    else:
        raise SourceFileWithoutTypeHeaderError


def scan_for_subtype(file_contents):
    m = DEFECT_SUBTYPE_REGEX.search(file_contents)
    if m:
        return m.group(1)
    else:
        raise SourceFileWithoutSubtypeHeaderError


def line_is_expected_error(line_contents):
    if ERROR_MARKER_REGEX.search(line_contents):
        return True
    else:
        return False


def get_file_contents(filename):
    with open(filename) as f:
        return f.read()


def compare(expected_errors, found_errors):
    pass


if __name__ == "__main__":
    main()
