"""Helper functions for writing publication network functions."""

import os

__all__ = ["edge_key", "node_file_path", "edge_file_path"]


def edge_key(node_1, node_2):
    """Generate a dictionary key for the given pair of nodes."""

    return "-".join(sorted((node_1, node_2)))


def node_file_path(name, data_dir):
    """Return the file path for a node."""
    return os.path.join(data_dir, f"{name}_nodes.tsv")


def edge_file_path(node_1, node_2, data_dir):
    """Find the edge file in data_dir for the provided node types.

    Known possible issues:
        If we need directed edges, the order of nodes in the file name
        may be important. Add in a weighted keyword argument, if true
        look for files only with the nodes in the order they were
        provided otherwise look for both. Another option is to not
        only check the file name but check the header for the START_ID
        and END_ID node types.
    """

    def edge_file_path(n1, n2):
        return os.path.join(data_dir, f"{n1}_{n2}_edges.tsv")

    if os.path.exists(edge_file_path(node_1, node_2)):
        file_path = edge_file_path(node_1, node_2)
    elif os.path.exists(edge_file_path(node_2, node_1)):
        file_path = edge_file_path(node_2, node_1)
    else:
        raise FileNotFoundError(
            f"No edge file for edges {node_1}, {node_2} found in"
            f" {data_dir}\n\nExpceted either file"
            f" '{edge_file_path(node_1, node_2)}'"
            f" or'{edge_file_path(node_2, node_1)}'"
        )

    return file_path
