class Benchmark:
    """Describes errors and nonerrors for a benchmark"""
    def __init__(self, errors, nonerrors):
        self._errors = errors
        self._nonerrors = nonerrors

    @property
    def errors(self):
        """Expected errors

        Returns:
            Data structure of expected errors.
        """
        return self._errors

    @property
    def nonerrors(self):
        """Expected non-errors.

        Used to identify false positives.

        Returns:
            Data structure of expected non-errors.
        """
        return self._nonerrors
