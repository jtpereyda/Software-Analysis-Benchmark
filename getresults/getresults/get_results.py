import argparse
import fnmatch
import os
import re
import itertools

DEFECT_TYPE_REGEX = re.compile(r"\*\ Defect\ Type:\s*(.*)", flags=re.VERBOSE)
DEFECT_SUBTYPE_REGEX = re.compile(r"\*\ Defect\ Sub-type:\s*(.*)", flags=re.VERBOSE)
ERROR_MARKER_REGEX = re.compile(r"/\*\s*ERROR:.*\*/")


class SourceFileWithoutTypeHeaderError(Exception):
    pass


class SourceFileWithoutSubtypeHeaderError(Exception):
    pass


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("testbench_dir", help="file or directory to search for expected errors")
    arguments = parser.parse_args(args=argv[1:])

    e = expected_errors(arguments.testbench_dir)
    defect_types = set()
    for error in e:
        defect_types.add(error["type"])
    for defect_type in defect_types:
        print("{0} -- {1}".format(defect_type, sum(error["type"] == defect_type for error in e)))
    print(len(e))


def expected_errors(filename):
    return parse_file_or_directory(filename)


def parse_file_or_directory(filename):
    """
    Parse expected errors from filename.

    Args:
        filename: File or directory to parse.

    Returns: Data structure with expected errors.
    """
    if os.path.isdir(filename):
        return parse_directory(filename)
    else:
        return find_expected_errors_in_file(filename)


def parse_directory(dirname):
    """
    Parse expected errors from files within dirname.

    Recursive by default.

    Args:
        dirname: Directory to search.

    Returns: Data structure with expected errors.
    """
    results = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in itertools.chain(fnmatch.filter(filenames, '*.c'), fnmatch.filter(filenames, '*.cpp')):
            results += find_expected_errors_in_file(os.path.join(root, filename))
    return results


def find_expected_errors_in_file(filename):
    expected = []
    try:
        expected = scan_for_expected_errors(get_file_contents(filename))
        for e in expected:
            e['file'] = filename
    except (SourceFileWithoutSubtypeHeaderError, SourceFileWithoutTypeHeaderError):
        warn("Ignoring improperly formatted file {0}".format(filename))
    return expected


def warn(message):
    """
    Present warning to user.

    Args:
        message: Warning message

    Returns: None
    """
    print(message)


def scan_for_expected_errors(file_contents):
    expected = get_expected_errors_from_file(file_contents)
    defect_type = scan_for_type(file_contents)
    defect_subtype = scan_for_subtype(file_contents)
    for e in expected:
        e['type'] = defect_type
        e['subtype'] = defect_subtype
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
    with open(filename, encoding='utf-8', errors='ignore') as f:
        return f.read()
