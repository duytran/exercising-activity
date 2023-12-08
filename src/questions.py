import pandas as pd
import streamlit as st
from src.utils import parse_seconds_to_time


def total_activity_times(df: pd.DataFrame):
    """
    How much total time have you spent exercising in the past year?
    """
    total_time = sum(df["time_seconds"])
    hours, minutes, seconds = parse_seconds_to_time(total_time)
    return hours, minutes, seconds


def total_activity_distance(df: pd.DataFrame):
    """
    What is the total distance you have covered in the past year?
    """
    total_distance = round(sum(df["distance"]))
    return total_distance


def mosted_activity(df: pd.DataFrame):
    """
    Which sport do you play the most and compare the rate with other sports?
    """
    grouped_at_df = df.groupby("activity_type").size().reset_index(name="count")
    mosted_activity_type = grouped_at_df.iloc[grouped_at_df["count"].idxmax()][
        "activity_type"
    ]

    return grouped_at_df, mosted_activity_type


def activity_by_month(df: pd.DataFrame):
    """
    Want to see activity chart by month?
    """
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["month_year"] = df["month"].astype(str) + "-" + df["year"].astype(str)
    df["month_year"] = pd.to_datetime(df["month_year"])
    grouped_time_df = df.groupby("month_year")["distance"].sum().reset_index()
    return grouped_time_df


def total_activity_calories(df: pd.DataFrame):
    total_calories = round(sum(df["calories"].astype(int)))
    return total_calories


def longest_activity_distance(df: pd.DataFrame):
    return max(df["distance"])


def longest_activity_time(df: pd.DataFrame):
    time = max(df["time_seconds"])
    return parse_seconds_to_time(time)


def maximum_activity_calories(df: pd.DataFrame):
    return max(df["calories"].astype(int))


def count_full_marathon(df: pd.DataFrame):
    return df[df["distance"] >= 42.195].shape[0]


def count_half_marathon(df: pd.DataFrame):
    return df[df["distance"] >= 21.0975].shape[0]


def count_10k_run(df: pd.DataFrame):
    return df[df["distance"] >= 10].shape[0]
