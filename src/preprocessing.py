import pandas as pd
import streamlit as st

from src.utils import time_to_seconds, pace_to_seconds

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


FEATURE_NUMBER = [
    "distance",
    "calories",
    "avg_hr",
    "avg_cadence",
    "avg_speed_seconds",
    "avg_stride_length",
    "time_seconds",
]


def load_select_feature(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    df = df[SELECTED_COLUMN]

    correct_column_name = {}
    for col_name in SELECTED_COLUMN:
        if col_name == "Avg Bike Cadence":
            correct_column_name["Avg Bike Cadence"] = "avg_cadence"
        else:
            correct_column_name[col_name] = col_name.replace(" ", "_").lower()

    # rename column name
    df = df.rename(columns=correct_column_name)
    # replace unknow value with 0
    df = df.replace("--", 0)
    # convert time string from hh:mm:ss to seconds
    df["time_seconds"] = df["time"].apply(time_to_seconds)
    df["moving_time_seconds"] = df["moving_time"].apply(time_to_seconds)
    df["elapsed_time_seconds"] = df["elapsed_time"].apply(time_to_seconds)
    df["avg_speed_seconds"] = df["avg_speed"].apply(pace_to_seconds)

    # st.write(df)

    # convert to numberic feature
    df[FEATURE_NUMBER] = df[FEATURE_NUMBER].apply(pd.to_numeric)
    return df


def load_running(df: pd.DataFrame) -> pd.DataFrame:
    running_df = df[df["activity_type"] == "Running"]
    return running_df


def load_cycling(df: pd.DataFrame) -> pd.DataFrame:
    cycling_df = df[df["activity_type"] == "Cycling"]
    return cycling_df
