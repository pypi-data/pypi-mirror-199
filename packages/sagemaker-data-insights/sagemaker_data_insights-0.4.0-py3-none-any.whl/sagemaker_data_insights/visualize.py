# pylint: disable=R0912, R0915

import altair as alt
import pandas as pd
import numpy as np


NONE_AXIS = alt.Axis(labels=False, title=None, ticks=False)


def plot_robust_histogram(
    h: dict,
    y_map: dict = None,
    ignore_target: bool = False,
    plot_outliers: bool = True,
    width: int = 300,
    height: int = 300,
    interactive: bool = True,
):
    """
    Generates Altair plot of a robust histogram produced by `calc_robust_histogram`. See examples in
    https://github.com/aws/sagemaker-data-insights/tree/visualizations#some-examples

    Parameters
    ----------
    h: dict
        robust histogram dictionary created by `calc_robust_histogram`
    y_map: dict or None
        When the target column is plotted for classification y_map is used to create the legend. As target column
        labels are encoded values: 0, 1, 2, etc., the y_map is used to map back from the encoded labels to the unencoded
        ones. y_map is produced by `analyze_target_classification`. This is not required for regression
    ignore_target: bool
        Whether to avoid plotting the target even if the data exists in the histogram. This flag is ignored When the
        histogram doesn't include target data
    plot_outliers: bool
        Whether to plot the outliers or ignore them
    width: int > 0
        width of the plot
    height: int > 0
        height of the plot
    interactive: bool
        enable interactive plot

    Returns
    -------
    Altair plot
    """
    # Create the data frame used for plotting
    df, target_labels = _prepare_robust_histogram_data_frame(h, y_map, plot_outliers)
    # x_domain is the range of the x-axis
    x_domain = (df["bars_left"].iloc[0], df["bars_right"].iloc[-1])
    tick_values = np.linspace(df["bars_left"].iloc[1], df["bars_right"].iloc[-2], 5)

    chart = alt.Chart(df)
    # Plot the bars of the histogram
    histplot = chart.mark_bar().encode(
        x=alt.X(
            "bars_left:Q", title="", bin="binned", scale=alt.Scale(domain=x_domain), axis=alt.Axis(values=tick_values)
        ),
        x2="bars_right:Q",
        y=alt.Y("bars_height:Q", title="Frequency [%]"),
        color=alt.Color("is_outlier", scale=alt.Scale(scheme="tableau10"), legend=None),
    )
    # If there are outliers, plot a separation rule between the outliers and the histogram
    histplot = _plot_outlier_separation_rules(histplot, chart, df)
    # Add outliers bars x coordinate
    histplot += (
        chart.mark_point(opacity=0)
        .encode(x="x:Q", y="y0")
        .mark_text(color="white", clip=False, dy=12, size=10)
        .encode(text="bar_text")
    )

    if interactive:
        # Selectors for interactive plot
        nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["x"], empty="none")
        selectors = chart.mark_point().encode(x="x:Q", opacity=alt.value(0)).add_selection(nearest)
        # Vertical rules
        rules = chart.mark_rule(color="gray").encode(x="x:Q").transform_filter(nearest)
        # The text has to be split into two because sometimes it appears above the bars (align=right) and sometimes
        # inside the bars (align=left)
        split_frequency = df["bars_height"].max() / 2
        text = []
        for df_, align in [
            (df[df["bars_height"] <= split_frequency], "right"),
            (df[df["bars_height"] > split_frequency], "left"),
        ]:
            text.append(
                alt.Chart(df_)
                .mark_point(opacity=0)
                .encode(x="x:Q", y="bars_height:Q")
                .mark_text(align=align, dx=5 if align == "left" else -5, dy=0, color="white", clip=True, angle=90)
                .encode(text=alt.condition(nearest, "bars_height_text", alt.value(" ")))
            )
        histplot = alt.layer(histplot, selectors, rules, *text)

    # If target statistics do not exist or ignored return the histogram
    if ignore_target or ("target_avg" not in h and "target_labels" not in h):
        return histplot.configure_axis(grid=False).properties(width=width, height=height)

    # remove invalid target column rows from the data frame
    df = df[df["valid_target_idxs"]].copy()

    if "target_avg" in h:
        # Regression
        # Add texts to appear on target plot
        for k in ["avg", "lower", "upper"]:
            df[f"{k}_text"] = ["%.3g" % v for v in df[k]]
        chart = alt.Chart(df)
        y_middle = (min(df["lower"]) + max(df["upper"])) / 2
        y_diff = 1.2 * (max(df["upper"]) - min(df["lower"])) / 2
        y_domain = (y_middle - y_diff, y_middle + y_diff)

        # Plot the average
        target_plot = chart.mark_line(color="red", opacity=0.5).encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=x_domain), axis=NONE_AXIS),
            y=alt.Y("avg:Q", axis=alt.Axis(title="Target value"), scale=alt.Scale(domain=y_domain)),
        )
        # Plot the error band
        target_plot += chart.mark_area(color="red", opacity=0.3).encode(x="x:Q", y="lower:Q", y2="upper:Q")
        # If there are outliers, plot a separation rule between the outliers and the histogram
        target_plot = _plot_outlier_separation_rules(target_plot, chart, df)
        if interactive:
            elements = []
            for y_key, dy in [("avg", 0), ("lower", 10), ("upper", -10)]:
                elements.append(
                    chart.mark_point(color="red", clip=True).encode(
                        x="x:Q",
                        y=alt.Y(f"{y_key}:Q", scale=alt.Scale(domain=y_domain)),
                        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
                    )
                )
                elements.append(
                    elements[-1]
                    .mark_text(align="left", dx=5, dy=dy, color="white", clip=True)
                    .encode(text=alt.condition(nearest, f"{y_key}_text", alt.value(" ")))
                )
            rules = chart.mark_rule(color="gray").encode(x="x:Q").transform_filter(nearest)
            target_plot = alt.layer(target_plot, selectors, *elements, rules)
    else:
        # Classification
        classification_df = _unstack_classification_df(df, target_labels)
        classification_df["label_freq_text"] = ["%.3g%%" % v for v in classification_df["label_freq"]]
        y_middle = (min(classification_df["label_freq"]) + max(classification_df["label_freq"])) / 2
        y_diff = (max(classification_df["label_freq"]) - min(classification_df["label_freq"])) / 2
        y_domain = (y_middle - y_diff, y_middle + 1.2 * y_diff)
        chart = alt.Chart(classification_df).encode(
            x=alt.X("x:Q", sort=df["x"].to_list(), scale=alt.Scale(domain=x_domain), axis=NONE_AXIS),
            y=alt.Y("label_freq:Q", axis=alt.Axis(title="Label frequency [%]"), scale=alt.Scale(domain=y_domain)),
        )
        target_plot = chart.mark_line().encode(
            color=alt.Color(
                "Target label:N", scale=alt.Scale(scheme="dark2"), legend=alt.Legend(title="Target labels")
            ),
        )
        # If there are outliers, plot a separation rule between the outliers and the histogram
        target_plot = _plot_outlier_separation_rules(target_plot, chart, df)
        if interactive:
            chart = chart.encode(color=alt.Color("Target label:N", scale=alt.Scale(scheme="dark2")))
            points = chart.mark_point(clip=True).encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
            text = chart.mark_text(align="left", dx=5, dy=-5, clip=True).encode(
                text=alt.condition(nearest, "label_freq_text", alt.value(" "))
            )
            rules = alt.Chart(classification_df).mark_rule(color="gray").encode(x="x:Q").transform_filter(nearest)
            target_plot = alt.layer(target_plot, selectors, rules, points, text)

    # concat the histogram and the target plot
    return (
        alt.vconcat(
            target_plot.properties(width=width, height=height / 2),
            histplot.properties(width=width, height=height / 2),
            spacing=0,
        )
        .configure_axis(grid=False)
        .resolve_scale(color="independent")
    )


def plot_frequent_elements(
    f: dict,
    y_map: dict = None,
    ignore_target: bool = False,
    max_bar_width: int = 30,
    width: int = 300,
    height: int = 300,
    interactive: bool = True,
):
    """
    Generates Altair plot of frequent elements produced by `calc_frequent_elements`. See examples in
    https://github.com/aws/sagemaker-data-insights/tree/visualizations#some-examples

    Parameters
    ----------
    f: dict
        frequent elements dictionary created by `calc_frequent_elements`
    y_map: dict or None
        When the target column is plotted for classification y_map is used to create the legend. As target column
        labels are encoded values: 0, 1, 2, etc., the y_map is used to map back from the encoded labels to the unencoded
        ones. y_map is produced by `analyze_target_classification`. This is not required for regression
    ignore_target: bool
        Whether to avoid plotting the target even if the data exists in the histogram. This flag is ignored When the
        histogram doesn't include target data
    max_bar_width: int
        maximum width of the bars
    width: int > 0
        The actual width of the plot is the minimum of width and max_bar_width * num_bars
    height: int > 0
        height of the plot
    interactive: bool
        enable interactive plot

    Returns
    -------
    Altair plot
    """
    df, target_labels = _prepare_frequent_elements_data_frame(f, y_map)
    # Add interactive texts
    df["frequency_text"] = ["%.3g%%" % v for v in df["frequency"]]
    if "target_avg" in f:
        for k in ["avg", "lower", "upper"]:
            df[f"{k}_text"] = ["%.3g" % v for v in df[k]]
    width = min(len(df) * max_bar_width, width)

    chart = alt.Chart(df)

    barplot = chart.mark_bar().encode(
        x=alt.X("x:N", sort=f["value"], title=""), y=alt.Y("frequency", title="Frequency [%]"),
    )
    if interactive:
        # Selectors for interactive plot
        nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["x"], empty="none")
        selectors = chart.mark_point().encode(x="x:N", opacity=alt.value(0)).add_selection(nearest)
        # The text has to be split into two because sometimes it appears above the bars (align=right) and sometimes
        # inside the bars (align=left)
        split_frequency = df["frequency"].max() / 2
        text = []
        for df_, align in [
            (df[df["frequency"] <= split_frequency], "right"),
            (df[df["frequency"] > split_frequency], "left"),
        ]:
            text.append(
                alt.Chart(df_)
                .mark_point(opacity=0)
                .encode(x="x:N", y="frequency:Q")
                .mark_text(align=align, dx=5 if align == "left" else -5, dy=0, color="white", clip=True, angle=90)
                .encode(text=alt.condition(nearest, "frequency_text", alt.value(" ")))
            )
        barplot = alt.layer(barplot, selectors, *text)

    if ignore_target or ("target_avg" not in f and "target_labels" not in f):
        return barplot.configure_axis(grid=False).properties(width=width, height=height)

    # remove invalid target column rows from the data frame
    df = df[df["valid_target_idxs"]]

    if "target_avg" in f:
        # Regression
        # Plot the average
        chart = alt.Chart(df).encode(x=alt.X("x:N", sort=f["value"], axis=NONE_AXIS))
        target_plot = chart.mark_point(filled=True, size=50, color="red").encode(
            y=alt.Y("avg:Q", axis=alt.Axis(title="Target"))
        )
        # Plot the error bar
        target_plot += chart.mark_errorbar(color="red").encode(
            y=alt.Y("lower:Q", axis=alt.Axis(title="")), y2="upper:Q"
        )
        if interactive:
            elements = []
            for y_key, dx, dy, align in [("avg", 5, 0, "left"), ("lower", 0, 5, "center"), ("upper", 0, -5, "center")]:
                elements.append(
                    chart.mark_point(opacity=0)
                    .encode(x="x:N", y=f"{y_key}:Q")
                    .mark_text(align=align, dx=dx, dy=dy, color="white", clip=True)
                    .encode(text=alt.condition(nearest, f"{y_key}_text", alt.value(" ")))
                )
            target_plot = alt.layer(target_plot, selectors, *elements)
    else:
        # Classification
        classification_df = _unstack_classification_df(df, target_labels)
        classification_df["label_freq_text"] = ["%.3g%%" % v for v in classification_df["label_freq"]]
        chart = alt.Chart(classification_df).encode(
            x=alt.X("x:N", sort=f["value"], axis=NONE_AXIS),
            y=alt.Y("label_freq:Q", axis=alt.Axis(title="Label frequency [%]")),
            color=alt.Color(
                "Target label:N", scale=alt.Scale(scheme="dark2"), legend=alt.Legend(title="Target labels")
            ),
        )
        target_plot = chart.mark_point().encode(color="Target label:N",)
        if interactive:
            text = chart.mark_text(align="left", dx=5, dy=-5, clip=True).encode(
                text=alt.condition(nearest, "label_freq_text", alt.value(" "))
            )
            target_plot = alt.layer(target_plot, selectors, text)

    # concat the frequent elements and the target plot
    return (
        alt.vconcat(
            target_plot.properties(width=width, height=height / 2),
            barplot.properties(width=width, height=height / 2),
            spacing=0,
        )
        .configure_axis(grid=False)
        .resolve_scale(color="independent")
    )


def _prepare_frequent_elements_data_frame(f: dict, y_map: dict):
    """
    Generate the data frame used for frequent elements plots

    Parameters
    ----------
    f: dict
        frequent elements dictionary created by `calc_frequent_elements`
    y_map: dict or None
        When the target column is plotted for classification y_map is used to create the legend. As target column
        labels are encoded values: 0, 1, 2, etc., the y_map is used to map back from the encoded labels to the unencoded
        ones. y_map is produced by `analyze_target_classification`. This is not required for regression

    Returns
    -------
    pandas.DataFrame with columns:
        x: frequent elements names
        frequency: frequency of elements in percent
        When target column regression statistics exists in f:
            avg: target average for each frequent element
            lower: target average minus one standard deviation for each frequent element
            upper: target average plus one standard deviation for each frequent element
            valid_target_idxs: boolean, whether the target column stats are valid for each frequent element
        When target column classification statistics exists in f:
            valid_target_idxs: boolean, whether the target column stats are valid for each frequent element
            for each target label, the frequency in percent for each frequent element
    target_labels: list or None
        a list of target labels when the task is classification, otherwise None
    """
    df = pd.DataFrame({"x": f["value"], "frequency": [freq * 100 for freq in f["frequency"]]})
    df, target_labels = _add_target_to_dataframe(f, df, y_map)
    return df, target_labels


def _add_target_to_dataframe(d: dict, df: pd.DataFrame, y_map: dict):
    target_labels = None
    if "target_avg" in d:
        # Add regression target stats to the data frame
        avg = np.array(d["target_avg"]).ravel()  # target average
        lower = np.array(d["target_avg"]) - np.array(d["target_std"])  # average minus std for lower confidence band
        upper = np.array(d["target_avg"]) + np.array(d["target_std"])  # average minus std for upper confidence band
        valid_idxs = np.isfinite(upper) & np.isfinite(lower)  # use only the points where the target is well defined
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        "avg": avg,
                        "std": d["target_std"],
                        "lower": lower,
                        "upper": upper,
                        "valid_target_idxs": valid_idxs,
                    }
                ),
            ],
            axis=1,
        )
    if "target_labels" in d:
        # Add classification target stats to the data frame
        tmp_dict = {}
        target_labels = []
        for key, item in d["target_labels"].items():
            # if the task is binary classification plot only the positive class
            if len(d["target_labels"].keys()) == 2 and key == 0:
                continue
            target_labels.append(y_map[key] if y_map else key)
            tmp_dict[str(target_labels[-1])] = list(np.array(item) * 100)
        df = pd.concat([df, pd.DataFrame(tmp_dict)], axis=1)
        if "bars_height" in df:
            df["valid_target_idxs"] = df["bars_height"] > 0
        else:
            df["valid_target_idxs"] = True
    return df, target_labels


def _unstack_classification_df(df, target_labels):
    # bars centers to be used as the x axis
    classification_df = df[[str(tl) for tl in target_labels]]
    classification_df.index = df["x"]
    classification_df = classification_df.unstack().reset_index()
    classification_df.columns = ["Target label", "x", "label_freq"]
    for k in ["lower_outlier_separation_rule", "upper_outlier_separation_rule"]:
        if k in df.columns:
            classification_df[k] = list(df[k])[0]
    return classification_df


def _prepare_robust_histogram_data_frame(h: dict, y_map: dict, plot_outliers: bool):
    """
    Generate the data frame used for robust histogram plots

    Parameters
    ----------
    h: dict
        robust histogram dictionary created by `calc_robust_histogram`
    y_map: dict or None
        When the target column is plotted for classification y_map is used to create the legend. As target column
        labels are encoded values: 0, 1, 2, etc., the y_map is used to map back from the encoded labels to the unencoded
        ones. y_map is produced by `analyze_target_classification`. This is not required for regression
    plot_outliers: bool
        Whether to include the outliers in the data frame or remove them

    Returns
    -------
    pandas.DataFrame with columns:
        is_outlier: "Not outlier" or "outlier"
        bars_left: Left x value of the bars
        bars_right: Right x value of the bars
        bars_height: The height of the bars corresponds to the frequency of the histogram bar in percents
        bar_text: a vector of text. Used to mark x values for outlier bins
        bars_height_text: The height of the bars in a user friendly format. Used for interactive plots
        x: Bars centers, used to plot target statistics
        y0: A vector of zeros
        When target column regression statistics exists in h:
            avg: target average for each histogram bar
            lower: target average minus one standard deviation for each histogram bar
            upper: target average plus one standard deviation for each histogram bar
            valid_target_idxs: boolean, whether the target column stats are valid for each histogram bar
        When target column classification statistics exists in h:
            for each target label, the frequency in percent for each histogram bar
            valid_target_idxs: boolean, whether the target column stats are valid for each histogram bar
            for each target label, the frequency in percent for each histogram bar
        When plotting outliers and lower bar is outlier:
            lower_outlier_separation_rule: x coordinate of the lower separation rule
        When plotting outliers and upper bar is outlier:
            upper_outlier_separation_rule: x coordinate of the upper separation rule
    target_labels: list or None
        A list of target labels when the task is classification, otherwise None
    """
    df = pd.DataFrame(
        {
            "is_outlier": ["Not outlier"] * len(h["hist_count"]),
            "bars_left": [float(val) for val in h["hist_edges"][:-1]],
            "bars_right": [float(val) for val in h["hist_edges"][1:]],
            "bars_height": h["hist_count"] / np.sum(h["hist_count"]) * 100,
            "bar_text": [""] * len(h["hist_count"]),
            "y0": [0] * len(h["hist_count"]),
        }
    )
    df, target_labels = _add_target_to_dataframe(h, df, y_map)

    # Fix the width and position of the outlier bins or remove them according to plot_outliers
    # When `plot_outliers` is True, the outlier bins, if they exist are make narrower by factor of `outlier_bin_width`
    # and moved farther than the histogram.
    # When `plot_outliers` is False, the outlier bins, if they exist are removed.
    bins_width = h["hist_edges"][2] - h["hist_edges"][1]
    if "lower_bin_is_outlier" in h and h["lower_bin_is_outlier"]:
        if plot_outliers:
            df.at[0, "is_outlier"] = "Outlier"
            df.at[0, "bar_text"] = "%.3g" % h["hist_edges"][0]
            df.at[0, "bars_left"] = h["hist_edges"][1] - 3 * bins_width
            df.at[0, "bars_right"] = h["hist_edges"][1] - 2 * bins_width
            df["lower_outlier_separation_rule"] = 0.5 * df.at[0, "bars_right"] + 0.5 * df.at[1, "bars_left"]
        else:
            df.drop(0, inplace=True)
    if "upper_bin_is_outlier" in h and h["upper_bin_is_outlier"]:
        if plot_outliers:
            idx = len(df) - 1
            df.at[idx, "is_outlier"] = "Outlier"
            df.at[idx, "bar_text"] = "%.3g" % h["hist_edges"][-1]
            df.at[idx, "bars_left"] = h["hist_edges"][-2] + 2 * bins_width
            df.at[idx, "bars_right"] = h["hist_edges"][-2] + 3 * bins_width
            df["upper_outlier_separation_rule"] = 0.5 * df.at[idx, "bars_left"] + 0.5 * df.at[idx - 1, "bars_right"]
        else:
            df = df[:-1]

    # x is the bins center, used for plotting the target statistics
    df["x"] = 0.5 * df["bars_left"] + 0.5 * df["bars_right"]
    df["bars_height_text"] = ["%.3g%%" % v for v in df["bars_height"]]
    return df, target_labels


def _plot_outlier_separation_rules(barplot, chart, df: pd.DataFrame):
    is_outlier = df["is_outlier"].to_list()
    # If there are outliers, plot a separation rule between the outliers and the histogram
    if is_outlier[0] == "Outlier":
        # add a vertical line separating the histogram from the lower outliers
        barplot += chart.mark_rule(color="gray").encode(x="lower_outlier_separation_rule:Q")
    if is_outlier[-1] == "Outlier":
        # add a vertical line separating the histogram from the upper outliers
        barplot += chart.mark_rule(color="gray").encode(x="upper_outlier_separation_rule:Q")
    return barplot


# TODO: remove this when no longer necessary. We might want to change the plots in the near future and that code could
#  help do that
# if __name__ == "__main__":
#     alt.themes.enable("dark")
#     from sagemaker_data_insights.const import TaskType as tt
#     from sagemaker_data_insights.histogram_functions import calc_robust_histogram
#
#     x = np.array([-15] * 5 + [100] * 3 + list(np.random.randn(400)))
#     xx = np.clip(x, -3, 3)
#     if True:
#         y = 5 * xx + 10 * np.random.randn(len(x))
#         task = tt.REGRESSION
#         y_map = None
#         title = "Histogram - Regression"
#     elif True:
#         y = np.round((3 + xx + xx * xx + 5 * np.random.randn(len(x))) / 20)
#         y = np.array([int(min(max(val, 0), 1)) for val in y])
#         task = tt.BINARY_CLASSIFICATION
#         y_map = {0: "Dog", 1: "cat"}
#         title = "Histogram - Binary classification"
#     else:
#         y = np.round((5 * xx + xx * xx + 20 * np.random.randn(len(x))) / 15)
#         y = np.array([int(min(max(val, 0), 2)) for val in y])
#         task = tt.MULTICLASS_CLASSIFICATION
#         y_map = {0: "Dog", 1: "cat", 2: "mouse"}
#         title = "Histogram - Multiclass classification"
#     h = calc_robust_histogram(x=x, y=y, task=task, robust_std_percentile=20, num_bins=20)
#     barplot = plot_robust_histogram(h, y_map, plot_outliers=True, ignore_target=False)
#     barplot.properties(title=title).show()
#     import json
#     print(json.dumps(barplot.to_dict()))
#
#
# if __name__ == "__main__":
#     alt.themes.enable("dark")
#     from sagemaker_data_insights.const import TaskType as tt
#     from sagemaker_data_insights.histogram_functions import calc_frequent_elements
#
#     x = np.random.randint(0, 2, (200,)) + np.random.randint(0, 3, (200,))
#     if False:
#         y = 5 * x + x * x + 10 * np.random.randn(len(x))
#         task = tt.REGRESSION
#         y_map = None
#         title = "Frequent elements - Regression"
#     elif True:
#         y = np.round((5 * x + x * x + 10 * np.random.randn(len(x))) / 30)
#         y = np.array([int(min(max(val, 0), 1)) for val in y])
#         task = tt.BINARY_CLASSIFICATION
#         y_map = {0: "Dog", 1: "cat"}
#         title = "Frequent elements - Binary classification"
#     else:
#         y = np.round((5 * x + x * x + 10 * np.random.randn(len(x))) / 15)
#         y = np.array([int(min(max(val, 0), 2)) for val in y])
#         task = tt.MULTICLASS_CLASSIFICATION
#         y_map = {0: "Dog", 1: "cat", 2: "mouse"}
#         title = "Frequent elements - Multiclass classification"
#     x = x.astype(str)
#     x[x == "0"] = "House"
#     x[x == "1"] = "Car"
#     x[x == "2"] = "Boat"
#     x[x == "3"] = "Umbrella"
#     h = calc_frequent_elements(x=x, y=y, task=task)
#     barplot = plot_frequent_elements(h, y_map)
#     barplot.properties(title=title).show()
#     import json
#     print(json.dumps(barplot.to_dict()))
