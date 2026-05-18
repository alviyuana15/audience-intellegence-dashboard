import streamlit as st
import plotly.express as px
import pandas as pd

from lib.loaders import load_user_data
from lib.ui import page_config, render_footer
from lib.utils import create_summary_count


page_config()

df = load_user_data()

st.sidebar.title("HIGO Analytics")
st.sidebar.caption("Location insight control panel")

location_type_filter = st.sidebar.multiselect(
    "Tipe Lokasi",
    options=sorted(df["Tipe Lokasi"].unique()),
    default=sorted(df["Tipe Lokasi"].unique())
)

location_name_filter = st.sidebar.multiselect(
    "Nama Lokasi",
    options=sorted(df["Nama Lokasi"].unique()),
    default=sorted(df["Nama Lokasi"].unique())
)

engagement_filter = st.sidebar.multiselect(
    "Engagement Level",
    options=sorted(df["Engagement Level"].unique()),
    default=sorted(df["Engagement Level"].unique())
)

filtered_df = df[
    (df["Tipe Lokasi"].isin(location_type_filter)) &
    (df["Nama Lokasi"].isin(location_name_filter)) &
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


st.markdown('<div class="page-title">Location Insight</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Location Performance · Audience Share · Campaign Opportunity</div>',
    unsafe_allow_html=True
)


total_audience = len(filtered_df)
unique_locations = filtered_df["Nama Lokasi"].nunique() if total_audience > 0 else 0
unique_location_types = filtered_df["Tipe Lokasi"].nunique() if total_audience > 0 else 0
top_location_name = filtered_df["Nama Lokasi"].mode()[0] if total_audience > 0 else "-"
top_location_type = filtered_df["Tipe Lokasi"].mode()[0] if total_audience > 0 else "-"
avg_score = filtered_df["Digital Interest Score"].mean() if total_audience > 0 else 0

location_name_summary = create_summary_count(filtered_df, "Nama Lokasi")
location_type_summary = create_summary_count(filtered_df, "Tipe Lokasi")

location_perf = (
    filtered_df
    .groupby(["Tipe Lokasi", "Nama Lokasi"])
    .agg(
        Jumlah_User=("User ID", "count"),
        Avg_Score=("Digital Interest Score", "mean"),
        High_Engagement_User=("Engagement Level", lambda x: (x == "High").sum())
    )
    .reset_index()
)

best_location_by_score = "-"
best_location_score = 0

if not location_perf.empty:
    best_score_row = location_perf.sort_values("Avg_Score", ascending=False).iloc[0]
    best_location_by_score = best_score_row["Nama Lokasi"]
    best_location_score = best_score_row["Avg_Score"]

high_engagement_location = "-"

if not location_perf.empty:
    high_row = location_perf.sort_values("High_Engagement_User", ascending=False).iloc[0]
    high_engagement_location = high_row["Nama Lokasi"]


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Audience</div>
        <div class="kpi-value">{total_audience:,}</div>
        <div class="kpi-note">audience pada lokasi terfilter</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#61DDAA;">
        <div class="kpi-label">Unique Locations</div>
        <div class="kpi-value">{unique_locations}</div>
        <div class="kpi-note">jumlah lokasi aktif</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#8D6FD1;">
        <div class="kpi-label">Location Types</div>
        <div class="kpi-value">{unique_location_types}</div>
        <div class="kpi-note">kategori lokasi aktif</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#78D3F8;">
        <div class="kpi-label">Top Location</div>
        <div class="kpi-value" style="font-size:23px;">{top_location_name}</div>
        <div class="kpi-note">lokasi dengan audience terbanyak</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#9270CA;">
        <div class="kpi-label">Avg Score</div>
        <div class="kpi-value">{avg_score:.1f}</div>
        <div class="kpi-note">rata-rata score lokasi</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


top_location_count = (
    location_name_summary.iloc[0]["Jumlah User"]
    if location_name_summary is not None and not location_name_summary.empty
    else 0
)

top_location_share = (
    top_location_count / total_audience * 100
    if total_audience > 0 else 0
)

top_type_count = (
    location_type_summary.iloc[0]["Jumlah User"]
    if location_type_summary is not None and not location_type_summary.empty
    else 0
)

top_type_share = (
    top_type_count / total_audience * 100
    if total_audience > 0 else 0
)


insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Location Concentration</div>
        <div class="insight-text">
            <b>{top_location_name}</b> menjadi lokasi dengan audience terbesar,
            berkontribusi sekitar {top_location_share:.1f}% dari data terfilter.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Location Type Signal</div>
        <div class="insight-text">
            <b>{top_location_type}</b> menjadi tipe lokasi paling dominan,
            mencakup sekitar {top_type_share:.1f}% dari audience.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Activation Priority</div>
        <div class="insight-text">
            <b>{best_location_by_score}</b> memiliki rata-rata score tertinggi
            sebesar {best_location_score:.1f}, potensial untuk aktivasi campaign.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="section-title">Location Breakdown</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Top Location Ranking",
    "Location Share",
    "Score Contribution",
    "Location Portfolio"
])


with tab1:
    st.subheader("Ranking Lokasi Berdasarkan Jumlah Audience")

    location_ranking = location_name_summary.sort_values(
        "Jumlah User",
        ascending=True
    )

    fig_location_ranking = px.bar(
        location_ranking,
        x="Jumlah User",
        y="Nama Lokasi",
        text="Jumlah User",
        orientation="h",
        title="Top Location Ranking by Audience Size",
        color="Nama Lokasi",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_location_ranking.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Nama Lokasi:</b> %{y}<br>" +
        "<b>Jumlah User:</b> %{x}<extra></extra>"
    )

    fig_location_ranking.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Jumlah User",
        yaxis_title="Nama Lokasi",
        showlegend=False,
        height=720
    )

    st.plotly_chart(fig_location_ranking, use_container_width=True)


with tab2:
    st.subheader("Share Audience Berdasarkan Tipe Lokasi")

    fig_location_share = px.pie(
        location_type_summary,
        names="Tipe Lokasi",
        values="Jumlah User",
        title="Audience Share by Location Type",
        hole=0.45,
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_location_share.update_traces(
        textinfo="percent+label",
        hovertemplate=
        "<b>Tipe Lokasi:</b> %{label}<br>" +
        "<b>Jumlah User:</b> %{value}<br>" +
        "<b>Share:</b> %{percent}<extra></extra>"
    )

    fig_location_share.update_layout(
        paper_bgcolor="#050B14",
        font_color="#FFFFFF"
    )

    st.plotly_chart(fig_location_share, use_container_width=True)


with tab3:
    st.subheader("Kontribusi Total Digital Interest Score Berdasarkan Tipe Lokasi")

    score_contribution = (
        filtered_df
        .groupby("Tipe Lokasi")["Digital Interest Score"]
        .sum()
        .reset_index()
    )

    score_contribution.columns = ["Tipe Lokasi", "Total Interest Score"]

    score_contribution = score_contribution.sort_values(
        "Total Interest Score",
        ascending=True
    )

    fig_score_contribution = px.bar(
        score_contribution,
        x="Total Interest Score",
        y="Tipe Lokasi",
        text="Total Interest Score",
        orientation="h",
        title="Total Interest Score Contribution by Location Type",
        color="Tipe Lokasi",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_score_contribution.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Tipe Lokasi:</b> %{y}<br>" +
        "<b>Total Interest Score:</b> %{x:.0f}<extra></extra>"
    )

    fig_score_contribution.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Total Interest Score",
        yaxis_title="Tipe Lokasi",
        showlegend=False
    )

    st.plotly_chart(fig_score_contribution, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">Interpretation</div>
        <div class="insight-text">
            Visualisasi ini menunjukkan kontribusi total digital interest score
            dari setiap tipe lokasi. Semakin tinggi total score, semakin besar
            potensi lokasi tersebut dalam menghasilkan audience dengan ketertarikan digital tinggi.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.subheader("Location Portfolio View")

    portfolio_df = (
        filtered_df
        .groupby(["Tipe Lokasi", "Nama Lokasi"])
        .agg(
            Jumlah_User=("User ID", "count"),
            Avg_Score=("Digital Interest Score", "mean")
        )
        .reset_index()
    )

    fig_treemap = px.treemap(
        portfolio_df,
        path=["Tipe Lokasi", "Nama Lokasi"],
        values="Jumlah_User",
        color="Avg_Score",
        color_continuous_scale=[
            "#08101E",
            "#12273C",
            "#1D3B59",
            "#5B8FF9"
        ],
        title="Location Portfolio berdasarkan Audience Size dan Average Score"
    )

    fig_treemap.update_traces(
        hovertemplate=
        "<b>Lokasi:</b> %{label}<br>" +
        "<b>Jumlah User:</b> %{value}<br>" +
        "<b>Avg Score:</b> %{color:.1f}<extra></extra>"
    )

    fig_treemap.update_layout(
        paper_bgcolor="#050B14",
        font_color="#FFFFFF"
    )

    st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown('<div class="section-title">Location-Based Campaign Recommendation</div>', unsafe_allow_html=True)

    rec1, rec2, rec3 = st.columns(3)

    with rec1:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">Commercial Area</div>
            <div class="insight-text">
                Mall dan cafe dapat digunakan untuk campaign berbasis shopping,
                food, entertainment, dan lifestyle.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rec2:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">Productive Area</div>
            <div class="insight-text">
                Office tower cocok untuk campaign finance, productivity,
                professional service, dan technology.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rec3:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">Mobility Area</div>
            <div class="insight-text">
                Transport hub cocok untuk campaign travel, news, food,
                quick promo, dan awareness message.
            </div>
        </div>
        """, unsafe_allow_html=True)


with st.expander("Lihat dataset location insight"):
    st.dataframe(filtered_df, use_container_width=True)

render_footer()                   