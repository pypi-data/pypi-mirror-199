from dataclasses import dataclass
from typing import Optional


@dataclass
class Metrics:
    """
    Metrics class for getting column stats
    """
    nrows: int
    cardinality: int
    numeric_finite_count: int
    null_like_count: int
    empty_count: int
    whitespace_count: int
    datetime_count: int
    datetime_non_float_count: int
    datetime_rows_parsed: int
    median: float
    max: Optional[float] = None
    min: Optional[float] = None
    mean: Optional[float] = None
    integer_count: Optional[int] = None
    labels: Optional[list] = None
    label_counts: Optional[list] = None
