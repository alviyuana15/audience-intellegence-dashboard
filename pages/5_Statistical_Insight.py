import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from scipy import stats

from lib.loaders import load_user_data
from lib.ui import page_config, render_footer


page_config()

df = load_user_data()

st.sidebar.title("HIGO Analytics")
st.sidebar.caption("Statistical insight control panel")

location_filter = st.sidebar.multiselect(
    "Tipe Lokasi",
    options=sorted(df["Tipe Lokasi"].unique()),
    default=sorted(df["Tipe Lokasi"].unique())
)

age_filter = st.sidebar.multiselect(
    "Kelompok Usia",
    options=sorted(df["Kelompok Usia"].unique()),
    default=sorted(df["Kelompok Usia"].unique())
)

engagement_filter = st.sidebar.multiselect(
    "Engagement Level",
    options=sorted(df["Engagement Level"].unique()),
    default=sorted(df["Engagement Level"].unique())
)

filtered_df = df[
    (df["Tipe Lokasi"].isin(location_filter)) &
    (df["Kelompok Usia"].isin(age_filter)) &
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


st.markdown('<div class="page-title">Statistical Insight</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Confidence Interval · Distribution · Statistical Summary</div>',
    unsafe_allow_html=True
)


# =========================================================
# BASIC STATS
# =========================================================

score_data = filtered_df["Digital Interest Score"].dropna()

n = len(score_data)

mean_score = score_data.mean()
median_score = score_data.median()
std_score = score_data.std()
min_score = score_data.min()
max_score = score_data.max()

confidence = 0.95

ci_low, ci_high = stats.t.interval(
    confidence=confidence,
    df=n-1,
    loc=mean_score,
    scale=stats.sem(score_data)
)


# =========================================================
# KPI
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Mean Score</div>
        <div class="kpi-value">{mean_score:.1f}</div>
        <div class="kpi-note">rata-rata score audience</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#61DDAA;">
        <div class="kpi-label">Median Score</div>
        <div class="kpi-value">{median_score:.1f}</div>
        <div class="kpi-note">nilai tengah distribusi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#8D6FD1;">
        <div class="kpi-label">Std Deviation</div>
        <div class="kpi-value">{std_score:.1f}</div>
        <div class="kpi-note">tingkat variasi data</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#78D3F8;">
        <div class="kpi-label">Min Score</div>
        <div class="kpi-value">{min_score:.0f}</div>
        <div class="kpi-note">score terendah</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#9270CA;">
        <div class="kpi-label">Max Score</div>
        <div class="kpi-value">{max_score:.0f}</div>
        <div class="kpi-note">score tertinggi</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# INSIGHT CARDS
# =========================================================

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Distribution Pattern</div>
        <div class="insight-text">
            Mean score berada di angka <b>{mean_score:.1f}</b>,
            sementara median score berada di angka <b>{median_score:.1f}</b>.
            Selisih keduanya membantu membaca kecenderungan distribusi data.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Data Variability</div>
        <div class="insight-text">
            Standard deviation sebesar <b>{std_score:.1f}</b>
            menunjukkan tingkat penyebaran score audience terhadap rata-rata.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Confidence Interval</div>
        <div class="insight-text">
            Dengan confidence level 95%, rata-rata score diperkirakan berada
            pada rentang <b>{ci_low:.2f}</b> hingga <b>{ci_high:.2f}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# BREAKDOWN
# =========================================================

st.markdown('<div class="section-title">Statistical Breakdown</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Score Distribution",
    "Confidence Interval",
    "Score by Age Group",
    "Age Trend"
])


with tab1:
    st.subheader("Tren Distribusi Digital Interest Score")

    score_distribution = filtered_df.copy()

    score_distribution["Score Range"] = pd.cut(
        score_distribution["Digital Interest Score"],
        bins=[0, 45, 55, 65, 75, 85, 100],
        labels=["0-45", "46-55", "56-65", "66-75", "76-85", "86-100"],
        include_lowest=True
    )

    score_trend = (
        score_distribution
        .groupby("Score Range")
        .agg(
            Jumlah_User=("User ID", "count"),
            Rata_rata_Score=("Digital Interest Score", "mean")
        )
        .reset_index()
    )

    fig_score_trend = px.line(
        score_trend,
        x="Score Range",
        y="Rata_rata_Score",
        markers=True,
        title="Average Digital Interest Score by Score Range",
        color_discrete_sequence=["#5B8FF9"]
    )

    fig_score_trend.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=
        "<b>Score Range:</b> %{x}<br>" +
        "<b>Rata-rata Score:</b> %{y:.1f}<extra></extra>"
    )

    fig_score_trend.add_hline(
        y=mean_score,
        line_dash="dash",
        line_color="#FFB020",
        annotation_text=f"Overall Mean: {mean_score:.1f}",
        annotation_position="right"
    )

    fig_score_trend.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Score Range",
        yaxis_title="Rata-rata Digital Interest Score",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig_score_trend, use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Score Trend Interpretation</div>
        <div class="insight-text">
            Chart ini menunjukkan rata-rata digital interest score pada setiap rentang score.
            Garis kuning menunjukkan overall mean sebesar <b>{mean_score:.1f}</b>.
            Rentang score yang berada di atas garis mean dapat dianggap sebagai area audience
            dengan kualitas engagement relatif lebih tinggi.
        </div>
    </div>
    """, unsafe_allow_html=True)


with tab2:
    st.subheader("Confidence Interval Rata-rata Score")

    ci_width = ci_high - ci_low

    fig_ci = go.Figure()

    fig_ci.add_trace(go.Indicator(
        mode="number+gauge",
        value=mean_score,
        number={
            "suffix": "",
            "font": {"size": 46, "color": "white"}
        },
        title={
            "text": f"Mean Score<br><span style='font-size:0.75em;color:#A8B3CF'>95% CI: {ci_low:.2f} - {ci_high:.2f}</span>",
            "font": {"size": 20, "color": "white"}
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickcolor": "white"
            },
            "bar": {"color": "#5B8FF9"},
            "bgcolor": "#151B2D",
            "borderwidth": 1,
            "bordercolor": "#2A3655",
            "steps": [
                {"range": [0, 45], "color": "#1D2436"},
                {"range": [45, 75], "color": "#1F3A3A"},
                {"range": [75, 100], "color": "#1D3B59"}
            ],
            "threshold": {
                "line": {"color": "#FFB020", "width": 4},
                "thickness": 0.75,
                "value": mean_score
            }
        }
    ))

    fig_ci.update_layout(
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        height=420
    )

    st.plotly_chart(fig_ci, use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Interpretation</div>
        <div class="insight-text">
            Dengan tingkat kepercayaan 95%, rata-rata digital interest score audience
            diperkirakan berada di antara <b>{ci_low:.2f}</b> hingga <b>{ci_high:.2f}</b>.
            Semakin sempit interval, semakin stabil estimasi rata-ratanya.
        </div>
    </div>
    """, unsafe_allow_html=True)


with tab3:
    st.subheader("Rata-rata Score Berdasarkan Kelompok Usia")

    score_age_group = (
        filtered_df
        .groupby("Kelompok Usia")["Digital Interest Score"]
        .mean()
        .reset_index()
    )

    score_age_group.columns = ["Kelompok Usia", "Rata-rata Score"]

    score_age_group = score_age_group.sort_values(
        "Rata-rata Score",
        ascending=True
    )

    fig_age_group_score = px.bar(
        score_age_group,
        x="Rata-rata Score",
        y="Kelompok Usia",
        text=score_age_group["Rata-rata Score"].round(1),
        orientation="h",
        title="Average Digital Interest Score by Age Group",
        color="Kelompok Usia",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_age_group_score.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Kelompok Usia:</b> %{y}<br>" +
        "<b>Rata-rata Score:</b> %{x:.1f}<extra></extra>"
    )

    fig_age_group_score.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Rata-rata Score",
        yaxis_title="Kelompok Usia",
        xaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(fig_age_group_score, use_container_width=True)

    best_age_group = score_age_group.sort_values(
        "Rata-rata Score",
        ascending=False
    ).iloc[0]["Kelompok Usia"]

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Age Group Signal</div>
        <div class="insight-text">
            Kelompok usia dengan rata-rata score tertinggi adalah
            <b>{best_age_group}</b>. Segmen ini dapat diprioritaskan untuk
            campaign berbasis digital interest.
        </div>
    </div>
    """, unsafe_allow_html=True)


with tab4:
    st.subheader("Tren Rata-rata Score Berdasarkan Usia")

    age_trend = (
        filtered_df
        .groupby("Usia")["Digital Interest Score"]
        .mean()
        .reset_index()
    )

    age_trend.columns = ["Usia", "Rata-rata Score"]

    fig_age_trend = px.line(
        age_trend,
        x="Usia",
        y="Rata-rata Score",
        markers=True,
        title="Average Digital Interest Score by Age",
        color_discrete_sequence=["#5B8FF9"]
    )

    fig_age_trend.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate=
        "<b>Usia:</b> %{x}<br>" +
        "<b>Rata-rata Score:</b> %{y:.1f}<extra></extra>"
    )

    fig_age_trend.add_hline(
        y=mean_score,
        line_dash="dash",
        line_color="#FFB020",
        annotation_text=f"Overall Mean: {mean_score:.1f}"
    )

    fig_age_trend.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Usia",
        yaxis_title="Rata-rata Digital Interest Score",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig_age_trend, use_container_width=True)

    correlation = filtered_df["Usia"].corr(
        filtered_df["Digital Interest Score"]
    )

    if correlation < -0.2:
        relation_text = "terdapat kecenderungan score menurun ketika usia meningkat"
    elif correlation > 0.2:
        relation_text = "terdapat kecenderungan score meningkat ketika usia meningkat"
    else:
        relation_text = "hubungan usia dan score relatif lemah"

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Trend Interpretation</div>
        <div class="insight-text">
            Korelasi usia dan digital interest score adalah <b>{correlation:.2f}</b>,
            yang berarti {relation_text}. Visual ini lebih mudah dibaca dibanding scatter plot
            karena menampilkan rata-rata score per usia.
        </div>
    </div>
    """, unsafe_allow_html=True)


with st.expander("Lihat dataset statistical insight"):
    st.dataframe(filtered_df, use_container_width=True)

render_footer()