import streamlit as st
import pandas as pd
import glob

import plotly.express as px

from src.utils import seconds_to_pace
from src.preprocessing import load_select_feature, load_running, load_cycling
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

# General question
st.title("Do you practice diligently?")
st.markdown(
    """
    :red[The author is quite lazy about exercising. If you don't like watching, please upload your data from Garmin Activity]"""
)
st.image("data/garmin.png")

uploaded_file = st.file_uploader("Choose see your statistic from file")
if uploaded_file is not None:
    df = load_select_feature(uploaded_file)
else:
    data_files = glob.glob("data/*.csv")
    df = load_select_feature(data_files[0])

st.header("Overview Statistic")
# ------------------------------------------------------------------------------
st.subheader("⏱️ Time Spent", divider="rainbow")
hours, minutes, seconds = total_activity_times(df)
col1, col2, col3 = st.columns(3)
col1.metric(":stopwatch: Hours", f"{hours}")
col2.metric(":stopwatch: Minutes", f"{minutes}")
col3.metric(":stopwatch: Seconds", f"{seconds}")

# ------------------------------------------------------------------------------
st.subheader("🏁 Total Distance", divider="rainbow")
total_distance = total_activity_distance(df)
st.metric("Distance", f"{total_distance} Km")

# ------------------------------------------------------------------------------
st.subheader("🏆 Mosted Activity", divider="rainbow")
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
st.header("🏃‍♂️ Running")
running_df = load_running(df)
tab1, tab2 = st.tabs(["🗃 Overview", "📈 Statistic"])

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
    running_by_month_df = activity_by_month(running_df)
    running_by_month_df["avg_pace"] = running_by_month_df["avg_speed_seconds"].apply(
        seconds_to_pace
    )

    fig = px.bar(
        running_by_month_df,
        x="month_year",
        y="distance",
        title="Running statistic over months",
        color_discrete_sequence=["gray"],
    )

    line = px.line(
        running_by_month_df, x="month_year", y=["avg_hr", "avg_cadence", "avg_pace"]
    )

    fig.add_traces(line.data)

    st.plotly_chart(fig)

# ------------------------------------------------------------------------------
st.header("🚴‍♂️ Cycling")
cycling_df = load_cycling(df)
tab1, tab2 = st.tabs(["🗃 Overview", "📈 Statistic"])

with tab1:
    col1, col2, col3 = st.columns(3)

    total_run_distance = total_activity_distance(cycling_df)
    col1.metric("Distance", f"{total_run_distance} km")

    hours, minutes, seconds = total_activity_times(cycling_df)
    col2.metric("Time", f"{hours}:{minutes}:{seconds}")

    total_run_calories = total_activity_calories(cycling_df)
    col3.metric("Calories", f"{total_run_calories} kCal")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Longest Activity Cycling", f"{longest_activity_distance(cycling_df)} km"
    )
    hours, minutes, seconds = longest_activity_time(cycling_df)
    col2.metric("Longest Activity Time", f"{hours}:{minutes}:{seconds}")
    col3.metric(
        "Maximum Activity Calories", f"{maximum_activity_calories(cycling_df)} kCal"
    )


with tab2:
    cycling_by_month_df = activity_by_month(cycling_df)
    cycling_by_month_df = cycling_by_month_df.rename(
        columns={"avg_speed_seconds": "avg_speed"}
    )

    fig = px.bar(
        running_by_month_df,
        x="month_year",
        y="distance",
        title="Running statistic over months",
        color_discrete_sequence=["gray"],
    )

    hr_line = px.line(cycling_by_month_df, x="month_year", y=["avg_hr", "avg_speed"])

    fig.add_traces(hr_line.data)

    st.plotly_chart(fig)
