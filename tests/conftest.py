import pytest
import datatest as dt
import sys
import os
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utility import InputingDF


class ValueStorage:
    value1 = None
    value2 = None


@pytest.fixture(scope="session")
@dt.working_directory(parentdir)
def df():
    return pd.read_excel("uniformity-excercise.xlsx", sheet_name="Sheet1")


@pytest.fixture(scope="session")
def databases(df):
    df.dropna(how="all", axis=1, inplace=True)

    # %% [markdown]
    # ### dividing data in 2 samples as per instructions

    # %%

    sample1_df = df[df.columns[1:9]]
    sample2_df = df[df.columns[9:]]

    # %% [markdown]
    # ### dropping useless columns and first two useles rows

    # %%
    sample1_df_clear = sample1_df.drop(sample1_df.index[[0, 1]])
    sample2_df_clear = sample2_df.drop(sample2_df.index[[0, 1]])
    sample1_df_clear = sample1_df_clear.reset_index(drop=True)
    sample2_df_clear = sample2_df_clear.reset_index(drop=True)

    # %% [markdown]
    # ### sanity renaming of columns

    # %%

    new_column_list = [
        "white_u",
        "white_v",
        "red_u",
        "red_v",
        "green_u",
        "green_v",
        "blue_u",
        "blue_v",
    ]

    sample1_df_clear.columns = new_column_list
    sample2_df_clear.columns = new_column_list

    # %% [markdown]
    # ### dealing with potential missing data

    # %%

    sample1_final = InputingDF(sample1_df_clear)
    sample2_final = InputingDF(sample2_df_clear)

    return [sample1_final, sample2_final]
