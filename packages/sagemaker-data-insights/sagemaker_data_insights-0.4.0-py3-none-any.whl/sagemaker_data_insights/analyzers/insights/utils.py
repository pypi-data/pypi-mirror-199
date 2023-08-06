import numpy as np
import pandas as pd
import warnings

from sagemaker_data_insights.const import TaskType as tt
from sagemaker_sklearn_extension.impute import RobustImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sagemaker_data_insights.analyzers.insights.sklearn_utils import _encode, _encode_check_unknown
from sklearn.utils.validation import check_is_fitted, column_or_1d, _num_samples


def get_label_encoder(task: str, y: np.array):
    """Prepares `LabelEncoder` against labels specified in an array, and returns a fitted `LabelEncoder` transform.

    For regression, we change any non-numeric value to nan. For multiclass and binary classification, we encode them.

    Args:
        task (str): The problem type. Must be a constant from [REGRESSION, BINARY_CLASSIFICATION,
        MULTICLASS_CLASSIFICATION].
        y (np.array): target data to use for fitting.

    Returns:
        function: `LabelEncoder` transform after fitting.
    """
    if task == tt.REGRESSION:
        return NALabelEncoder().fit(y)

    if task == tt.BINARY_CLASSIFICATION:
        # This code is to insure that the minority class is encoded as `1`
        y_transformed = LabelEncoder().fit_transform(y)
        y_valid = y[np.isfinite(y_transformed)]
        labels, counts = np.unique(y_valid, return_counts=True)
        labels_count = []
        for idx, label in enumerate(labels):
            labels_count.append((label, counts[idx]))
        if labels_count[0][1] > labels_count[1][1]:
            majority_label = labels_count[0][0]
            minority_label = labels_count[1][0]
        else:
            majority_label = labels_count[1][0]
            minority_label = labels_count[0][0]
        return RobustLabelEncoder(
            labels=[majority_label], fill_label_value=minority_label, include_unseen_class=True
        ).fit(y)

    return RobustLabelEncoder().fit(y)


class NALabelEncoder(BaseEstimator, TransformerMixin):
    """Encoder for transforming labels to NA values.

       Uses `RobustImputer` on 1D inputs of labels
       - Uses `is_finite_numeric` mask for encoding by default
       - Only uses the `RobustImputer` strategy `constant` and fills using `np.nan`
       - Default behavior encodes non-float and non-finite values as nan values in
          the target column of a given regression dataset

       Parameters
       ----------

       mask_function : callable -> np.array, dtype('bool') (default=None)
           A vectorized python function, accepts np.array, returns np.array
           with dtype('bool')

           For each value, if mask_function(val) == False, that value will
           be imputed. mask_function is used to create a boolean mask that determines
           which values in the input to impute.

           Use np.vectorize to vectorize singular python functions.

    """

    def __init__(self, mask_function=None):
        self.mask_function = mask_function

    def fit(self, y):
        """Fit the encoder on y.

        Parameters
        ----------
        y : {array-like}, shape (n_samples,)
            Input column, where `n_samples` is the number of samples.

        Returns
        -------
        self : NALabelEncoder
        """
        self.model_ = RobustImputer(strategy="constant", fill_values=np.nan, mask_function=self.mask_function)
        y = y.reshape(-1, 1)
        self.model_.fit(X=y)
        return self

    def transform(self, y):
        """Encode all non-float and non-finite values in y as NA values.

        Parameters
        ----------
        y : {array-like}, shape (n_samples)
            The input column to encode.

        Returns
        -------
        yt : {ndarray}, shape (n_samples,)
            The encoded input column.
        """
        check_is_fitted(self, "model_")
        y = y.reshape(-1, 1)
        return self.model_.transform(y).flatten()

    def inverse_transform(self, y):
        """Returns input column"""
        return y

    def _more_tags(self):
        return {"X_types": ["1dlabels"]}


class RobustLabelEncoder(LabelEncoder):
    """Encode labels for seen and unseen labels.

    Seen labels are encoded with value between 0 and n_classes-1.  Unseen labels are encoded with
        ``self.fill_encoded_label_value`` with a default value of n_classes.

    Similar to ``sklearn.preprocessing.LabelEncoder`` with additional features.
    - ``RobustLabelEncoder`` encodes unseen values with ``fill_encoded_label_value`` or ``fill_label_value``
      if ``fill_unseen_labels=True`` for ``transform`` or ``inverse_transform`` respectively
    - ``RobustLabelEncoder`` can use predetermined labels with the parameter``labels``.

    Examples
    --------
    >>> from sagemaker_sklearn_extension.preprocessing import RobustLabelEncoder
    >>> rle = RobustLabelEncoder()
    >>> rle.fit([1, 2, 2, 6])
    RobustLabelEncoder(fill_encoded_label_value=None,
                   fill_label_value='<unseen_label>', fill_unseen_labels=True,
                   labels=None)
    >>> rle.classes_
    array([1, 2, 6])
    >>> rle.transform([1, 1, 2, 6])
    array([0, 0, 1, 2])
    >>> rle.transform([1, 1, 2, 6, 1738])
    array([ 0,  0,  1,  2, 3])
    >>> rle.inverse_transform([0, 0, 1, 2])
    array([1, 1, 2, 6])
    >>> rle.inverse_transform([-1738, 0, 0, 1, 2])
    ['<unseen_label>', 1, 1, 2, 6]

    It can also be used to transform non-numerical labels (as long as they are
    hashable and comparable) to numerical labels.

    >>> rle = RobustLabelEncoder()
    >>> rle.fit(["hot dog", "hot dog", "banana"])
    RobustLabelEncoder(fill_encoded_label_value=None,
                   fill_label_value='<unseen_label>', fill_unseen_labels=True,
                   labels=None)
    >>> list(rle.classes_)
    ['banana', 'hot dog']
    >>> rle.transform(["hot dog", "hot dog"])
    array([1, 1])
    >>> rle.transform(["banana", "llama"])
    array([0, 2])
    >>> list(rle.inverse_transform([2, 2, 1]))
    ['<unseen_label>', '<unseen_label>', 'hot dog']

    Parameters
    ----------
    labels : list of values (default = None)
        List of unique values for label encoding. Overrides ``self.classes_``.
        If ``labels`` is None, RobustLabelEncoder will automatically determine the labels.

    fill_unseen_labels : boolean (default = True)
        Whether or not to fill unseen values during transform or inverse_transform.

    fill_encoded_label_value : int (default = n_classes)
        Replacement value for unseen labels during ``transform``.
        Default value is n_classes.

    fill_label_value : str (default = '<unseen_label>')
        Replacement value for unseen encoded labels during ``inverse_transform``.

    include_unseen_class: boolean (default = False)
        Whether or not ``fill_label_value`` should be included as a class.

    Attributes
    ----------
    classes_ : array of shape (n_classes,)
        Holds the label for each class that is seen when the encoder is ``fit``.
    """

    def __init__(
        self,
        labels=None,
        fill_unseen_labels=True,
        fill_encoded_label_value=None,
        fill_label_value="<unseen_label>",
        include_unseen_class=False,
    ):
        super().__init__()
        self.labels = labels
        self.fill_unseen_labels = fill_unseen_labels
        self.fill_encoded_label_value = fill_encoded_label_value
        self.fill_label_value = fill_label_value
        self.include_unseen_class = include_unseen_class

    def fit(self, y):
        """Fit label encoder.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Label values.

        Returns
        -------
        self : RobustLabelEncoder.
        """
        y = column_or_1d(y, warn=True)
        self.classes_ = self._check_labels_and_sort() or _encode(y)
        return self

    def _check_labels_and_sort(self):
        if not self.labels:
            return None
        if self._is_sorted(self.labels):
            return self.labels
        warnings.warn("`labels` parameter is expected to be sorted. Sorting `labels`.")
        return sorted(self.labels)

    def _is_sorted(self, iterable):
        return all(iterable[i] <= iterable[i + 1] for i in range(len(iterable) - 1))

    def fit_transform(self, y):
        """Fit label encoder and return encoded labels.

        Parameters
        ----------
        y : array-like of shape [n_samples]
            Label values.

        Returns
        -------
        y_encoded : array-like of shape [n_samples]
                    Encoded label values.
        """
        return self.fit(y).transform(y)

    def transform(self, y):
        """Transform labels to normalized encoding.

        If ``self.fill_unseen_labels`` is ``True``, use ``self.fill_encoded_label_value`` for unseen values.
        Seen labels are encoded with value between 0 and n_classes-1.  Unseen labels are encoded with
        ``self.fill_encoded_label_value`` with a default value of n_classes.

        Parameters
        ----------
        y : array-like of shape [n_samples]
            Label values.

        Returns
        -------
        y_encoded : array-like of shape [n_samples]
                    Encoded label values.
        """
        check_is_fitted(self, "classes_")
        y = column_or_1d(y, warn=True)

        # transform of empty array is empty array
        if _num_samples(y) == 0:
            return np.array([])

        if self.fill_unseen_labels:
            _, mask = _encode_check_unknown(y, self.classes_, return_mask=True)
            y_encoded = np.searchsorted(self.classes_, y)
            fill_encoded_label_value = self.fill_encoded_label_value or len(self.classes_)
            y_encoded[~mask] = fill_encoded_label_value
        else:
            _, y_encoded = _encode(y, uniques=self.classes_, encode=True)

        return y_encoded

    def inverse_transform(self, y):
        """Transform labels back to original encoding.

        If ``self.fill_unseen_labels`` is ``True``, use ``self.fill_label_value`` for unseen values.

        Parameters
        ----------
        y : numpy array of shape [n_samples]
            Encoded label values.

        Returns
        -------
        y_decoded : numpy array of shape [n_samples]
                    Label values.
        """
        check_is_fitted(self, "classes_")
        y = column_or_1d(y, warn=True)

        if y.dtype.kind not in ("i", "u"):
            try:
                y = y.astype(np.float).astype(np.int)
            except ValueError:
                raise ValueError("`y` contains values not convertible to integer.")

        # inverse transform of empty array is empty array
        if _num_samples(y) == 0:
            return np.array([])

        labels = np.arange(len(self.classes_))
        diff = np.setdiff1d(y, labels)

        if diff.size > 0 and not self.fill_unseen_labels:
            raise ValueError("y contains previously unseen labels: %s" % str(diff))

        y_decoded = [self.classes_[idx] if idx in labels else self.fill_label_value for idx in y]
        return y_decoded

    def get_classes(self):
        """Returns the values of the unencoded classes.
        If ``self.include_unseen_class`` is ``True`` include ``self.fill_label_value`` as a class.

        Returns
        -------
        classes : array of shape (n_classes,)
        """
        if self.include_unseen_class and self.fill_unseen_labels:
            return np.append(self.classes_, [self.fill_label_value])

        return self.classes_

def calc_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Calculates the Pearson correlation between two arrays.

    Args:
        x (np.ndarray): The first array
        y (np.ndarray): The second array

    Returns:
        float: The correlation.
    """
    return float(pd.DataFrame(x).corrwith(pd.DataFrame(y)))
