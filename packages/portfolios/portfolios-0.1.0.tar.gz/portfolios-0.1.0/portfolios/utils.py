import rich
import numpy as np
from pathlib import Path

__all__ = ["flatten", "toMatrix", "pkgdir", "rootdir"]

pkgdir = Path(__file__).parent

rootdir = pkgdir.parent

def flatten(dictionary, sep=".") -> dict:
    """Flatten a dictionary of dictionaries into a single dictionary.

    Args:
        dictionary (dict): A dictionary of dictionaries.

    Returns:
        dict: A flattened dictionary.

    """
    flattened = {}

    for key, value in dictionary.items():
        if isinstance(value, dict):
            lowered = flatten(value, sep=sep)
            for k, v in lowered.items():
                flattened[f"{key}{sep}{k}"] = v
        elif isinstance(value, list):
            for i, v in enumerate(value):
                if isinstance(v, dict):
                    lowered = flatten(v, sep=sep)
                    for k, v in lowered.items():
                        flattened[f"{key}{sep}nb{i}{sep}{k}"] = v
                else:
                    flattened[f"{key}{sep}nb{i}"] = v
        else:
            flattened[key] = value
    return flattened


def toMatrix(dictionary, sep=".") -> dict:
    """Convert a dictionary of dictionaries into a matrix.

    Args:
        dictionary (dict): A dictionary of dictionaries.

    Returns:
        dict: A matrix.

    """
    flattened = flatten(dictionary, sep=sep)
    keys = list(flattened.keys())
    values = list(flattened.values())
    max_len = max(len(key.split(sep)) for key in keys)
    matrix = np.empty((len(keys), max_len)).astype(object)
    matrix[:] = ''
    values = np.array(values)
    for i, key in enumerate(keys):
        for j, k in enumerate(key.split(sep)):
            matrix[i, j] = k
            
    matrix[:, -1] = values
    return matrix.tolist()