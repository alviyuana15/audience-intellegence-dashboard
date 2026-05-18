import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats

# PAGE CONFIG

st.set_page_config(
    page_title="HIGO Audience Profiling Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA

@st.cache_data
def load_data():
    df = pd.read_csv("dummy_higo_user_data.csv")

    if "Tanggal Login" in df.columns:
        df["Tanggal Login"] = pd.to_datetime(df["Tanggal Login"])

    return df


df = load_data()

# SIDEBAR

st.sidebar.title("🔎 Dashboard Filter")
st.sidebar.write("Gunakan filter berikut untuk mengeksplor data pengguna.")

location_filter = st.sidebar.multiselect(
    "Pilih Tipe Lokasi",
    options=sorted(df["Tipe Lokasi"].unique()),
    default=sorted(df["Tipe Lokasi"].unique())
)

interest_filter = st.sidebar.multiselect(
    "Pilih Minat Digital",
    options=sorted(df["Minat Digital"].unique()),
    default=sorted(df["Minat Digital"].unique())
)

age_group_filter = st.sidebar.multiselect(
    "Pilih Kelompok Usia",
    options=sorted(df["Kelompok Usia"].unique()),
    default=sorted(df["Kelompok Usia"].unique())
)

phone_filter = st.sidebar.multiselect(
    "Pilih Merk HP",
    options=sorted(df["Merk HP"].unique()),
    default=sorted(df["Merk HP"].unique())
)

time_filter = st.sidebar.multiselect(
    "Pilih Time Segment",
    options=sorted(df["Time Segment"].unique()),
    default=sorted(df["Time Segment"].unique())
)

# APPLY FILTER

filtered_df = df[
    (df["Tipe Lokasi"].isin(location_filter)) &
    (df["Minat Digital"].isin(interest_filter)) &
    (df["Kelompok Usia"].isin(age_group_filter)) &
    (df["Merk HP"].isin(phone_filter)) &
    (df["Time Segment"].isin(time_filter))
]

# HEADER

st.title("📊 HIGO Audience Profiling & Digital Interest Dashboard")

st.markdown("""
Dashboard ini menggunakan data dummy untuk mensimulasikan pengguna digital touchpoint berbasis lokasi.  
Analisis berfokus pada profil pengguna, tipe lokasi, waktu login, perangkat, minat digital, engagement level, dan estimasi statistik.
""")

# KPI CARDS

total_users = len(filtered_df)
avg_age = filtered_df["Usia"].mean()
avg_score = filtered_df["Digital Interest Score"].mean()
top_location = filtered_df["Tipe Lokasi"].mode()[0] if not filtered_df.empty else "-"
top_interest = filtered_df["Minat Digital"].mode()[0] if not filtered_df.empty else "-"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Avg Age", f"{avg_age:.1f}" if not np.isnan(avg_age) else "-")
col3.metric("Avg Interest Score", f"{avg_score:.1f}" if not np.isnan(avg_score) else "-")
col4.metric("Top Location Type", top_location)
col5.metric("Top Interest", top_interest)


st.divider()

# DATA PREVIEW

with st.expander("📄 Lihat Preview Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# CHART 1: USERS BY LOCATION TYPE

st.subheader("1. Distribusi User Berdasarkan Tipe Lokasi")

location_summary = (
    filtered_df["Tipe Lokasi"]
    .value_counts()
    .reset_index()
)

location_summary.columns = ["Tipe Lokasi", "Jumlah User"]

fig_location = px.bar(
    location_summary,
    x="Tipe Lokasi",
    y="Jumlah User",
    text="Jumlah User",
    title="Jumlah User per Tipe Lokasi"
)

fig_location.update_traces(textposition="outside")
fig_location.update_layout(xaxis_title="Tipe Lokasi", yaxis_title="Jumlah User")

st.plotly_chart(fig_location, use_container_width=True)

# CHART 2: AGE DISTRIBUTION

st.subheader("2. Distribusi Usia Pengguna")

fig_age = px.histogram(
    filtered_df,
    x="Usia",
    nbins=20,
    title="Distribusi Usia Pengguna",
    marginal="box"
)

fig_age.update_layout(xaxis_title="Usia", yaxis_title="Jumlah User")

st.plotly_chart(fig_age, use_container_width=True)

# CHART 3: AGE GROUP

st.subheader("3. Distribusi Kelompok Usia")

age_group_summary = (
    filtered_df["Kelompok Usia"]
    .value_counts()
    .reset_index()
)

age_group_summary.columns = ["Kelompok Usia", "Jumlah User"]

fig_age_group = px.pie(
    age_group_summary,
    names="Kelompok Usia",
    values="Jumlah User",
    title="Proporsi Kelompok Usia"
)

st.plotly_chart(fig_age_group, use_container_width=True)

# CHART 4: LOGIN TIME SEGMENT

st.subheader("4. Pola Login Berdasarkan Time Segment")

time_summary = (
    filtered_df["Time Segment"]
    .value_counts()
    .reset_index()
)

time_summary.columns = ["Time Segment", "Jumlah User"]

fig_time = px.bar(
    time_summary,
    x="Time Segment",
    y="Jumlah User",
    text="Jumlah User",
    title="Jumlah Login Berdasarkan Time Segment"
)

fig_time.update_traces(textposition="outside")
fig_time.update_layout(xaxis_title="Time Segment", yaxis_title="Jumlah User")

st.plotly_chart(fig_time, use_container_width=True)

# CHART 5: PHONE BRAND

st.subheader("5. Distribusi Merk HP")

phone_summary = (
    filtered_df["Merk HP"]
    .value_counts()
    .reset_index()
)

phone_summary.columns = ["Merk HP", "Jumlah User"]

fig_phone = px.bar(
    phone_summary,
    x="Merk HP",
    y="Jumlah User",
    text="Jumlah User",
    title="Merk HP yang Digunakan Pengguna"
)

fig_phone.update_traces(textposition="outside")
fig_phone.update_layout(xaxis_title="Merk HP", yaxis_title="Jumlah User")

st.plotly_chart(fig_phone, use_container_width=True)

# CHART 6: DIGITAL INTEREST

st.subheader("6. Distribusi Minat Digital")

interest_summary = (
    filtered_df["Minat Digital"]
    .value_counts()
    .reset_index()
)

interest_summary.columns = ["Minat Digital", "Jumlah User"]

fig_interest = px.bar(
    interest_summary,
    x="Minat Digital",
    y="Jumlah User",
    text="Jumlah User",
    title="Minat Digital Pengguna"
)

fig_interest.update_traces(textposition="outside")
fig_interest.update_layout(
    xaxis_title="Minat Digital",
    yaxis_title="Jumlah User"
)

st.plotly_chart(fig_interest, use_container_width=True)

# CHART 7: ENGAGEMENT LEVEL

st.subheader("7. Distribusi Engagement Level")

engagement_summary = (
    filtered_df["Engagement Level"]
    .value_counts()
    .reset_index()
)

engagement_summary.columns = ["Engagement Level", "Jumlah User"]

fig_engagement = px.bar(
    engagement_summary,
    x="Engagement Level",
    y="Jumlah User",
    text="Jumlah User",
    title="Engagement Level Pengguna"
)

fig_engagement.update_traces(textposition="outside")
fig_engagement.update_layout(
    xaxis_title="Engagement Level",
    yaxis_title="Jumlah User"
)

st.plotly_chart(fig_engagement, use_container_width=True)

# CHART 8: HEATMAP INTEREST VS LOCATION

st.subheader("8. Heatmap Minat Digital Berdasarkan Tipe Lokasi")

heatmap_data = pd.crosstab(
    filtered_df["Tipe Lokasi"],
    filtered_df["Minat Digital"]
)

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Heatmap Minat Digital vs Tipe Lokasi"
)

fig_heatmap.update_layout(
    xaxis_title="Minat Digital",
    yaxis_title="Tipe Lokasi"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# CHART 9: AVG SCORE BY LOCATION

st.subheader("9. Rata-rata Digital Interest Score per Tipe Lokasi")

score_location = (
    filtered_df
    .groupby("Tipe Lokasi")["Digital Interest Score"]
    .mean()
    .reset_index()
)

score_location.columns = ["Tipe Lokasi", "Rata-rata Digital Interest Score"]

fig_score_location = px.bar(
    score_location,
    x="Tipe Lokasi",
    y="Rata-rata Digital Interest Score",
    text=score_location["Rata-rata Digital Interest Score"].round(1),
    title="Rata-rata Digital Interest Score Berdasarkan Tipe Lokasi"
)

fig_score_location.update_traces(textposition="outside")
fig_score_location.update_layout(
    xaxis_title="Tipe Lokasi",
    yaxis_title="Rata-rata Score",
    yaxis_range=[0, 100]
)

st.plotly_chart(fig_score_location, use_container_width=True)

# CHART 10: AUDIENCE SEGMENT

st.subheader("10. Audience Segment")

segment_summary = (
    filtered_df["Audience Segment"]
    .value_counts()
    .reset_index()
)

segment_summary.columns = ["Audience Segment", "Jumlah User"]

fig_segment = px.bar(
    segment_summary,
    x="Audience Segment",
    y="Jumlah User",
    text="Jumlah User",
    title="Distribusi Audience Segment"
)

fig_segment.update_traces(textposition="outside")
fig_segment.update_layout(
    xaxis_title="Audience Segment",
    yaxis_title="Jumlah User"
)

st.plotly_chart(fig_segment, use_container_width=True)

# CONFIDENCE INTERVAL

st.divider()
st.header("📌 Confidence Interval Analysis")

st.markdown("""
Bagian ini menghitung **95% Confidence Interval** untuk rata-rata usia pengguna.
Tujuannya adalah memperkirakan rentang nilai rata-rata usia populasi berdasarkan data sampel dummy.
""")

age_data = filtered_df["Usia"].dropna()

if len(age_data) > 1:
    n = len(age_data)
    mean_age = np.mean(age_data)
    std_age = np.std(age_data, ddof=1)

    confidence_level = 0.95
    alpha = 1 - confidence_level

    t_critical = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin_error = t_critical * (std_age / np.sqrt(n))

    ci_lower = mean_age - margin_error
    ci_upper = mean_age + margin_error

    col_ci1, col_ci2, col_ci3, col_ci4 = st.columns(4)

    col_ci1.metric("Sample Size", f"{n:,}")
    col_ci2.metric("Mean Age", f"{mean_age:.2f}")
    col_ci3.metric("CI Lower Bound", f"{ci_lower:.2f}")
    col_ci4.metric("CI Upper Bound", f"{ci_upper:.2f}")

    ci_df = pd.DataFrame({
        "Metric": ["Mean Age"],
        "Mean": [mean_age],
        "Lower Bound": [ci_lower],
        "Upper Bound": [ci_upper]
    })

    fig_ci = px.scatter(
        ci_df,
        x="Metric",
        y="Mean",
        error_y=ci_df["Upper Bound"] - ci_df["Mean"],
        error_y_minus=ci_df["Mean"] - ci_df["Lower Bound"],
        title="95% Confidence Interval Rata-rata Usia"
    )

    fig_ci.update_layout(
        yaxis_title="Usia",
        xaxis_title=""
    )

    st.plotly_chart(fig_ci, use_container_width=True)

    st.success(
        f"Rata-rata usia pengguna adalah {mean_age:.2f} tahun. "
        f"Dengan 95% confidence interval, rata-rata usia diperkirakan berada "
        f"di antara {ci_lower:.2f} hingga {ci_upper:.2f} tahun."
    )

else:
    st.warning("Data tidak cukup untuk menghitung confidence interval.")

# KEY INSIGHTS

st.divider()
st.header("💡 Key Insights")

if not filtered_df.empty:
    top_location_type = filtered_df["Tipe Lokasi"].value_counts().idxmax()
    top_interest = filtered_df["Minat Digital"].value_counts().idxmax()
    top_phone = filtered_df["Merk HP"].value_counts().idxmax()
    top_time_segment = filtered_df["Time Segment"].value_counts().idxmax()
    top_age_group = filtered_df["Kelompok Usia"].value_counts().idxmax()
    top_segment = filtered_df["Audience Segment"].value_counts().idxmax()

    st.markdown(f"""
    Berdasarkan data yang sudah difilter:

    1. Tipe lokasi dengan jumlah user terbanyak adalah **{top_location_type}**.
    2. Minat digital paling dominan adalah **{top_interest}**.
    3. Merk HP yang paling banyak digunakan adalah **{top_phone}**.
    4. Login paling banyak terjadi pada segmen waktu **{top_time_segment}**.
    5. Kelompok usia paling dominan adalah **{top_age_group}**.
    6. Audience segment terbesar adalah **{top_segment}**.
    """)

else:
    st.warning("Tidak ada data yang sesuai dengan filter.")

# BUSINESS RECOMMENDATIONS

st.divider()
st.header("🚀 Business Recommendations")

st.markdown("""
1. **Mall** cocok untuk campaign bertema Shopping, Food, dan Entertainment.
2. **Campus** cocok untuk campaign Education, Gaming, Technology, dan produk Gen Z.
3. **Office Tower** cocok untuk campaign Finance, Productivity, Professional Service, dan Technology.
4. **Transport Hub** cocok untuk campaign Travel, News, Food, dan promo cepat.
5. Segmentasi audience dapat digunakan untuk membuat campaign yang lebih personal dan relevan.
6. Jam login tertinggi dapat menjadi acuan untuk menentukan waktu terbaik menjalankan campaign.
7. High engagement users dapat diprioritaskan sebagai target utama untuk campaign digital performance.
""")

# DOWNLOAD FILTERED DATA

st.divider()
st.header("⬇️ Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_higo_user_data.csv",
    mime="text/csv"
)

# FOOTER

st.caption(
    "Created as a dummy data analytics project for audience profiling, digital interest analysis, and location-based campaign insight."
)