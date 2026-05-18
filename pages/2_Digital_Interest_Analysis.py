import streamlit as st
import plotly.express as px
import pandas as pd

from lib.loaders import load_user_data
from lib.ui import page_config, render_footer
from lib.utils import create_summary_count, create_average_summary


page_config()

df = load_user_data()

st.sidebar.title("HIGO Analytics")
st.sidebar.caption("Digital interest control panel")

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

engagement_filter = st.sidebar.multiselect(
    "Engagement Level",
    options=sorted(df["Engagement Level"].unique()),
    default=sorted(df["Engagement Level"].unique())
)

filtered_df = df[
    (df["Tipe Lokasi"].isin(location_filter)) &
    (df["Minat Digital"].isin(interest_filter)) &
    (df["Engagement Level"].isin(engagement_filter))
]


COLOR_PALETTE = [
    "#5B8FF9",
    "#61DDAA",
    "#65789B",
    "#8D6FD1",
    "#78D3F8",
    "#9661BC",
    "#5D7092",
    "#6DC8EC",
    "#9270CA",
    "#7C99AC"
]


st.markdown("""
<style>
.page-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 14px;
    letter-spacing: 3px;
    color: #8FAADC;
    text-transform: uppercase;
    margin-bottom: 34px;
}

.kpi-card {
    background-color: #151B2D;
    border: 1px solid #2A3655;
    border-radius: 16px;
    padding: 24px 26px;
    min-height: 155px;
    border-top: 4px solid #5B8FF9;
}

.kpi-label {
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8FAADC;
    font-weight: 700;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 34px;
    color: #FFFFFF;
    font-weight: 800;
    margin-bottom: 8px;
}

.kpi-note {
    font-size: 14px;
    color: #A8B3CF;
}

.insight-card {
    background-color: #151B2D;
    border: 1px solid #2A3655;
    border-radius: 16px;
    padding: 22px 24px;
    min-height: 125px;
}

.insight-title {
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8FAADC;
    font-weight: 700;
    margin-bottom: 14px;
}

.insight-text {
    font-size: 16px;
    color: #FFFFFF;
    line-height: 1.6;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 30px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="page-title">Digital Interest Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Interest Category · Score Performance · Location Relationship</div>',
    unsafe_allow_html=True
)


total_audience = len(filtered_df)
avg_score = filtered_df["Digital Interest Score"].mean() if total_audience > 0 else 0
top_interest = filtered_df["Minat Digital"].mode()[0] if total_audience > 0 else "-"
interest_categories = filtered_df["Minat Digital"].nunique() if total_audience > 0 else 0
top_engagement = filtered_df["Engagement Level"].mode()[0] if total_audience > 0 else "-"

interest_summary = create_summary_count(filtered_df, "Minat Digital")
score_interest = create_average_summary(
    filtered_df,
    "Minat Digital",
    "Digital Interest Score"
)

highest_score_interest = "-"
highest_score_value = 0

if score_interest is not None and not score_interest.empty:
    highest_row = score_interest.sort_values(
        "Rata-rata Digital Interest Score",
        ascending=False
    ).iloc[0]

    highest_score_interest = highest_row["Minat Digital"]
    highest_score_value = highest_row["Rata-rata Digital Interest Score"]


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Top Interest</div>
        <div class="kpi-value" style="font-size:28px;">{top_interest}</div>
        <div class="kpi-note">kategori minat paling dominan</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#61DDAA;">
        <div class="kpi-label">Avg Score</div>
        <div class="kpi-value">{avg_score:.1f}</div>
        <div class="kpi-note">rata-rata digital interest score</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#8D6FD1;">
        <div class="kpi-label">Highest Score</div>
        <div class="kpi-value" style="font-size:26px;">{highest_score_interest}</div>
        <div class="kpi-note">{highest_score_value:.1f} average score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#78D3F8;">
        <div class="kpi-label">Categories</div>
        <div class="kpi-value">{interest_categories}</div>
        <div class="kpi-note">kategori interest aktif</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#9270CA;">
        <div class="kpi-label">Top Engagement</div>
        <div class="kpi-value" style="font-size:28px;">{top_engagement}</div>
        <div class="kpi-note">level engagement dominan</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


top_interest_count = (
    interest_summary.iloc[0]["Jumlah User"]
    if interest_summary is not None and not interest_summary.empty
    else 0
)

top_interest_share = (
    top_interest_count / total_audience * 100
    if total_audience > 0 else 0
)

high_engagement_count = (
    (filtered_df["Engagement Level"] == "High").sum()
    if total_audience > 0 else 0
)

high_engagement_share = (
    high_engagement_count / total_audience * 100
    if total_audience > 0 else 0
)

top_location_for_interest = "-"

if total_audience > 0:
    top_location_for_interest = (
        filtered_df.groupby("Tipe Lokasi")["Digital Interest Score"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )


insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Interest Concentration</div>
        <div class="insight-text">
            <b>{top_interest}</b> menjadi minat digital dominan dengan kontribusi
            sekitar {top_interest_share:.1f}% dari audience terfilter.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Engagement Quality</div>
        <div class="insight-text">
            {high_engagement_share:.1f}% audience berada pada kategori
            <b>High Engagement</b>, yang dapat diprioritaskan untuk campaign performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Location Opportunity</div>
        <div class="insight-text">
            <b>{top_location_for_interest}</b> memiliki rata-rata score tertinggi,
            sehingga potensial untuk aktivasi campaign berbasis minat digital.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="section-title">Digital Interest Breakdown</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Interest Ranking",
    "Score by Interest",
    "Interest by Location",
    "Score Distribution"
])


with tab1:
    st.subheader("Ranking Minat Digital")

    interest_summary_sorted = interest_summary.sort_values(
        "Jumlah User",
        ascending=True
    )

    fig_interest = px.bar(
        interest_summary_sorted,
        x="Jumlah User",
        y="Minat Digital",
        text="Jumlah User",
        title="Ranking Minat Digital Berdasarkan Jumlah User",
        orientation="h",
        color="Minat Digital",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_interest.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Minat Digital:</b> %{y}<br>" +
        "<b>Jumlah User:</b> %{x}<extra></extra>"
    )

    fig_interest.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Jumlah User",
        yaxis_title="Minat Digital",
        showlegend=False
    )

    st.plotly_chart(fig_interest, use_container_width=True)


with tab2:
    st.subheader("Rata-rata Digital Interest Score per Kategori")

    score_interest_sorted = score_interest.sort_values(
        "Rata-rata Digital Interest Score",
        ascending=False
    )

    fig_score_interest = px.bar(
        score_interest_sorted,
        x="Minat Digital",
        y="Rata-rata Digital Interest Score",
        text=score_interest_sorted["Rata-rata Digital Interest Score"].round(1),
        title="Average Digital Interest Score by Interest Category",
        color="Minat Digital",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_score_interest.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Minat Digital:</b> %{x}<br>" +
        "<b>Rata-rata Score:</b> %{y:.1f}<extra></extra>"
    )

    fig_score_interest.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Minat Digital",
        yaxis_title="Rata-rata Score",
        yaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_score_interest, use_container_width=True)


with tab3:
    st.subheader("Heatmap Minat Digital Berdasarkan Tipe Lokasi")

    heatmap_data = pd.crosstab(
        filtered_df["Tipe Lokasi"],
        filtered_df["Minat Digital"]
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        title="Heatmap Minat Digital vs Tipe Lokasi",
        color_continuous_scale=[
            "#08101E",
            "#12273C",
            "#1D3B59",
            "#5B8FF9"
        ]
    )

    fig_heatmap.update_traces(
        hovertemplate=
        "<b>Tipe Lokasi:</b> %{y}<br>" +
        "<b>Minat Digital:</b> %{x}<br>" +
        "<b>Jumlah User:</b> %{z}<extra></extra>"
    )

    fig_heatmap.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Minat Digital",
        yaxis_title="Tipe Lokasi"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)


with tab4:
    st.subheader("Distribusi Score Berdasarkan Minat Digital")

    fig_box = px.box(
        filtered_df,
        x="Digital Interest Score",
        y="Minat Digital",
        color="Minat Digital",
        title="Distribusi Digital Interest Score per Minat Digital",
        color_discrete_sequence=COLOR_PALETTE,
        orientation="h"
    )

    fig_box.update_traces(
        hovertemplate=
        "<b>Minat Digital:</b> %{y}<br>" +
        "<b>Score:</b> %{x}<extra></extra>"
    )

    fig_box.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Digital Interest Score",
        yaxis_title="Minat Digital",
        xaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_box, use_container_width=True)


with st.expander("Lihat dataset digital interest"):
    st.dataframe(filtered_df, use_container_width=True)

render_footer()