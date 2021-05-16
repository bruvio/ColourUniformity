#!/usr/bin/env python

# from conftest import ValueStorage


import pytest
import sys
import os
import datatest as dt
import warnings

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


warnings.simplefilter("ignore")


# @pytest.mark.parametrize("db",databases)
def test_columns_samples(databases):
    for db in databases:
        dt.validate(
            db.columns,
            {
                "white_u",
                "white_v",
                "red_u",
                "red_v",
                "green_u",
                "green_v",
                "blue_u",
                "blue_v",
            },
        )


@pytest.mark.mandatory
def test_imputer_samples(databases):
    for db in databases:
        assert (db.isnull().sum()).all() == 0


@pytest.mark.mandatory
def test_shape_samples(databases):
    for db in databases:
        assert db.shape == (35, 8)
