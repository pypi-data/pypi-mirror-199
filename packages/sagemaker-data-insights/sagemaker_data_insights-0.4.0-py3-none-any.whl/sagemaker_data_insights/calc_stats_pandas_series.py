import pandas as pd
import numpy as np

from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.histogram_functions import _unique_without_whitespaces
from sagemaker_data_insights.utils.feature_transform import get_feature_transform


def _calc_stats_pandas_series(
    x: pd.Series,
    max_unique_labels: int = 100,
    datetime_num_rows: int = 10000,
    dw_light_mode: bool = False,
    optimize_datetime_parsing: bool = False,
    random_state: int = 1,
):
    nrows = x.shape[0]
    x_no_na = x.dropna()
    x_numpy = x.astype(str).to_numpy().astype(str)
    unique, counts = _unique_without_whitespaces(x_no_na.to_numpy(dtype=str))

    x_head = x.astype(str).head(datetime_num_rows)

    x_float = get_feature_transform(ft.NUMERIC, True).fit_transform(x_numpy.reshape((-1, 1))).ravel()
    is_numeric = ~pd.isnull(x_float)
    numeric_count = np.sum(is_numeric)

    DATETIME_SAMPLE_SIZE = 1000
    DATETIME_SAMPLE_THRESHOLD = 0.95
    if len(x) < DATETIME_SAMPLE_SIZE:
        optimize_datetime_parsing = False

    reparse_datetimes = False
    if optimize_datetime_parsing:
        # Datetime parsing is slow when operating on columns without many dates
        # such as long textual columns or categorical columns.  We implement a
        # short-circuit that samples a column. If there aren't many dates in
        # that column, then the column is marked as not as date column.
        # If there are many dates in the column, the column will be parsed as
        # usual.  We use a sample size of 1000 and a threshold of 95% - meaning
        # that at least 95% of the sample must be a 'date' in order to consider
        # parsing the colum further.
        # Currently `optimize_date_parsing` is used in Ganymede for performance
        # reasons with dates.
        x_sample = x_head.sample(n=DATETIME_SAMPLE_SIZE, random_state=random_state)
        is_numeric_sample = is_numeric[x_sample.index]
        is_datetime = ~pd.isnull(pd.to_datetime(x_sample.astype(str), errors="coerce"))
        is_datetime_non_numeric = is_datetime * ~is_numeric_sample[:datetime_num_rows]

        # Multiplication factor from our sample to the entire column.
        factor = len(x) / DATETIME_SAMPLE_SIZE

        datetime_count = int(np.sum(is_datetime) * factor)

        if datetime_count / len(x) > DATETIME_SAMPLE_THRESHOLD:
            # If our sample shows that the majority of rows contain dates, then we can proceed to completely parse
            # the row as it won't be slow.
            reparse_datetimes = True
        else:
            # To avoid recomputing this, we only compute it if we are not going to reparse datetimes.
            datetime_non_float_count = int(np.sum(is_datetime_non_numeric) * factor)

    if not optimize_datetime_parsing or reparse_datetimes:
        # This code path is used by Canvas and parses the 'head' only.
        is_datetime = ~pd.isnull(pd.to_datetime(x_head, errors="coerce"))
        is_datetime_non_numeric = is_datetime * ~is_numeric[:datetime_num_rows]

        datetime_count = int(np.sum(is_datetime))
        datetime_non_float_count = int(np.sum(is_datetime_non_numeric))

    stats = {
        "cardinality": len(unique),
        "median": float(np.nanmedian(x_float)) if numeric_count > 0 else np.nan,
        "numeric_finite_count": int(np.sum(is_numeric)),
        "null_like_count": int(nrows - x_no_na.shape[0]),
        "empty_count": int(np.sum(x_numpy == "")),
        "whitespace_count": int(np.sum(np.char.strip(x_numpy) == "")) - int(np.sum(x_numpy == "")),
        "datetime_count": datetime_count,
        "datetime_non_float_count": datetime_non_float_count,
        "datetime_rows_parsed": len(is_datetime),
        "nrows": nrows,
    }

    if not dw_light_mode:
        stats.update(
            {
                "labels": unique.tolist()[:max_unique_labels],
                "label_counts": counts.tolist()[:max_unique_labels],
                "max": float(np.nanmax(x_float)) if numeric_count > 0 else np.nan,
                "min": float(np.nanmin(x_float)) if numeric_count > 0 else np.nan,
                "mean": float(np.nanmean(x_float)) if numeric_count > 0 else np.nan,
                "integer_count": int(np.sum([val.is_integer() for val in x_float])),
            }
        )

    return stats
