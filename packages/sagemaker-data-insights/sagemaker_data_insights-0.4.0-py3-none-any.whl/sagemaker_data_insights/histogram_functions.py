# pylint: disable=R0912

import numpy as np
import pandas as pd

from sagemaker_data_insights.const import TaskType as tt


def calc_robust_histogram(  # noqa: C901
    x: np.ndarray,
    y: np.ndarray = None,
    task=None,
    num_bins=20,
    stds=5,
    robust_std_percentile=5,
    robust_histogram_eps=1e-10,
):
    """
    Calculates robust histogram for a vector

    Parameters
    ----------
    x : np.ndarray
        feature data. A column numpy array of size (height,). All values must be valid floats
    y : np.ndarray  or None
        target column. A column numpy array of size (height,). When the task is classification, y cannot contain NaN or
        None values
    task : str in [REGRESSION, BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION]
        When y is not None task must be provided
    num_bins : int >= 3
        number of bins in histogram
    stds : float > 0
        Values which are farther away than `stds` robust standard deviations from the robust mean are considered
        outliers
    robust_std_percentile : int in [1, 99]
        Robust standard deviation used for outlier detection is calculate on all data between percentile
        robust_std_percentile to 100 - robust_std_percentile
    robust_histogram_eps: float
        Small value used to pad some internal values. All values in [lower_bound, upper_bound) are valid. In order to
        avoid having np.max(x) always becoming an outlier we add a small float to it

    Returns
    -------
    dict : data insights histogram
        hist_count: list(int)
            Number of items in each histogram bar
        hist_edges: list(float)
            Histogram edges
        lower_bin_is_outlier: boolean
            Indicator whether the left most bin is an outliers bin
        upper_bin_is_outlier: boolean
            Indicator whether the right most bin is an outliers bin
        target_avg: list(float)
            The average of the target column for each histogram bar. This field exists only when y is provided and the
            task is regression
        target_std: list(float)
            The standard deviation of the target column for each histogram bar. This field exists only when y is
            provided and the task is regression
        target_labels: dict
            This field exists only when y is provided and the task is classification
            The dict keys are the target labels. The value for each key is a list(float) indicating the percentage of
            labels for each histogram bar that equal the key
"""
    if np.sum(~np.isfinite(x)) > 0:
        raise ValueError("Error: x contains NaN or infinite values")
    if num_bins < 3:
        raise ValueError("Error: num_bins < 3")
    ps = np.percentile(x, [robust_std_percentile, 100 - robust_std_percentile])
    std = np.std(np.clip(x, ps[0], ps[1]))
    if std <= robust_histogram_eps:
        std = np.std(x)
    med = np.median(x)
    max_x = np.max(x)
    min_x = np.min(x)
    # All values in [lower_bound, upper_bound) are valid
    upper_bound = min(max_x + robust_histogram_eps, med + stds * std)
    lower_bound = max(min_x, med - stds * std)
    # Whether lower and upper outliers exists
    has_upper_outliers = sum(x > upper_bound) > 0
    has_lower_outliers = sum(x < lower_bound) > 0
    if has_lower_outliers or has_upper_outliers:
        num_bins -= int(has_lower_outliers) + int(has_upper_outliers)
        bin_width = (upper_bound - lower_bound) / num_bins
        bins = [lower_bound + bin_width * i for i in range(num_bins + 1)]
        if has_lower_outliers:
            # Add bin for lower outliers
            bins = [min_x] + bins
        if has_upper_outliers:
            # Add bin for upper outliers
            bins = bins + [max_x]
    else:
        bins = num_bins
    count, bin_edges = np.histogram(x, bins=bins)
    h = {
        "hist_count": count.astype(int).tolist(),
        "hist_edges": bin_edges.astype(float).tolist(),
        "lower_bin_is_outlier": bool(has_lower_outliers),
        "upper_bin_is_outlier": bool(has_upper_outliers),
    }
    if y is not None:
        _verify_y(y, task)
        if task == tt.REGRESSION:
            h["target_avg"] = []
            h["target_std"] = []
        else:
            h["target_labels"] = {}
            all_target_labels = np.unique(y).tolist()
            for y_label in all_target_labels:
                h["target_labels"][y_label] = []
        for idx in range(count.shape[0]):
            # y_ is the part of y which belongs to the bin of index "idx". It is used to calculate statistics for the
            # target column for this bin
            if idx == 0:
                y_ = y[x < bin_edges[idx + 1]]
            elif idx == count.shape[0] - 1:
                y_ = y[x >= bin_edges[idx]]
            else:
                y_ = y[(x >= bin_edges[idx]) & (x < bin_edges[idx + 1])]
            if task == tt.REGRESSION:
                # Add target statistics for bin "idx" when the task is regression using the vector y_
                _regression_append(y_, h["target_avg"], h["target_std"])
            else:
                # Add target statistics for bin "idx" when the task is classification using the vector y_
                _classification_append(y_, h["target_labels"], all_target_labels)
    return h


def robust_histogram_num_outliers(robust_histogram):
    num_outliers = 0
    if robust_histogram["lower_bin_is_outlier"]:
        num_outliers += robust_histogram["hist_count"][0]
    if robust_histogram["upper_bin_is_outlier"]:
        num_outliers += robust_histogram["hist_count"][-1]
    return num_outliers


def _frequent_element_helper(x: np.ndarray, y: np.ndarray, max_num_elements: int):
    """
    Prepares base factors that will bed needed for frequency calculation
    """
    valid_idxs = ~pd.isnull(x)
    x = x[valid_idxs]
    if y is not None:
        y = y[valid_idxs]

    unique, counts = _unique_without_whitespaces(x)
    num_values = np.sum(counts)

    # sort the keys alphabetically so ties in counts will be broken alphabetically
    sorting_indexes = np.argsort(unique)
    unique = unique[sorting_indexes]
    counts = counts[sorting_indexes]

    # include only max_num_elements most frequent elements
    indices = np.argsort(-counts, kind="stable")[:max_num_elements]

    return x, y, unique, counts, num_values, indices


def calc_frequent_elements(x: np.ndarray, y: np.ndarray = None, task=None, max_num_elements=10, sort_type="frequency"):
    """
    Gather statistics about the frequent elements for a vector

    Parameters
    ----------
    x : np.ndarray
        feature data. A column numpy array of size (height,). Data type must be sortable (by numpy)
    y : np.ndarray or None
        target column. A column numpy array of size (height,). When the task is classification, y cannot contain NaN or
        None values
    task : str in [REGRESSION, BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION]
        When y is not None task must be provided
    max_num_elements : int > 0
        maximum number of elements to include in the response. The top max_num_elements most frequent elements are
        returned. Ties are broken by ascending alphabetical order
    sort_type : str in ['frequency', 'value']
        whether to return the result sorted by the frequency or ascending alphabetically by value
    dw_light_mode: True or False
        For Data Wrangler Embedded Data Insight Chart only

    Returns
    -------
    dict : data insights frequent elements stats
        value: list(str)
            Most frequent items in the data. Converted to strings
        frequency: list(float)
            Frequency of each element
        target_avg: list(float)
            The average of the target column for each feature value. This field exists only when y is provided and the
            task is regression
        target_std: list(float)
            The standard deviation of the target column for each feature value. This field exists only when y is
            provided and the task is regression
        target_labels: dict
            This field exists only when y is provided and the task is classification
            The dict keys are the target labels. The value for each key is a list(float) indicating the percentage of
            labels for each feature value that equal the key
"""
    assert sort_type in ["frequency", "value"]

    x, y, unique, counts, num_values, indices = _frequent_element_helper(x, y, max_num_elements)

    f = {"value": unique[indices], "frequency": counts[indices] / num_values}

    # sort according to sort_type if required
    if sort_type != "frequency":
        sorting_indexes = np.argsort(f[sort_type])
        f["value"] = np.array(f["value"])[sorting_indexes]
        f["frequency"] = np.array(f["frequency"])[sorting_indexes]

    f["value"] = f["value"].tolist()
    f["frequency"] = f["frequency"].tolist()
    if y is not None:
        _verify_y(y, task)
        if task == tt.REGRESSION:
            f["target_avg"] = []
            f["target_std"] = []
        else:
            f["target_labels"] = {}
            all_target_labels = np.unique(y).tolist()
            for y_label in all_target_labels:
                f["target_labels"][y_label] = []
        for frequent_value in f["value"]:
            # y_ is the part of y for rows where x == frequent_value. It is used to calculate statistics for the target
            # column
            y_ = y[x == frequent_value]
            if task == tt.REGRESSION:
                # Add target statistics for rows where x == frequent_value when the task is regression using the
                # vector y_
                _regression_append(y_, f["target_avg"], f["target_std"])
            else:
                # Add target statistics for rows where x == frequent_value when the task is classification using the
                # vector y_
                _classification_append(y_, f["target_labels"], all_target_labels)
    return f


def _verify_y(y: np.array, task: str):
    if task not in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]:
        raise ValueError(
            "Error: when y is provided task must be REGRESSION, BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION"
        )
    if task in [tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION, tt.CLASSIFICATION]:
        if any(value is np.nan for value in y) > 0:
            raise ValueError("Error: nans are not allowed in y for classification task")
        if any(value is None for value in y) > 0:
            raise ValueError("Error: None are not allowed in y for classification task")


def _regression_append(y_, target_avg, target_std):
    # Add target statistics when the task is regression. y_ is usually a subset of the target column where some other
    # condition is satisfied. For example when the value of a feature x belongs to some range or equals to some value
    if y_.shape[0] == 0:
        # When y_ is empty, missing value is the appropriate target value
        target_avg.append(np.nan)
        target_std.append(np.nan)
    else:
        target_avg.append(float(np.nanmean(y_)))
        target_std.append(float(np.nanstd(y_)))


def _classification_append(y_, target_labels, all_target_labels):
    unique, counts = np.unique(y_, return_counts=True)
    unique = unique.tolist()
    count_dict = dict(zip(unique, counts))
    for label in all_target_labels:
        target_labels[label].append(float(count_dict[label] / y_.shape[0]) if label in count_dict.keys() else float(0))


def _unique_without_whitespaces(x):
    """
    Returns the list of unique items with their counts excluding items of only whitespaces. Items of only whitespaces
    are considered missing thus they are not valid keys for frequent elements plots
    """
    unique, counts = np.unique(x, return_counts=True)
    unique_ = []
    counts_ = []
    for u, c in zip(unique, counts):
        if str(u).strip() != "":
            unique_.append(u)
            counts_.append(int(c))
    return np.array(unique_), np.array(counts_)
