# pylint: disable-msg=E1121

import re
from collections import Counter

import numpy as np
import pandas as pd
import scipy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer

# from whatthelang import WhatTheLang
# from iso639 import languages


def sanitize_strings(strs):
    # Replace leading an trailing whitespace with tokens.
    strs = [show_whitespace(s) for s in strs]
    # Deduplicate strings while maintaining initial order.
    return list(dict.fromkeys(strs))


def show_whitespace(string):
    """Replaces leading and trailing whitespace with tokens. Additionally tokenizes an empty string."""
    if string == "":
        return "{empty string}"

    WHITESPACE = "{whitespace}"
    string = re.sub(r"^\s+", WHITESPACE, string)
    string = re.sub(r"\s+$", WHITESPACE, string)

    return string


def tokenize(data, analyzer, max_ngram):
    """
    Tokenize text

    Parameters
    ----------
    data : list of strings to tokenize
    analyzer : str
        `word`: word tokenizer. Converts to lower case.
        `char`: char tokenizer
        `char_wb`: char tokenizer with word breaks
    max_ngram : int
        number of ngram "merge" iterations

    Returns
    -------
    list :
        list (of length max_ngram) of lists of strings. The first item in the list contains the 1-ngrams, the second -
        the 2-ngrams etc.
"""

    with_case = re.compile(r"(?u)\b\w\w+\b").findall

    def _word_splitter(x):
        return [s.lower() for s in with_case(x)]

    if analyzer == "word":
        splitter = _word_splitter
    elif analyzer in ["char", "char_wb"]:
        splitter = list
    else:
        raise ValueError(f"unknown value for mode: {analyzer}")

    def _tokenize_ngram_simple(string, n, join_token=" "):
        tokens = splitter(string)
        return [join_token.join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

    by_ngram = [[] for _ in range(max_ngram)]
    for text in data:
        for n in np.arange(1, max_ngram + 1):
            if analyzer == "char_wb":
                cur_token_list = []
                words = text.split()
                for word in words:
                    cur_token_list.extend(_tokenize_ngram_simple(word, n, join_token=""))
            else:
                cur_token_list = _tokenize_ngram_simple(text, n)
            by_ngram[n - 1].append(cur_token_list)
    return by_ngram


##################
# token stats
##################
def calculate_frequencies(tokenized_data):
    """

    Parameters
    ----------
    tokenized_data: nested list. tokenized_data[n-1] contains a list, one item per document. tokenized_data[n-1][i]
        is a list of the n-grams in the i'th document

    Returns
    -------
    doc_frequency: list of n items. doc_frequency[n-1] is a dict contianing the document frequency of each n-gram
        observed {ngram: freq}, meaning that number of lines it appeared in
    """

    max_ngram = len(tokenized_data)

    doc_frequency = [Counter() for _ in range(max_ngram)]

    for n in range(max_ngram):
        token_lists = tokenized_data[n]
        for token_list in token_lists:
            counts = Counter(token_list)
            doc_frequency[n].update(counts.keys())

    return doc_frequency


def unique_frequent_tokens(doc_frequency, max_frequency):
    """
    Parameters
    ----------
    doc_frequency: Counter object containing document frequency number per token
    max_frequency: integer >= 1, for all integers x in 1 through max_min_count we compute the number of unique tokens
        after filtering out tokens appearing in less or equal than x documents

    Returns
    -------
    unique_count: list, where unique_count[x] is the number of unique tokens appearing more than x times
    """
    unique_count = [len(doc_frequency)]
    for min_count in range(1, max_frequency):
        cur_count = len([token for token in doc_frequency if doc_frequency[token] > min_count])
        unique_count.append(cur_count)
    return unique_count


def remove_stop_words(token_frequency):
    tokens = token_frequency.keys() - ENGLISH_STOP_WORDS
    return Counter({key: token_frequency[key] for key in sorted(tokens)})


def _compute_infrequent_token_count(tokenized, common, ignore_stop_words):
    all_others = 0
    if ignore_stop_words:
        common = set(ENGLISH_STOP_WORDS).union(common)
    for tokens in tokenized:
        if not set(tokens).issubset(common):
            all_others += 1
    return all_others


def most_common(frequency, tokenized_data, num_common, num_examples, ignore_stop_words=False, add_other_count=False):
    """

    Parameters
    ----------
    frequency: dict/Counter mapping tokens to frequency
    tokenized_data: list of tokens per sentence. Needed when 'add_other_count' is True
    num_common: number of most common tokens we require
    num_examples: total number of sentences in the corpus. Answers are given in percentages, so this is required
    ignore_stop_words: bool, If true, return most common tokens other than stop words
    add_other_count: bool, if true, adds another counter for all non-common tokens

    Returns
    -------
    frequency of each of the common tokens, as a percentage of the number of documents. The format is a list of
    dictionaries, one for each item. This format is required for downstream functions providing plots

    """
    if ignore_stop_words:
        frequency = remove_stop_words(frequency)
    ret = frequency.most_common(num_common)
    if add_other_count:
        all_other_count = _compute_infrequent_token_count(tokenized_data, {x[0] for x in ret}, ignore_stop_words)
        ret.append(("OTHER", all_other_count))
    return {"value": [x[0] for x in ret], "frequency": [x[1] / num_examples for x in ret]}


def use_char_analyzer(char_count):
    median = sorted(char_count)[len(char_count) // 2]
    return median < 10


##################
# numeric features
##################


class CharacterStatistics:
    """
    Extracts syntactic features from a string
        word_count: number of words
        char_count: string length
        special_ratio: ratio of non alphanumeric characters to non-spaces in the string, 0 if empty string
        digit_ratio: ratio of digits characters to non-spaces in the string, 0 if empty string
        lower_ratio: ratio of lowercase characters to non-spaces in the string, 0 if empty string
        capital_ratio: ratio of uppercase characters to non-spaces in the string, 0 if empty string
    """

    @staticmethod
    def word_count(text: str) -> float:
        return int(len(text.split()))

    @staticmethod
    def char_count(text: str) -> float:
        return int(len(text))

    @staticmethod
    def special_ratio(text: str) -> float:
        text = re.sub("\\s+", "", text)
        if not text:
            return 0.0
        special_characters = re.sub(r"[\w]+", "", text)
        return len(special_characters) / len(text)

    @staticmethod
    def digit_ratio(text: str) -> float:
        text = re.sub("\\s+", "", text)
        if not text:
            return 0.0
        return sum(c.isdigit() for c in text) / len(text)

    @staticmethod
    def lower_ratio(text: str) -> float:
        text = re.sub("\\s+", "", text)
        if not text:
            return 0.0
        return sum(c.islower() for c in text) / len(text)

    @staticmethod
    def capital_ratio(text: str) -> float:
        text = re.sub("\\s+", "", text)
        if not text:
            return 0.0
        return sum(c.isupper() for c in text) / len(text)

    functions = {
        "word_count": word_count.__func__,
        "char_count": char_count.__func__,
        "special_ratio": special_ratio.__func__,
        "digit_ratio": digit_ratio.__func__,
        "lower_ratio": lower_ratio.__func__,
        "capital_ratio": capital_ratio.__func__,
    }


##################
# importance of tokens
##################


def token_importance(
    X_unprocessed,
    y,
    task,
    num_top_features=20,
    analyzer="word",
    ngram_range=(1, 3),
    min_df=1,
    max_df=1.0,
    random_state=0,
    n_jobs=1,
    stop_words: list = ENGLISH_STOP_WORDS,
):
    vectorizer = CountVectorizer(
        analyzer=analyzer, ngram_range=ngram_range, min_df=min_df, max_df=max_df, max_features=100
    )
    vectorized_data = vectorizer.fit_transform(list(X_unprocessed.reshape((-1))))

    if scipy.sparse.issparse(vectorized_data) and not isinstance(vectorized_data, scipy.sparse.csc_matrix):
        vectorized_data = vectorized_data.tocsc()

    binarized_data = (vectorized_data.toarray() > 0).astype(np.int)
    frequencies = np.sum(binarized_data, axis=0)
    frequencies = [float(int(freq) / len(X_unprocessed)) for freq in frequencies]

    pdf = {
        "feature_names": vectorizer.get_feature_names(),
        "frequencies": frequencies,
    }

    if y is None:
        sort_key = "frequencies"
    else:
        from sagemaker_data_insights.model_utils import _calc_prediction_power
        prediction_power = [
            _calc_prediction_power(
                vectorized_data[:, idx].todense().reshape((-1, 1)), y, task, random_state=random_state, n_jobs=n_jobs
            )
            for idx in range(vectorized_data.shape[1])
        ]
        sort_key = "prediction_power"
        prediction_power, normalized_prediction_power = zip(*prediction_power)
        pdf["prediction_power"] = prediction_power
        pdf["normalized_prediction_power"] = normalized_prediction_power

    pdf = pd.DataFrame(pdf)
    # remove multiple words
    pdf = pdf[~pdf["feature_names"].str.contains(" ")]
    # remove stop words
    pdf = pdf[~pdf["feature_names"].str.lower().isin(stop_words)]
    # sort
    pdf = pdf.sort_values("feature_names", axis=0)
    pdf = pdf.sort_values(sort_key, axis=0, ascending=False, kind="stable")
    pdf = pdf.head(num_top_features)
    return pdf.to_dict("list")

# Disabled due to dependency issues
# def _code_to_lang(code):
#     keys = ["alpha2", "part1", "part2b", "part2t", "part3"]
#     for k in keys:
#         try:
#             return languages.get(**{k: code}).name
#         except AttributeError:
#             continue
#     return "UNKNOWN"
#
#
# def language_stats(data, max_lang_number=8):
#     wtl = WhatTheLang()
#     lang = Counter()
#     for text in data:
#         try:
#             cur_lang = wtl.predict_lang(text)
#         except ValueError:
#             cur_lang = "CANT_PREDICT"
#         lang[cur_lang] = lang[cur_lang] + 1
#     ret = Counter()
#     for language, c in lang.most_common(max_lang_number):
#         if language == "CANT_PREDICT":
#             ret["UNKNOWN"] = c
#         else:
#             ret[_code_to_lang(language)] = c
#     ret["OTHER"] = sum(lang.values()) - sum(ret.values())
#     language_count_pairs = sorted(ret.items(), key=lambda x: -x[1])
#     return {
#         "value": [x[0] for x in language_count_pairs],
#         "frequency": [x[1] / len(data) for x in language_count_pairs],
#     }
