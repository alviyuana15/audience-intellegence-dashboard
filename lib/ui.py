import streamlit as st
from lib.utils import apply_filters


def page_config():
    st.set_page_config(
        page_title="HIGO Audience Profiling Dashboard",
        page_icon="📊",
        layout="wide"
    )


def render_sidebar_filters(df):
    st.sidebar.title("HIGO analytics")
    st.sidebar.caption("Audience intelligence control panel")

    location_filter = st.sidebar.multiselect(
        "Tipe Lokasi",
        options=sorted(df["Tipe Lokasi"].unique()),
        default=sorted(df["Tipe Lokasi"].unique())
    )

    interest_filter = st.sidebar.multiselect(
        "Minat Digital",
        options=sorted(df["Minat Digital"].unique()),
        default=sorted(df["Minat Digital"].unique())
    )

    age_group_filter = st.sidebar.multiselect(
        "Kelompok Usia",
        options=sorted(df["Kelompok Usia"].unique()),
        default=sorted(df["Kelompok Usia"].unique())
    )

    phone_filter = st.sidebar.multiselect(
        "Merk HP",
        options=sorted(df["Merk HP"].unique()),
        default=sorted(df["Merk HP"].unique())
    )

    time_filter = st.sidebar.multiselect(
        "Time Segment",
        options=sorted(df["Time Segment"].unique()),
        default=sorted(df["Time Segment"].unique())
    )

    engagement_filter = st.sidebar.multiselect(
        "Engagement Level",
        options=sorted(df["Engagement Level"].unique()),
        default=sorted(df["Engagement Level"].unique())
    )

    filtered_df = apply_filters(
        df,
        location_filter,
        interest_filter,
        age_group_filter,
        phone_filter,
        time_filter,
        engagement_filter
    )

    return filtered_df


def render_kpi_cards(filtered_df):
    total_users = len(filtered_df)
    avg_age = filtered_df["Usia"].mean()
    avg_score = filtered_df["Digital Interest Score"].mean()

    top_location = filtered_df["Tipe Lokasi"].mode()[0] if not filtered_df.empty else "-"
    top_interest = filtered_df["Minat Digital"].mode()[0] if not filtered_df.empty else "-"

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Users", f"{total_users:,}")
    col2.metric("Avg Age", f"{avg_age:.1f}" if total_users > 0 else "-")
    col3.metric("Avg Interest Score", f"{avg_score:.1f}" if total_users > 0 else "-")
    col4.metric("Top Location", top_location)
    col5.metric("Top Interest", top_interest)


def render_footer():
    st.divider()
    st.caption(
        "Created as a dummy data analytics project for audience profiling, "
        "digital interest analysis, and location-based campaign insight."
    )