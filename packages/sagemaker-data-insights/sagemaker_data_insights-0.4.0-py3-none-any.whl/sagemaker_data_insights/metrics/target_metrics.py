from dataclasses import dataclass
from typing import List


@dataclass
class TargetMetrics:
    labels: List
    label_counts: List
    cardinality: int
    max: int
    min: int
    numeric_finite_count: int
    nrows: int
    null_like_count: int
    empty_count: int
    whitespace_count: int
