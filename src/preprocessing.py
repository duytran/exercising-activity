import pandas as pd

from src.utils import time_to_seconds

SELECTED_COLUMN = [
    "Activity Type",
    "Date",
    "Title",
    "Distance",
    "Calories",
    "Time",
    "Avg HR",
    "Max HR",
    "Aerobic TE",
    "Avg Bike Cadence",
    "Max Bike Cadence",
    "Avg Speed",
    "Max Speed",
    "Total Ascent",
    "Total Descent",
    "Avg Stride Length",
    "Best Lap Time",
    "Number of Laps",
    "Max Temp",
    "Moving Time",
    "Elapsed Time",
    "Min Elevation",
    "Max Elevation",
]


def load_select_feature(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    df = df[SELECTED_COLUMN]

    correct_column_name = {}
    for col_name in SELECTED_COLUMN:
        correct_column_name[col_name] = col_name.replace(" ", "_").lower()

    # rename column name
    df = df.rename(columns=correct_column_name)
    # replace unknow value with 0
    df = df.replace("--", 0)
    # convert time string from hh:mm:ss to seconds
    df["time_seconds"] = df["time"].apply(time_to_seconds)
    df["moving_time_seconds"] = df["moving_time"].apply(time_to_seconds)
    df["elapsed_time_seconds"] = df["elapsed_time"].apply(time_to_seconds)

    return df


def load_running(df: pd.DataFrame) -> pd.DataFrame:
    running_df = df[df["activity_type"] == "Running"]
    return running_df
