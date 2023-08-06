from pyspark.sql import functions as sf
from pyspark.sql.types import (
    StringType,
    DateType,
    TimestampType,
)


def drop_missing(df, input_column=None):
    """
    Spark transformer to drop rows with missing values.

    Args:
        df: spark DataFrame

    """
    indicator_col_name = temp_col_name(df)
    if input_column:
        indicator = handle_missing_get_indicator_column(df, input_column, df.schema[input_column].dataType)
        output_df = df.withColumn(indicator_col_name, indicator)
    else:
        output_df = df
        for f in df.schema.fields:
            indicator = handle_missing_get_indicator_column(df, "`" + f.name + "`", f.dataType)
            if indicator_col_name in output_df.columns:
                output_df = output_df.withColumn(
                    indicator_col_name, sf.when(indicator | output_df[indicator_col_name], True).otherwise(False)
                )
            else:
                output_df = df.withColumn(indicator_col_name, indicator)
    output_df = output_df.where(f"{indicator_col_name} == 0").drop(indicator_col_name)

    return output_df


def temp_col_name(df, *illegal_names, prefix: str = "temp_col"):
    """Generates a temporary column name that is unused.
    """
    name = prefix
    idx = 0
    name_set = set(list(df.columns) + list(illegal_names))
    while name in name_set:
        name = f"_{prefix}_{idx}"
        idx += 1

    return name


def handle_missing_get_indicator_column(df, input_column, expected_type):
    """Helper function used to get an indicator for all missing values."""
    dcol = df[input_column].cast(expected_type)
    if isinstance(expected_type, StringType):
        indicator = sf.isnull(dcol) | (sf.trim(dcol) == "")
    elif isinstance(expected_type, (DateType, TimestampType)):
        indicator = sf.col(input_column).isNull()
    else:
        indicator = sf.isnull(dcol) | sf.isnan(dcol)
    return indicator
