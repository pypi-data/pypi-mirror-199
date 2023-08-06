from pydeequ.profiles import *


def column_profiler(spark_session, df, selected_columns: list = []):
    """
    Column profiler to run analysis on all/a subset of columns in the dataframe

    Parameters
    ----------
    spark_session: spark session
    df: spark DataFrame
    selected_columns: list, a list of input columns

    Returns
    -------
    profiles: dict, column profiles
    """
    if selected_columns:
        df = df.select(*selected_columns)

    result = ColumnProfilerRunner(spark_session).onData(df).run()

    return result.profiles
