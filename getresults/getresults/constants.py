import re

DEFECT_TYPE_REGEX = re.compile(r"\*\ Defect\ Type:\s*(.*)", flags=re.VERBOSE)
DEFECT_SUBTYPE_REGEX = re.compile(r"\*\ Defect\ Sub-type:\s*(.*)", flags=re.VERBOSE)
ERROR_MARKER_REGEX = re.compile(r"/\*\s*ERROR:.*\*/", flags=re.IGNORECASE)
NONERROR_MARKER_REGEX = re.compile(r"/\*\s*NO\sERROR:.*\*/", flags=re.IGNORECASE)
