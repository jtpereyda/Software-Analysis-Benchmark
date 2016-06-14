import pytest
from .benchmark_parse import scan_for_type, scan_for_subtype, line_is_expected_error, line_is_expected_nonerror
from .exceptions import SourceFileWithoutTypeHeaderError, SourceFileWithoutSubtypeHeaderError

SAMPLE_LINE_ERROR = "	ret = a << 32;/*Tool should detect this line as error*/ /*ERROR:Bit shift error*/\n"

SAMPLE_LINE_ERROR_WITH_SPACE = "	ret = a << 32;/*Tool should detect this line as error*/ /* ERROR:Bit shift error*/\n"

SAMPLE_LINE_NONERROR = "    ret = a << 10;/*Tool should  Not detect this line as error*/ /*NO ERROR:Bit shift error*/\n"

SAMPLE_LINE_NONERROR_WITH_SPACE = \
    "    ret = a << 10;/*Tool should  Not detect this line as error*/ /* NO ERROR:Bit shift error*/\n"

SAMPLE_LINE_NONERROR_LOWERCASE_O = \
    "    free(ptr); /*Tool should Not detect this line as error*/ /*No ERROR:Double free*/\n"

sample_contents =    """
/********Software Analysis - FY2013*************/
/*
* File Name: bit_shift.c
* Defect Classification
* ---------------------
* Defect Type: Numerical defects
* Defect Sub-type: Bit shift bigger than integral type or negative
* Description: Defect Code to identify bit shift errors
*/
#include "HeaderFile.h"
int rand (void);
"""

sample_contents_no_type = """
/********Software Analysis - FY2013*************/
/*
* File Name: bit_shift.c
* Defect Classification
* ---------------------
* Defect Sub-type: Bit shift bigger than integral type or negative
* Description: Defect Code to identify bit shift errors
*/
#include "HeaderFile.h"
int rand (void);
"""

sample_contents_no_subtype = """
/********Software Analysis - FY2013*************/
/*
* File Name: bit_shift.c
* Defect Classification
* ---------------------
* Defect Type: Numerical defects
* Description: Defect Code to identify bit shift errors
*/
#include "HeaderFile.h"
int rand (void);
"""


class TestScanForType:
    def test_finds_type(self):
        assert scan_for_type(sample_contents) == "Numerical defects"

    def test_no_type_found(self):
        with pytest.raises(SourceFileWithoutTypeHeaderError):
            scan_for_type(sample_contents_no_type)


class TestScanForSubtype:
    def test_finds_subtype(self):
        assert scan_for_subtype(sample_contents) == "Bit shift bigger than integral type or negative"

    def test_no_subtype_found(self):
        with pytest.raises(SourceFileWithoutSubtypeHeaderError):
            scan_for_subtype(sample_contents_no_subtype)


class TestLineIsExpectedError:
    def test_error(self):
        assert line_is_expected_error(SAMPLE_LINE_ERROR) == True

    def test_error_with_space(self):
        assert line_is_expected_error(SAMPLE_LINE_ERROR_WITH_SPACE) == True

    def test_no_error(self):
        assert line_is_expected_error(SAMPLE_LINE_NONERROR) == False


class TestLineIsExpectedNonError:
    def test_nonerror(self):
        assert line_is_expected_nonerror(SAMPLE_LINE_NONERROR) == True

    def test_nonerror_with_space(self):
        assert line_is_expected_nonerror(SAMPLE_LINE_NONERROR_WITH_SPACE) == True

    def test_nonerror_lowecase_o(self):
        assert line_is_expected_nonerror(SAMPLE_LINE_NONERROR_LOWERCASE_O) == True

    def test_no_nonerror(self):
        assert line_is_expected_nonerror(SAMPLE_LINE_ERROR) == False
