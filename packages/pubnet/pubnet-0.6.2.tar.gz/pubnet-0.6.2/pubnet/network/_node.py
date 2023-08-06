"""Class for storing node data."""

import os
import re

import numpy as np
import pandas as pd
from pubnet.data import default_data_dir

__all__ = ["Node", "from_file", "from_data"]


class Node:
    """
    Class for storing node data for PubNet class.

    Provides a wrapper around a panda dataframe adding in information
    about the ID column, which is identified by the special syntax
    f"{name}:ID({namespace})" in order to be compatible with Neo4j
    data.  Here the value `namespace` refers to the node so it's not
    important since we already know the the node.

    This class should primarily be initialized through `PubNet` methods.

    Parameters
    ----------
    data : pandas.DataFrame
        `DataFrame` containing node's features.
    id : str, default "detect"
        The `data` column to use as the ID. If `"detect"`, determine the id
        column based on the above mentioned Neo4j syntax. If the provided
        column name doesn't exist, the column will be generated as
        `1:len(data)`.
    features : "all" or list of str, default "all"
        A list of the columns to keep. If "all" keep all columns.

    Attributes
    ----------
    id : str
        The name of the node id. This is the feature that will be used in edges
        to link to the node.
    features
    columns
    shape
    """

    def __init__(self, data, id="detect", features="all"):
        self._data = data
        if data is None:
            self._data = pd.DataFrame()
            self.id = None
            return

        if id == "detect":
            id_regex = r"(\w+):ID\((\w+)\)"
            id_column = list(
                filter(
                    lambda x: x is not None,
                    [re.search(id_regex, name) for name in data.columns],
                )
            )[0]
            self.id = id_column.groups()[0]
            self._data.columns = self._data.columns.str.replace(
                id_column.group(), self.id, regex=False
            )
        else:
            assert (
                id in data.columns
            ), f"Id not in data.\n\tAvailable features: {data.columns}."
            self.id = id

        if features != "all":
            assert isinstance(
                features, list
            ), 'Features must be a list or "all"'
            try:
                self._data = self._data[features]
            except KeyError as err:
                raise KeyError(
                    "One or more selected feature not in data.\n\n\tSelected"
                    f" features: {features}\n\tData's features:"
                    f" {self._data.columns}"
                ) from err

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __getitem__(self, key):
        if key is None:
            # When node is empty, self.id == None.
            return pd.Series(dtype=pd.Float64Dtype)

        if isinstance(key, str):
            return self._data[key]

        if isinstance(key, int):
            return self._data[self._data.columns[key]]

        if isinstance(key, tuple):
            assert (
                len(key) <= 2
            ), f"Nodes are 2d; {key} has too many dimensions."
            rows = key[0]
            columns = key[1]
        elif isinstance(key, list) and isinstance(key[0], str):
            columns = key
            rows = slice(None)
        else:
            rows = key
            columns = slice(None)

        if not isinstance(rows, slice):
            is_mask = len(rows) > 1
            if is_mask and isinstance(rows, pd.Series):
                is_mask = isinstance(rows.values[0], (bool, np.bool8))
            else:
                is_mask = is_mask and isinstance(rows[0], (bool, np.bool8))

            if is_mask:
                return self._data[columns].loc[rows]

        return self._data[columns][rows]

    def __len__(self):
        return len(self._data)

    def set(self, new_data):
        self._data = new_data

    @property
    def features(self):
        """A list of all the node's features."""
        return self._data.columns

    @property
    def columns(self):
        """Alias for features to correspond with dataframe terminology."""
        return self.features

    @property
    def shape(self):
        """A tuple with number of rows and number of features."""
        return self._data.shape

    def get_random(self, n=1, seed=None):
        """
        Sample rows in `Node`.

        Parameters
        ----------
        n : positive int, default 1
            Number of nodes to sample.
        seed : positive int, optional
            Random seed for reproducibility. If not provided, seed is select at
            random.

        Returns
        -------
        nodes : dataframe
            Subset of nodes.
        """

        rng = np.random.default_rng(seed=seed)
        return self._data.loc[rng.integers(0, self._data.shape[0], size=(n,))]

    def isequal(self, node_2):
        """Test if two `Node`s have the same values in all their columns."""

        if not (self.features == node_2.features).all():
            return False

        for feature in self.features:
            if not (self[feature].values == node_2[feature].values).all():
                return False

        return True

    def to_file(
        self,
        node_name,
        graph_name,
        data_dir=default_data_dir(),
        format="tsv",
    ):
        """
        Save the `Node` to file.

        The node will be saved to a graph (a directory in the `data_dir` where
        the graphs nodes and edges are stored).

        Parameters
        ----------
        node_name : str
            Name of the `Node`.
        graph_name : str
            Name of the graph to store it under.
        data_dir : str, optional
            Where the graph is stored. If empty, uses `default_data_dir`.
        format : {"tsv", "gzip", "binary"}, default "tsv"
            the format to save the file as. The binary format uses apache
            feather.

        See also
        --------
        `from_file`
        `pubmed.data.default_data_dir`
        `pubmed.network.pubnet.to_dir`
        `pubmed.network.pubnet.from_dir`
        """

        self._data.columns = self._data.columns.str.replace(
            self.id, f"{self.id}:ID({node_name})", regex=False
        )

        ext = {"binary": "feather", "gzip": "tsv.gz", "tsv": "tsv"}
        file_name = node_name + "_nodes." + ext[format]
        data_dir = os.path.join(data_dir, graph_name)

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        file_path = os.path.join(data_dir, file_name)
        if format == "binary":
            self._data.to_feather(file_path)
        else:
            # `to_csv` will infer whether to use gzip based on extension.
            self._data.to_csv(file_path, sep="\t", index=False)

        self._data.columns = self._data.columns.str.replace(
            f"{self.id}:ID({node_name})", self.id, regex=False
        )


def from_file(file_name, *args):
    """
    Read a `Node` in from a file

    The node will be saved to a graph (a directory in the `data_dir` where
    the graphs nodes and edges are stored).

    Parameters
    ----------
    node_name : str
        Name of the `Node`.
    graph_name : str
        Name of the graph to store it under.
    data_dir : str, optional
        Where the graph is stored.

    Returns
    -------
    node : Node

    Other Parameters
    ----------------
    *args
        All other args are passed forward to the `Node` class.

    See Also
    --------
    `Node`
    `Node.to_file`
    `from_data`
    `pubmed.data.default_data_dir`
    `pubmed.network.pubnet.to_dir`
    `pubmed.network.pubnet.from_dir`
    """

    ext = file_name.split(".")[-1]
    if ext == "feather":
        data = pd.read_feather(file_name)
    else:
        data = pd.read_csv(
            file_name,
            delimiter="\t",
        )
    return from_data(data, *args)


def from_data(data, *args):
    """
    Create a node from a DataFrame.

    Paramaters
    ----------
    Data, DataFrame

    Returns
    -------
    node, Node

    Other Parameters
    ----------------
    *args
        All other args are passed forward to the `Node` class.

    See Also
    --------
    `Node`
    `from_file` : read a `Node` from file.
    `Node.to_file` : save a `Node` to file.
    """

    return Node(data, *args)
