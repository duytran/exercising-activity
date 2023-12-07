import streamlit as st
import pandas as pd
import glob

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from src.utils import time_to_seconds

data_files = glob.glob("data/*.csv")
activities_df = pd.read_csv(data_files[0])

# Selected column
selected_column = [
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
selected_activities_df = activities_df[selected_column]

# convert activity time to numberial time (seconds)
selected_activities_df["Numberical Time"] = selected_activities_df["Time"].apply(
    time_to_seconds
)


st.write(selected_activities_df.head())

# Which the activiy have longest time?
longest_time_idx = selected_activities_df["Numberical Time"].idxmax()
st.write(longest_time_idx)
longest_activity = selected_activities_df.iloc[longest_time_idx]
st.write(longest_activity)

# activities_profile = ProfileReport(selected_activities_df, explorative=True)
# st_profile_report(activities_profile)
