from typing import Any


class AverageAccumulator:
    """An aggregator class to maintain an average."""

    def __init__(self):
        self.sum = 0.0
        self.n = 0

    def value(self) -> float:
        """Returns the average based on currently obtained data. If there is no data, returns 0.

        Returns:
            float: the average
        """
        if self.n == 0:
            return 0

        return self.sum / self.n

    def accumulate(self, o: Any) -> None:
        """Aggregates another accumulator or a floating point.
        """
        if isinstance(o, AverageAccumulator):
            self.sum += o.sum
            self.n += o.n
        else:
            self.sum += o
            self.n += 1

    def reset(self):
        """Reset the class"""
        self.sum = 0.0
        self.n = 0


class Histogram:
    """ A class used for storing histogrammic data."""

    def __init__(self):
        self.hist = {}

    def witness(self, val, count=1):
        """See the value and count it in the histogram."""
        if val in self.hist:
            self.hist[val] = self.hist[val] + count
        else:
            self.hist[val] = count

    def top_n(self, n):
        """Returns the top 'n' items (or top(len(histogram)) if len(histogram) < n), sorted by count."""
        if len(self.hist) < n:
            n = len(self.hist)

        values = list(map(lambda x: x[0], sorted(self.hist.items(), key=lambda item: item[1], reverse=True)))
        return values[0:n]

    def merge(self, hist):
        """Merge statistics from another histogram into this histogram."""
        for val, count in hist.hist.items():
            self.witness(val, count)

    def __str__(self):
        return str(self.hist)

    # TODO. This is fine for the prototype but ideally we want to do something
    # more intelligent using the histogramatic data we have.  We currently take
    # the smallest and the largest witnessed tokens as the
    # lower and upper bounds, but perhaps we want to exclude outliers better.
    def range(self):
        """Returns an upper and lower bound for the token lengths based on witnessed values."""
        if not self.hist.keys():
            return None, None
        return min(self.hist.keys()), max(self.hist.keys())
