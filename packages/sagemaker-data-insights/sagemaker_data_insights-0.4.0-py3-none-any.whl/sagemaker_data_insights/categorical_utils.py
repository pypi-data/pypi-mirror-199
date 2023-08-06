from typing import List, Dict
from collections import Counter
from difflib import SequenceMatcher
import logging
import numpy as np

from sklearn.cluster import AgglomerativeClustering


def find_duplicate_categories(
    strs: List[str],
    max_categories: int = 100,
    max_str_length=50,
    correction_threshold=0.7,
    distance_threshold: float = 0.1,
) -> Dict[str, str]:
    """Given a list of textual categories containing typographical errors, this
    method will return a mapping that defines corrections to those categories.

    Args:
        categories (List[str]): A list of textual categories.
        max_categories (int, optional): The maximum number of categories to
                                process (for performance).
        max_str_length (int, optional): The maximum length of a string to consider (for performance).
        correction_threshold (int, optional): Corrections are only made if the
                                most popular category is occurs with at least
                                this threshold.
        distance_threshold (float, optional): The distance threshold to use when
                                computing clusters (0-1).

    Returns:
        Dict[str, str]: A map from categories to corrected categories. Only
        categories to be corrected are included in this map.
    """
    # 1. Preprocess and validate input.
    # Remove duplicates. This is crucial for performance if the list has many duplicate entries.
    deduped_strs = set(strs)
    # Remove strings that are too long.
    categories = list(set(filter(lambda x: len(x) <= max_str_length, deduped_strs)))

    n = len(categories)

    # If there are too few distinct categories, there is nothing to do. If there
    # are too many, we don't proceed due to performance constraints.
    # Note: it would be a better optimization to choose the top max_categories to process.
    if n > max_categories or n < 2:
        return {}

    # 2. Compute the distance matrix for the set of categories
    distances = _compute_distance_matrix(categories)

    # 3. Find hieararchial clusters in the categories.
    hierarchial = AgglomerativeClustering(
        n_clusters=None, distance_threshold=distance_threshold, affinity="precomputed", linkage="complete"
    )
    hierarchial.fit(distances)

    # Interpret the hierarchical clusters. Fit returns a list of ordinals with
    # equal ordinals corresponding to identical categories.  We transform this
    # list to a list of lists.
    labels = hierarchial.labels_
    label_indices = {}
    for index, label in enumerate(labels):
        if label in label_indices:
            label_indices[label].append(index)
        else:
            label_indices[label] = [index]

    # 4. Construct a mapping of category counts that we will use to sort categories by popularity.
    category_counts = Counter(strs)  # pylint: disable=E1121

    category_mapping = {}
    for _, indices in label_indices.items():
        if len(indices) <= 1:
            continue

        # Create a list of ordered pairs containing categories and their counts.
        category_class = [categories[i] for i in indices]
        category_class_with_counts = [(cat, category_counts[cat]) for cat in category_class]

        # Find the canonical representative of the equivalance class based on popularity.
        representative, representative_count = max(category_class_with_counts, key=lambda x: x[1])

        # Make sure the category representative meets the correction_threshold to make corrections
        total_count = sum([category_counts[cat] for cat in category_class])
        popularity = representative_count / total_count

        if popularity < correction_threshold:
            continue

        logging.debug("Found %d category typo(s) for textual category", len(category_class) - 1)

        # Add the mappings to the category mapping
        for cat in category_class:
            if cat == representative:
                continue
            category_mapping[cat] = representative

    return category_mapping


def correct_category_typos(strs: List[str]) -> List[str]:
    """Given a list of textual categories containing typographical errors, this
    method will a corrected list of categories.

    Args:
        strs (List[strs]): A list of textual categories.

    Returns:
        List[strs]: A corrected list of categories.
    """
    category_mapping = find_duplicate_categories(strs)

    # Apply the category mapping to the strings to produce a corrected set of strs.
    corrected_strs = strs[:]
    for i, s in enumerate(strs):
        if s in category_mapping:
            corrected_strs[i] = category_mapping[s]

    return corrected_strs


def _compute_distance_matrix(strs: List[str]) -> np.ndarray:
    """Computes a distance matrix between strings using fuzzy string matching."""
    n = len(strs)
    distances = np.zeros(shape=(n, n))
    for i, ic in enumerate(strs):
        for j, jc in enumerate(strs):
            distances[i, j] = 1 - similarity_score(ic, jc)

    return distances


def similarity_score(s1: str, s2: str) -> float:
    """A similarity score between strings. This method is symmetric in the arguments.

    This uses a fast implementation of Levenshtein distance. This uses difflibs under the hood.

    Args:
        s1 (str): The first string
        s2 (str): The second string

    Returns:
        float: A number from 0 to 1 indicating how similiar the strings are, with 1 being the most similar.
    """
    if not s1 or not s2:
        return 0

    m = SequenceMatcher(None, s1, s2)
    return m.ratio()
