class Benchmark:
    """Describes errors and nonerrors for a benchmark"""
    def __init__(self, errors=None, nonerrors=None):
        if errors is None:
            errors = []
        if nonerrors is None:
            nonerrors = []

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

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Benchmark(errors=self.errors + other.errors,
                             nonerrors=self.nonerrors + other.nonerrors)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))
