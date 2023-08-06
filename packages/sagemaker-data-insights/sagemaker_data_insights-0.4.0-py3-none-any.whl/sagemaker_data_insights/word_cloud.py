import altair as alt
import pandas as pd
import numpy as np


def _spiral(width: int, height: int, num_loops: int = 20, min_distance: int = 5, num_points: int = 5000):
    """
    Creates the spiral of possible positions for the words.
        - Width and height are the dimensions of the plot
        - num_loops is the number of loops in the spiral
        - min_distance is the minimal distance between consecutive points on the spiral
        - num_points is the number of points to try to put on the spiral. Points are removed if they are outside the
            plot or too close to other points
    """
    max_radius = np.sqrt(width * width + height * height) / 2
    spiral = []
    for index in range(num_points):
        r = max_radius * index / num_points
        theta = index / num_points * 2 * np.pi * num_loops
        x = r * np.cos(theta) + width / 2
        y = r * np.sin(theta) + height / 2
        if spiral:
            # This is not the first point
            dx = x - spiral[-1][0]
            dy = y - spiral[-1][1]
            d = np.sqrt(dx * dx + dy * dy)
        else:
            # This is the first point
            d = 2 * min_distance
        if d > min_distance and 0 < x < width and 0 < y < height:
            spiral.append((x, y))
    return spiral


class Rect:
    # Rectangle. Used to detect intersection between words
    def __init__(self, xl: float, xr: float, yt: float, yb: float):
        """
        xl - x left
        xr - x right
        yt - y top
        yb - y bottom
        """
        assert xr > xl and yt > yb
        self.xl = xl
        self.xr = xr
        self.yt = yt
        self.yb = yb

    def intersects(self, r):
        # If one rectangle is on left side of other
        if self.xl >= r.xr or r.xl >= self.xr:
            return False
        # If one rectangle is above other
        if self.yb >= r.yt or r.yb >= self.yt:
            return False
        return True


def _fit_words(
    data: pd.DataFrame,
    width: int,
    height: int,
    size_factor: int,
    min_font_size: int = 5,
    font_width_factor: float = 0.6,
):
    """
    Fit as many words as possible without collisions.
        - Width and height are the plot size
        - The words font size is given by the word frequency multiplied by `size_factor`.
        - The words are fitted into the figure by their order in the `data` according to the spiral created by
            `_spiral`.
        - Once a word can not be fitted, no more words will be added.
        - Words with font size smaller than `min_font_size` will not be added.
        - To calculate the width of the bounding box around each word, we use the heuristic font_size *
            font_width_factor * number of characters in the word

    Returns
    -------
    pd.DataFrame of the words with their position
    """
    df = {"Word": [], "size": [], "prediction_power_unrounded": [], "rect": [], "Frequency": []}

    spiral = _spiral(width, height)

    for _, row in data.iterrows():
        word = row["words"]
        frequency = row["frequencies"]
        font_size = np.round(frequency * size_factor)
        if font_size < min_font_size:
            continue
        success = False
        for x, y in spiral:
            # r is the rectangle bounding box around the word. The height is given by `font_size`. For word width we
            # use the heuristic of `font_size` * `font_width_factor` * number of characters in the word. The default
            # value of `font_width_factor` = 0.6 is good for the default font used in altair
            r = Rect(
                x - font_width_factor * font_size * len(word) / 2,
                x + font_width_factor * font_size * len(word) / 2,
                y + font_size / 2,
                y - font_size / 2,
            )
            intersects_previous = False
            for r2 in df["rect"]:
                if r.intersects(r2):
                    intersects_previous = True
                    break
            if intersects_previous or r.xl < 0 or r.xr > width or r.yb < 0 or r.yt > height:
                continue
            success = True
            break
        if not success:
            break
        df["Word"].append(word)
        df["size"].append(font_size)
        df["prediction_power_unrounded"].append(row["prediction_power_unrounded"])
        df["rect"].append(r)
        df["Frequency"].append("%.3g%%" % (frequency * 100))
    df["x"] = [(r.xl + r.xr) / 2 for r in df["rect"]]
    df["y"] = [(r.yt + r.yb) / 2 for r in df["rect"]]
    df.pop("rect")
    df["Prediction power"] = ["%.3g" % v for v in df["prediction_power_unrounded"]]
    return pd.DataFrame(df)


def _find_best_size_factor(data: pd.DataFrame, width: int, height: int, min_num_words: int):
    best_size_factor = None
    best_num_words = 0
    for size_factor in reversed(np.logspace(1, 4, 50)):
        df = _fit_words(data, width, height, size_factor)
        if not best_size_factor or len(df) > best_num_words:
            best_size_factor = size_factor
            best_num_words = len(df)
        if len(df) >= min(min_num_words, len(data)):
            break
    return best_size_factor


def _create_word_cloud_data_frame(words: list, frequencies: list, prediction_power: list):
    data = pd.DataFrame({"words": words, "frequencies": frequencies})
    data["frequencies"] = data["frequencies"] / np.sum(data["frequencies"])
    if prediction_power:
        data["prediction_power_unrounded"] = prediction_power
        data = data.sort_values("prediction_power_unrounded", ascending=False, ignore_index=True)
    else:
        data["prediction_power_unrounded"] = 0.0
        data = data.sort_values("frequencies", ascending=False, ignore_index=True)
    return data


def plot_word_cloud(
    words: list,
    frequencies: list,
    prediction_power: list = None,
    width: int = 300,
    height: int = 300,
    min_num_words: int = 100,
    interactive: bool = True,
):
    """
    Generates Altair plot of a word cloud produced by `analyze_feature`. See examples in
    https://github.com/aws/sagemaker-data-insights/tree/visualizations#some-examples
    - The size of the words is proportional to word frequency
    - The color of the words is proportional to the words' prediction power if prediction_power is provided. Otherwise
        it would be white.
    - The size of the words will be optimized to include at least `min(min_num_words, len(words))` words in the plot.
        Note that this is not always possible.

    Parameters
    ----------
    words: list(str)
        list of words
    frequencies: list(float)
        list of word frequency. Doesn't have to be normalized
    prediction_power: list(float) or None
        list of word prediction power normalized to the range [0, 1] or None
    width: int > 0
        width of the plot
    height: int > 0
        height of the plot
    min_num_words: int > 0
        minimum number of words to include in the plot
    interactive: bool
        enable interactive word cloud plot

    Returns
    -------
    Altair plot
    """
    assert len(words) == len(frequencies)
    assert prediction_power is None or len(words) == len(prediction_power)
    data = _create_word_cloud_data_frame(words, frequencies, prediction_power)
    best_size_factor = _find_best_size_factor(data, width, height, min_num_words)
    tooltip = ["Word", "Frequency", "Prediction power"] if interactive else alt.value(None)
    return (
        alt.Chart(_fit_words(data, width, height, best_size_factor), width=width, height=height)
        .mark_text(align="center", baseline="middle",)
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[0, width]), axis=None),
            y=alt.X("y:Q", scale=alt.Scale(domain=[0, height]), axis=None),
            text="Word",
            size=alt.Size("size:Q", scale=alt.Scale(domain=(1, 64), range=(1, 64)), legend=None),
            color=alt.Color(
                "prediction_power_unrounded:Q",
                scale=alt.Scale(scheme="blues", domain=alt.Undefined if prediction_power else (0, 1)),
                legend=None,
            ),
            tooltip=tooltip,
        )
    )


def _display_test_cases_internal():
    import os
    from examples.example import calc_data_insights
    from sagemaker_data_insights.const import TaskType

    alt.themes.enable("dark")

    data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../test/data", "movies.csv.gz"))
    text_f = "x00010"  # or 'x00011'
    data = data[[text_f, "y"]]

    di = calc_data_insights(data, TaskType.REGRESSION, "y")
    f = di["features"][text_f]["important_words"]
    plot_word_cloud(f["feature_names"], f["frequencies"], f["normalized_prediction_power"]).show()


# if __name__ == "__main__":
#     _display_test_cases_internal()
