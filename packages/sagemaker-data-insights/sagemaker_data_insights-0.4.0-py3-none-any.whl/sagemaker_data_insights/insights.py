import logging


class Insights:
    # Severity
    HIGH = "high_sev"  # High severity insights indicate a probable issue in the data. There should be very few false
    # positive high severity insights. It is recommended to highlight these warnings
    MEDIUM = "med_sev"  # Medium severity insights indicate a possible issue with the data. By design, many of these
    # insights are false positive
    LOW = "low_sev"  # Low severity insights are either not important or with low confidence. Generally, they should
    # not be presented and are included here for completeness
    MEDIUM_FEATURE = "med_sev_feature"  # This is a medium sev insight for a feature. Should be considered medium
    # severity if the feature is important (e.g. if the feature is in top 5 most important features) and as low
    # severity otherwise

    # All insights are documented in
    # https://quip-amazon.com/mtjFAjDJctrk/AP-pre-training-report-Part-2-Warnings-and-recommendations
    # Note: The quip document is not maintained while the documentation here is maintained

    ################################
    # Target column insights
    ################################
    SKEWED_TARGET = "Skewed target"
    SKEWED_TARGET_THRESHOLD = 3
    # HIGH
    # Triggered by `analyze_target_regression` when target column includes outliers and it's skew is larger than
    # SKEWED_TARGET_THRESHOLD
    # info: {}
    HEAVY_TAILED_TARGET = "Heavy tailed target"
    HEAVY_TAILED_TARGET_THRESHOLD = 10
    # HIGH
    # Triggered by `analyze_target_regression` when target column includes outliers and SKEWED_TARGET is not activated
    # and kurtosis is larger than HEAVY_TAILED_TARGET_THRESHOLD
    # info: {}
    TARGET_OUTLIERS = "Target has few outliers"
    TARGET_OUTLIERS_THRESHOLD = 3
    # MEDIUM
    # Triggered by `analyze_target_regression` when target column includes outliers and SKEWED_TARGET is not activated
    # and kurtosis is between TARGET_OUTLIERS_THRESHOLD and HEAVY_TAILED_TARGET_THRESHOLD
    # info: {}
    REGRESSION_FREQUENT_LABEL = "Regression frequent label"
    ALLOWED_FREQUENCY_FACTOR = 5
    ALLOWED_FREQUENCY = 0.1
    # MEDIUM
    # Triggered by `analyze_target_regression` when the frequency of the most common target label is larger than
    # max(ALLOWED_FREQUENCY, ALLOWED_FREQUENCY_FACTOR/target_cardinality)
    # info: {"label": the too common label, "frequency": frequency of the too common label}
    REGRESSION_MANY_NONNUMERIC = "Regression many non-numeric values"
    REGRESSION_MANY_NONNUMERIC_THRESHOLD = 0.05
    NUM_NONUMERIC_LABELS = 10
    # HIGH
    # Triggered by `analyze_target_regression` when the frequency of non-numeric values is larger than
    # REGRESSION_MANY_NONNUMERIC_THRESHOLD
    # info: {"frequency": non-numeric frequency,
    #        "values": list of at most NUM_NONUMERIC_LABELS most common non-numeric values
    #        }
    REGRESSION_NONNUMERIC = "Regression non-numeric values"
    # MEDIUM
    # Triggered by `analyze_target_regression` when the frequency of non-numeric values is larger than 5%
    # info: {"frequency": non-numeric frequency,
    #        "values": list of the 10 most common non-numeric values
    #        }
    VERY_SMALL_MINORITY = "Very small minority class"
    VERY_SMALL_MINORITY_THRESHOLD = 20
    # HIGH
    # Triggered by `analyze_target_classification` when the task is BINARY_CLASSIFICATION and the minority label count
    # is less than VERY_SMALL_MINORITY_THRESHOLD
    # info: {"count": minority label count
    #        "label": minority label
    #        "sample_size": size of the sample used
    #        "ratio": count / sample_size
    #        }
    HIGH_TARGET_CARDINALITY = "Too many classes"
    HIGH_TARGET_CARDINALITY_THRESHOLD = 100
    # MEDIUM
    # Triggered by `analyze_target_classification` when the task is MULTICLASS_CLASSIFICATION and cardinality of the
    # target column is larger than HIGH_TARGET_CARDINALITY_THRESHOLD
    # info: {"cardinality": target column cardinality}
    RARE_TARGET_LABEL = "Too few instances per class"
    RARE_TARGET_LABEL_THRESHOLD = 10
    # HIGH
    # Triggered by `analyze_target_classification` when the task is MULTICLASS_CLASSIFICATION and
    # HIGH_TARGET_CARDINALITY was not triggered and there is a label with a count of at most RARE_TARGET_LABEL_THRESHOLD
    # info: {"label": the rare label, "count": rare label count}
    IMBALANCED_CLASSES = "Classes too imbalanced"
    IMBALANCED_CLASS_RATIO = 0.01
    # MEDIUM
    # Triggered by `analyze_target_classification` when the task is MULTICLASS_CLASSIFICATION and
    # HIGH_TARGET_CARDINALITY was not triggered and there is a label with a count of more than
    # RARE_TARGET_LABEL_THRESHOLD but less than IMBALANCED_CLASS_RATIO the count of the most common label
    # info: {"label": infrequent label, "count": infrequent label count, "most_frequent_label": most frequent label,
    # "most_frequent_label_count": most frequent label count}

    ################################
    # Feature insights
    ################################
    TARGET_LEAKAGE = "Target leakage"
    TARGET_LEAKAGE_THRESHOLD = 0.95
    # HIGH
    # Triggered by `analyze_feature` when the normalized prediction power of a feature is larger than
    # {TARGET_LEAKAGE_THRESHOLD}.
    # Important: If there are many features (e.g. > 2) with target leakage then it's probable that the task is just
    # "easy". In that case it's not advised to raise multiple target leakage warnings. Instead, it's recommended to
    # raise a "Multiple target leakage" warning. See
    # https://quip-amazon.com/mtjFAjDJctrk/AP-pre-training-report-Part-2-Warnings-and-recommendations#aBW9CAmXLVG
    # info: {}
    TARGET_CORRELATION = "Target correlation"
    TARGET_CORRELATION_THRESHOLD = 0.95
    # HIGH
    # Triggered by `analyze_feature` when the Pearson correlation coefficients are above the threshold
    # {TARGET_CORRELATION_THRESHOLD}.
    # Important: This is added in addition to Target leakage for performance reasons (it is quicker).
    # info: {}
    UNINFORMATIVE_FEATURE = "Uninformative feature"
    UNINFORMATIVE_FEATURE_THRESHOLD = 0
    # LOW
    # Triggered by `analyze_feature` when the normalized prediction power of a feature is smaller or equal to
    # {UNINFORMATIVE_FEATURE_THRESHOLD}.
    # info: {}
    CONSTANT_FEATURE = "Constant feature"
    # LOW
    # Triggered by `analyze_feature` when the feature has a single value
    # info: {}
    NUMERIC_DISGUISED_MISSING_VALUE = "Numeric disguised missing value"
    NUMERIC_DISGUISED_THRESHOLD = 0.1
    NUMERIC_DISGUISED_RATIO = 10
    NUMERIC_DISGUISED_MIN_UNIQUE = 20
    # MEDIUM_FEATURE
    # Triggered by `analyze_feature` for a numeric feature where there is a value that is very frequent and we suspect
    # that it is used to indicate a missing value. For example the value 0 or 999. The insight is triggered when all
    # the conditions below are satisfied:
    #   1. The frequency of the most common value is > {NUMERIC_DISGUISED_THRESHOLD}
    #   2. The frequency of the most common value > {NUMERIC_DISGUISED_RATIO} times the frequency of the second most
    #   common value
    #   3. The most common value is numeric
    #   4. The column contains at least {NUMERIC_DISGUISED_MIN_UNIQUE} unique values
    # info: {'value': the disguised missing value, 'frequency': frequency of the disguised missing}
    CATEGORICAL_RARE_CATEGORIES = "Categorical rare categories"
    CATEGORICAL_RARE_CATEGORIES_THRESHOLD = 0.05
    NUM_RARE_CATEGORIES_THRESHOLD = 2
    # MEDIUM_FEATURE
    # Triggered by `analyze_feature` for a categorical feature where there is at least one category with frequency less
    # than {CATEGORICAL_RARE_CATEGORIES_THRESHOLD} of the frequency of the most frequent category
    # info: {"rare_categories": list of the rare categories, "rare_categories_frequency": list of the rare categories
    # frequency}
    QUICK_MODEL_VERY_LOW = "Quick model very low validation score"
    # HIGH
    # Triggered by `quick_model` when the validation score of the trivial model is higher than the validation score of
    # xgboost
    # info: {}
    QUICK_MODEL_LOW = "Quick model low validation score"
    QUICK_MODEL_LOW_BIAS = 0.05
    # MEDIUM
    # Triggered by `quick_model` when the validation score of xgboost is lower than
    # {QUICK_MODEL_LOW_BIAS} + (1 - {QUICK_MODEL_LOW_BIAS}) * {trivial validation score}. So xgboost is better than the
    # trivial model, but only marginally
    # info: {}
    MANY_DUPLICATE_ROWS = "Many duplicate rows"
    MANY_DUPLICATE_ROWS_THRESHOLD = 0.05
    # HIGH
    # Triggered by `duplicate_rows` when the ratio of duplicate rows is larger than {MANY_DUPLICATE_ROWS_THRESHOLD}
    # info: {"sample_size": size of the sample used
    #        "duplicate_ratio": ratio of duplicate samples to sample size}
    DUPLICATE_ROWS = "Duplicate rows"
    # MEDIUM
    # Triggered by `duplicate_rows` when the dataset includes duplicate rows and MANY_DUPLICATE_ROWS is not triggered
    # info: {"sample_size": size of the sample used
    #        "duplicate_ratio": ratio of duplicate samples to sample size}
    HIGH_CONFIDENCE_PATTERN = "High-confidence pattern detected"
    HIGH_CONFIDENCE_PATTERN_THRESHOLD = 0.85
    # MEDIUM
    # Triggered by `analyze_feature` when a pattern is found with a high confidence but there are still outliers.
    # info: {"pattern": the pattern found, "confidence": the confidence of the pattern, "num_experiments": the number
    # of experiments run "sample_size": total number of strings considered (with replacement)}

    @staticmethod
    def generate(key, severity, info=None):
        logging.debug("Adding insight, key:%s, severity:%s", key, severity)
        assert severity in [Insights.HIGH, Insights.MEDIUM, Insights.MEDIUM_FEATURE, Insights.LOW]
        assert key in list(Insights().__class__.__dict__.values())
        d = {"key": key, "severity": severity}
        if info:
            d["info"] = info
        return d
