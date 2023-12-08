import streamlit as st
import pandas as pd
import glob

import plotly.express as px

from src.utils import time_to_seconds, parse_seconds_to_time
from src.preprocessing import load_select_feature, load_running
from src.questions import (
    total_activity_times,
    total_activity_distance,
    mosted_activity,
    activity_by_month,
    total_activity_calories,
    longest_activity_distance,
    longest_activity_time,
    maximum_activity_calories,
    count_full_marathon,
    count_half_marathon,
    count_10k_run,
)

data_files = glob.glob("data/*.csv")
df = load_select_feature(data_files[0])

# General question
st.title("Do you practice diligently?")
st.header("Overview Statistic")

# ------------------------------------------------------------------------------
st.subheader("Time Spent", divider="rainbow")
hours, minutes, seconds = total_activity_times(df)
col1, col2, col3 = st.columns(3)
col1.metric(":stopwatch: Hours", f"{hours}")
col2.metric(":stopwatch: Minutes", f"{minutes}")
col3.metric(":stopwatch: Seconds", f"{seconds}")

# ------------------------------------------------------------------------------
st.subheader("Total Distance", divider="rainbow")
total_distance = total_activity_distance(df)
st.metric("Distance", f"{total_distance} Km")

# ------------------------------------------------------------------------------
st.subheader("Mosted Activity", divider="rainbow")
grouped_at_df, mosted_activity_type = mosted_activity(df)

st.metric(
    "Activity Type",
    f"{mosted_activity_type}",
)

fig = px.pie(
    grouped_at_df,
    names="activity_type",
    values="count",
    title="Percentage of Activity",
)
st.plotly_chart(fig)

# ------------------------------------------------------------------------------
st.subheader("Activity by Months", divider="rainbow")
grouped_time_df = activity_by_month(df)
fig = px.area(grouped_time_df, x="month_year", y="distance", title="Activity by Months")
st.plotly_chart(fig)

# ------------------------------------------------------------------------------
st.header("Running Statistic")
running_df = load_running(df)
tab1, tab2 = st.tabs(["📈 Overview", "🗃 Data"])

with tab1:
    col1, col2, col3 = st.columns(3)

    total_run_distance = total_activity_distance(running_df)
    col1.metric("Distance", f"{total_run_distance} km")

    hours, minutes, seconds = total_activity_times(running_df)
    col2.metric("Time", f"{hours}:{minutes}:{seconds}")

    total_run_calories = total_activity_calories(running_df)
    col3.metric("Calories", f"{total_run_calories} kCal")

    col1, col2, col3 = st.columns(3)
    col1.metric("Longest Activity Run", f"{longest_activity_distance(running_df)} km")
    hours, minutes, seconds = longest_activity_time(running_df)
    col2.metric("Longest Activity Time", f"{hours}:{minutes}:{seconds}")
    col3.metric(
        "Maximum Activity Calories", f"{maximum_activity_calories(running_df)} kCal"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Full Marathon", f"{count_full_marathon(running_df)}")
    col2.metric("Half Marathon", f"{count_half_marathon(running_df)}")
    col3.metric("10 km Run", f"{count_10k_run(running_df)}")


with tab2:
    st.header("")
