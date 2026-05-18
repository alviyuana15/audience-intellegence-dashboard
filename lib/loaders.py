import pandas as pd
import streamlit as st


@st.cache_data
def load_user_data():
    df = pd.read_csv("data/dummy_higo_user_data.csv")

    if "Tanggal Login" in df.columns:
        df["Tanggal Login"] = pd.to_datetime(df["Tanggal Login"])

    return df


@st.cache_data
def load_summary_table(sheet_name):
    return pd.read_excel(
        "data/higo_summary_tables.xlsx",
        sheet_name=sheet_name
    )