# %%
from functools import partial, wraps
import math
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


def InputingDF(df):
    """imputes dataframe with median strategy

    Args:
        df ([type]): [pandas dataframe]

    Returns:
        [type]: [imputed pandas dataframe]
    """
    df.replace("", np.NaN, inplace=True)

    imp = SimpleImputer(missing_values=np.NaN, strategy="median")
    idf = pd.DataFrame(imp.fit_transform(df))
    idf.columns = df.columns
    idf.index = df.index
    return idf


def create_list(colour):
    """utility function for creating list from colour measurements points

    Args:
        colour ([numpy.ndarray]): [column wise list containing measurements]

    Returns:
        [list]: [list of measurements ]
    """
    fList = []
    for o in range(0, len(colour)):
        mInput = [colour[o][0], colour[o][1]]
        x, y = float(mInput[0]), float(mInput[1])
        fList += [(x, y)]
    return fList


def distance(p0, p1):
    """[computes Euclidean distance between given points]

    Args:
        p0 ([list]): [first point]
        p1 ([list]): [second point]

    Returns:
        [float]: [distance]
    """

    return [
        math.sqrt((p0[0][0] - p1[0][0]) ** 2 + (p0[0][1] - p1[0][1]) ** 2),
        "distance between index {} and {}".format(p0[1], p1[1]),
    ]


def print_result(func=None, *, prefix=""):
    """decorator to prettify print of results"""
    if func is None:
        return partial(print_result, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__ + " called with parameters \n")
        for arg in args:
            print(arg)
        result = func(*args, **kwargs)
        print(f"{prefix}{result}")
        # return result

    return wrapper


def create_point(colour):
    """[given a numpy array with measurements points returns list of points]

    Args:
        colour ([string]): [name of the colour]

    Returns:
        [list]: [list of measurement points]
    """
    x = []
    y = []
    for o in range(0, len(colour)):
        x.append(colour[o][0])
        y.append(colour[o][1])

    fList = list(zip(x, y))
    return fList


def create_matrix(colour, m=5, n=7):
    """create matrix of measurements ordered accordingly to README file provided

    Args:
        colour ([string]): [name of the colour]
        m (int, optional): [number of rows]. Defaults to 5.
        n (int, optional): [number of columns]. Defaults to 7.

    Returns:
        [numpy array]: [matrix of measurement points]
    """
    fList = create_point(colour)
    matrix = [[0 for x in range(0, n)] for y in range(0, m)]
    index = 1
    for i in range(m - 1, -1, -1):
        for j in range(0, n):
            matrix[i][j] = [fList[j + n * (m - i - 1)], index]
            index += 1
    mm = np.asarray(matrix, dtype=object)
    return mm


def get_adjacents(i, j, matrix):
    """given a matrix and a couple of indices finds indexes of points
    adjacent to given input

    Args:
        i ([int]): [index of row]
        j ([int]): [index of column]
        matrix ([numpy array]): [matrix of measurements]

    Returns:
        [list]: [list of adjacent indexes]
    """
    m = matrix.shape[0]
    n = matrix.shape[1]
    adjacent_indexes = []
    if i > m or j > n or i < 0 or j < 0:
        return adjacent_indexes
    if i > 0:
        adjacent_indexes.append((i - 1, j))

    if i + 1 < m:
        adjacent_indexes.append((i + 1, j))

    if j > 0:
        adjacent_indexes.append((i, j - 1))

    if j + 1 < n:
        adjacent_indexes.append((i, j + 1))
    return adjacent_indexes


def create_adjacent_list(adjacent_indexes, matrix):
    """given the list of adjacent indeces returns values for those indexes
    for the given input matrix

    Args:
        adjacent_indexes ([list]): [list of adjacent indexes to use]
        matrix ([numpy array]): [matrix of measurement]

    Returns:
        [list]: [list of coordinates]
    """
    aList = []
    if adjacent_indexes:

        for o in range(0, len(adjacent_indexes)):
            mInput = matrix[adjacent_indexes[o][0], adjacent_indexes[o][1]][0]
            x, y = float(mInput[0]), float(mInput[1])
            aList += [
                [(x, y), matrix[adjacent_indexes[o][0], adjacent_indexes[o][1]][1]]
            ]
        return aList
