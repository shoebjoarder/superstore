import threading
from collections import OrderedDict
from typing import Any, Dict, List, Tuple

import pandas as pd


# The dataset lives in the browser (dcc.Store) and is re-sent to the server on
# every callback. Rebuilding a ~10k-row DataFrame (and dropping NaNs) on each
# invocation is wasted work, especially when a single store update fans out to
# several callbacks that each rebuild the *same* frame. This module memoizes the
# cleaned DataFrame so that repeated/simultaneous callbacks reuse one build.

_CACHE_MAX = 8
_cache: "OrderedDict[Tuple, pd.DataFrame]" = OrderedDict()
_lock = threading.Lock()


def _fingerprint(records: List[Dict[str, Any]]) -> Tuple:
    """Cheap, collision-resistant key for a list of record dicts.

    Filtering always changes the row count and a data entry always prepends a
    new row, so length plus the first/last row identifiers uniquely identify the
    payloads this app produces — without paying to hash the whole 5 MB blob.
    """
    if not records:
        return ("empty",)
    first, last = records[0], records[-1]
    return (
        len(records),
        first.get("Order ID"),
        first.get("Product ID"),
        last.get("Order ID"),
        last.get("Product ID"),
    )


def get_clean_df(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Return ``pd.DataFrame(records).dropna()``, memoized by content.

    A defensive copy is returned so callers may freely mutate (add columns,
    append rows) without corrupting the cached frame.
    """
    key = _fingerprint(records)
    with _lock:
        cached = _cache.get(key)
        if cached is not None:
            _cache.move_to_end(key)
            return cached.copy()

    df = pd.DataFrame(records).dropna()

    with _lock:
        _cache[key] = df
        _cache.move_to_end(key)
        while len(_cache) > _CACHE_MAX:
            _cache.popitem(last=False)
    return df.copy()
