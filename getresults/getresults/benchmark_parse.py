import fnmatch
import itertools
import os

from .utils import get_file_contents
from .benchmark import Benchmark
from .constants import DEFECT_TYPE_REGEX, DEFECT_SUBTYPE_REGEX, ERROR_MARKER_REGEX, NONERROR_MARKER_REGEX
from .error_handling import warn
from .exceptions import SourceFileWithoutTypeHeaderError, SourceFileWithoutSubtypeHeaderError


def parse_benchmarks(filename):
    """
    Parse a file or directory for expected benchmark errors and non-errors.

    Args:
        filename: File or directory to search. Directories are recursively searched.

    Returns:
        Benchmark: Expected results from benchmark file(s).
    """
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
    results = Benchmark()
    for root, dirnames, filenames in os.walk(dirname):
        for filename in itertools.chain(fnmatch.filter(filenames, '*.c'), fnmatch.filter(filenames, '*.cpp')):
            results += find_expected_errors_in_file(os.path.join(root, filename))
    return results


def find_expected_errors_in_file(filename):
    errors = []
    nonerrors = []
    try:
        errors, nonerrors = scan_for_expected_errors(get_file_contents(filename))
        for item in itertools.chain(errors, nonerrors):
            item['file'] = filename
    except (SourceFileWithoutSubtypeHeaderError, SourceFileWithoutTypeHeaderError):
        warn("Ignoring improperly formatted file {0}".format(filename))
    return Benchmark(errors, nonerrors)


def scan_for_expected_errors(file_contents):
    errors, nonerrors = get_expected_errors_and_nonerrors_from_file(file_contents)
    defect_type = scan_for_type(file_contents)
    defect_subtype = scan_for_subtype(file_contents)
    for item in itertools.chain(errors, nonerrors):
        item['type'] = defect_type
        item['subtype'] = defect_subtype
    return errors, nonerrors


def get_expected_errors_and_nonerrors_from_file(file_contents):
    lines = file_contents.splitlines()
    errors = []
    nonerrors = []
    for line_number, line in enumerate(lines, start=1):
        if line_is_expected_error(line):
            errors.append({'line': line_number})
        if line_is_expected_nonerror(line):
            nonerrors.append({'line': line_number})
    return errors, nonerrors


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


def line_is_expected_nonerror(line_contents):
    if NONERROR_MARKER_REGEX.search(line_contents):
        return True
    else:
        return False
