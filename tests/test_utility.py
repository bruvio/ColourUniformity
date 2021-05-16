#!/usr/bin/env python

# from conftest import ValueStorage

import sys
import os
import pytest
import warnings
import itertools
import numpy as np

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from utility import create_list, distance, create_matrix, create_point, get_adjacents

warnings.simplefilter("ignore")


@pytest.mark.usefixtures("databases")
def test_create_list(databases):
    colours = ["white", "blue", "red", "green"]

    for db in databases:
        for colour in colours:
            vars()[colour] = db[[colour + "_u", colour + "_v"]].values
            colour_list = create_list(vars()[colour])

            assert (len(colour_list) == 35) & (len(colour_list[0]) == 2)


@pytest.mark.usefixtures("databases")
@pytest.fixture(scope="function")
def fList(databases):
    fList = []
    colours = ["white", "blue", "red", "green"]
    for db in databases:
        for colour in colours:
            vars()[colour] = db[[colour + "_u", colour + "_v"]].values
            colour_list = create_list(vars()[colour])
            fullList = [
                [(colour_list[i][0], colour_list[i][1]), i + 1] for i in range(0, 35)
            ]
            fList.append(fullList)
    return fList


@pytest.mark.usefixtures("fList")
def test_distance_input_point(fList):
    for colour_list in fList:
        for i in colour_list:
            assert (
                (isinstance(i[0][0], float))
                & (isinstance(i[1], int))
                & (isinstance(i[0], tuple))
            )


@pytest.mark.usefixtures("fList")
def test_distance(fList):
    for colour_list in fList:
        for p0, p1 in itertools.combinations(colour_list, 2):
            assert isinstance(distance(p0, p1)[0], float) & isinstance(
                distance(p0, p1)[1], str
            )


@pytest.mark.usefixtures("databases")
def test_create_point(databases):
    colours = ["white", "blue", "red", "green"]
    for db in databases:
        for colour in colours:
            vars()[colour] = db[[colour + "_u", colour + "_v"]].values
            point_list = create_point(vars()[colour])
            assert isinstance(point_list, list)


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("databases")
def matrices(databases):
    matrices = []
    colours = ["white", "blue", "red", "green"]
    for db in databases:
        for colour in colours:
            vars()[colour] = db[[colour + "_u", colour + "_v"]].values
            matrix = create_matrix(vars()[colour])
            matrices.append(matrix)
            #
    return matrices


@pytest.mark.usefixtures("matrices")
def test_create_matrix(matrices):
    for matrix in matrices:
        assert isinstance(matrix, np.ndarray)


@pytest.mark.usefixtures("matrices")
def test_matrices_shape(matrices):
    for matrix in matrices:
        m = matrix.shape[0]
        n = matrix.shape[1]
        assert (m == 5) & (n == 7)


@pytest.mark.usefixtures("matrices")
def test_adjacent(matrices):
    i, j = 0, 0
    for matrix in matrices:
        adjacent_indexes = get_adjacents(i, j, matrix)
        for index in adjacent_indexes:
            assert index in [(1, 0), (0, 1)]


@pytest.mark.xfail(reason="index out of bound")
def test_adjacent_outbounds(matrices):
    i, j = -1, 0
    for matrix in matrices:
        adjacent_indexes = get_adjacents(i, j, matrix)
        for index in adjacent_indexes:
            assert index is False
