"""File For feature binning."""
from __future__ import annotations
from itertools import groupby
from typing import List, Sequence, cast

import pandas as pd

from ethicml.utility import DataTuple

__all__ = ["bin_cont_feats"]


def bin_cont_feats(data: DataTuple) -> DataTuple:
    """Bin the continuous fetures.

    Given a datatuple, bin the columns that have ordinal features
    and return as afresh new DataTuple.

    :param data: The data to bin.
    :returns: A DataTuple where the ordinal columns have been replaced.
    """
    groups: Sequence[list[str]] = [
        list(group)
        for _, group in groupby(cast(List[str], data.x.columns), lambda x: x.split("_")[0])
    ]

    copy: pd.DataFrame = data.x.copy()

    for group in groups:
        # if there is only one element in the group, then it corresponds to a continuous feature
        if len(group) == 1 and data.x[group[0]].nunique() > 2:
            copy[group] = pd.DataFrame(pd.cut(data.x[group].to_numpy()[:, 0], 5))
            copy = pd.concat([copy, pd.get_dummies(copy[group])], axis="columns")
            copy = copy.drop(group, axis="columns")

    return data.replace(x=copy)
