# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%


import pandas as pd
import itertools
from utility import (
    InputingDF,
    create_list,
    distance,
    print_result,
    create_matrix,
    get_adjacents,
    create_adjacent_list,
)
import warnings

warnings.simplefilter("ignore")

# %% [markdown]
# ### reading file

# %%


# %% [markdown]
# # Solving task A


def read_data():
    df = pd.read_excel("uniformity-excercise.xlsx", sheet_name="Sheet1")

    # %% [markdown]
    # ### removing empty columns

    # %%

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

    return sample1_final, sample2_final


# %%
@print_result(prefix="The return value is ")
def task_A(colour, DF):
    """main function to solve task A

    Args:
        colour ([string]): [name of the colour to be used for calculations]
        DF ([pandas dataframe]): [dataframe containing input data to be
        used]

    Returns:
        [float]: [max colour difference between any 2 points for the
        given colour]
    """
    vars()[colour] = DF[[colour + "_u", colour + "_v"]].values

    fList = create_list(vars()[colour])

    fullList = [[(fList[i][0], fList[i][1]), i + 1] for i in range(0, 35)]
    vars()["max_distance_" + colour] = distance(fullList[0], fullList[1])
    for p0, p1 in itertools.combinations(fullList, 2):

        vars()["max_distance_" + colour] = max(
            vars()["max_distance_" + colour], distance(p0, p1)
        )

    return vars()["max_distance_" + colour]


# %% [markdown]
# # Solving task B

# %%
@print_result(prefix="The return value is ")
def task_B(colour, DF):
    """main function to solve task B
        scans the matrix to find the two points that are horizontally
        or vertically adjacent and returns the max colour distance
    Args:
        colour ([string]): [name of the colour to be used for
        calculations]
        DF ([pandas dataframe]): [dataframe containing input
        data to be used]
    Returns:
        [float]: [max distance between any two adjacent points
        horizontally or vertically]
    """
    vars()[colour] = DF[[colour + "_u", colour + "_v"]].values
    matrix = create_matrix(vars()[colour])
    m = matrix.shape[0]
    n = matrix.shape[1]
    maxAdjacent_max_distance = 0
    comment = ""
    for i in range(0, m):
        for j in range(0, n):

            adjacent_indexes = get_adjacents(i, j, matrix)
            aList = create_adjacent_list(adjacent_indexes, matrix)

            if aList:

                Adjacent_max_distance = 0
                for p in aList:
                    if distance(matrix[i][j], p)[0] > Adjacent_max_distance:
                        Adjacent_max_distance = distance(matrix[i][j], p)[0]
                        comment = distance(matrix[i][j], p)[1]

            maxAdjacent_max_distance = max(
                maxAdjacent_max_distance, Adjacent_max_distance
            )
    return [Adjacent_max_distance, comment]


# %%

if __name__ == "__main__":

    sample1_final, sample2_final = read_data()
    colours = ["white", "blue", "red", "green"]
    # %%
    for db in [sample1_final, sample2_final]:
        for colour in colours:
            task_A(colour, db)
            task_B(colour, db)
