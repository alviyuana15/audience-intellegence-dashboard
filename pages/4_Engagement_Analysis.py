import streamlit as st
import plotly.express as px
import pandas as pd

from lib.loaders import load_user_data
from lib.ui import page_config, render_footer
from lib.utils import create_summary_count


page_config()

df = load_user_data()

st.sidebar.title("HIGO Analytics")
st.sidebar.caption("Engagement analysis control panel")

engagement_filter = st.sidebar.multiselect(
    "Engagement Level",
    options=sorted(df["Engagement Level"].unique()),
    default=sorted(df["Engagement Level"].unique())
)

interest_filter = st.sidebar.multiselect(
    "Minat Digital",
    options=sorted(df["Minat Digital"].unique()),
    default=sorted(df["Minat Digital"].unique())
)

segment_filter = st.sidebar.multiselect(
    "Audience Segment",
    options=sorted(df["Audience Segment"].unique()),
    default=sorted(df["Audience Segment"].unique())
)

location_filter = st.sidebar.multiselect(
    "Tipe Lokasi",
    options=sorted(df["Tipe Lokasi"].unique()),
    default=sorted(df["Tipe Lokasi"].unique())
)

filtered_df = df[
    (df["Engagement Level"].isin(engagement_filter)) &
    (df["Minat Digital"].isin(interest_filter)) &
    (df["Audience Segment"].isin(segment_filter)) &
    (df["Tipe Lokasi"].isin(location_filter))
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


st.markdown('<div class="page-title">Engagement Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Engagement Level · Audience Segment · Score Quality</div>',
    unsafe_allow_html=True
)


total_audience = len(filtered_df)
avg_score = filtered_df["Digital Interest Score"].mean() if total_audience > 0 else 0
median_score = filtered_df["Digital Interest Score"].median() if total_audience > 0 else 0
top_engagement = filtered_df["Engagement Level"].mode()[0] if total_audience > 0 else "-"
top_segment = filtered_df["Audience Segment"].mode()[0] if total_audience > 0 else "-"
high_users = (filtered_df["Engagement Level"] == "High").sum() if total_audience > 0 else 0
high_rate = high_users / total_audience * 100 if total_audience > 0 else 0

engagement_summary = create_summary_count(filtered_df, "Engagement Level")
segment_summary = create_summary_count(filtered_df, "Audience Segment")

score_segment = (
    filtered_df
    .groupby("Audience Segment")["Digital Interest Score"]
    .mean()
    .reset_index()
)

score_segment.columns = ["Audience Segment", "Rata-rata Digital Interest Score"]

best_segment = "-"
best_segment_score = 0

if not score_segment.empty:
    best_segment_row = score_segment.sort_values(
        "Rata-rata Digital Interest Score",
        ascending=False
    ).iloc[0]

    best_segment = best_segment_row["Audience Segment"]
    best_segment_score = best_segment_row["Rata-rata Digital Interest Score"]


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">High Users</div>
        <div class="kpi-value">{high_users:,}</div>
        <div class="kpi-note">audience kategori high engagement</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#61DDAA;">
        <div class="kpi-label">High Rate</div>
        <div class="kpi-value">{high_rate:.1f}%</div>
        <div class="kpi-note">proporsi high engagement</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#8D6FD1;">
        <div class="kpi-label">Avg Score</div>
        <div class="kpi-value">{avg_score:.1f}</div>
        <div class="kpi-note">rata-rata digital interest score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#78D3F8;">
        <div class="kpi-label">Top Level</div>
        <div class="kpi-value" style="font-size:28px;">{top_engagement}</div>
        <div class="kpi-note">engagement level dominan</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#9270CA;">
        <div class="kpi-label">Top Segment</div>
        <div class="kpi-value" style="font-size:23px;">{top_segment}</div>
        <div class="kpi-note">segmen audience dominan</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


medium_users = (filtered_df["Engagement Level"] == "Medium").sum() if total_audience > 0 else 0
medium_rate = medium_users / total_audience * 100 if total_audience > 0 else 0

low_users = (filtered_df["Engagement Level"] == "Low").sum() if total_audience > 0 else 0
low_rate = low_users / total_audience * 100 if total_audience > 0 else 0

top_interest_high = "-"

if total_audience > 0:
    high_df = filtered_df[filtered_df["Engagement Level"] == "High"]
    if not high_df.empty:
        top_interest_high = high_df["Minat Digital"].mode()[0]


insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Engagement Quality</div>
        <div class="insight-text">
            {high_rate:.1f}% audience berada pada kategori <b>High Engagement</b>,
            menunjukkan potensi kuat untuk campaign performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Dominant Segment</div>
        <div class="insight-text">
            <b>{top_segment}</b> menjadi audience segment terbesar,
            sehingga dapat menjadi prioritas awal dalam targeting.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">High Intent Signal</div>
        <div class="insight-text">
            Pada kategori high engagement, minat digital yang paling dominan adalah
            <b>{top_interest_high}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="section-title">Engagement Breakdown</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Engagement Level",
    "Score Distribution",
    "Segment Performance",
    "Engagement Matrix"
])


with tab1:
    st.subheader("Distribusi Engagement Level")

    fig_engagement = px.pie(
        engagement_summary,
        names="Engagement Level",
        values="Jumlah User",
        title="Engagement Level Share",
        hole=0.45,
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_engagement.update_traces(
        textinfo="percent+label",
        hovertemplate=
        "<b>Engagement Level:</b> %{label}<br>" +
        "<b>Jumlah User:</b> %{value}<br>" +
        "<b>Share:</b> %{percent}<extra></extra>"
    )

    fig_engagement.update_layout(
        paper_bgcolor="#050B14",
        font_color="#FFFFFF"
    )

    st.plotly_chart(fig_engagement, use_container_width=True)

    level_cols = st.columns(3)

    with level_cols[0]:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">Low Engagement</div>
            <div class="insight-text">
                {low_rate:.1f}% audience berada pada level Low.
                Segmen ini membutuhkan pesan campaign yang lebih sederhana dan awareness-driven.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with level_cols[1]:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">Medium Engagement</div>
            <div class="insight-text">
                {medium_rate:.1f}% audience berada pada level Medium.
                Segmen ini potensial untuk edukasi produk dan retargeting.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with level_cols[2]:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">High Engagement</div>
            <div class="insight-text">
                {high_rate:.1f}% audience berada pada level High.
                Segmen ini paling potensial untuk conversion-oriented campaign.
            </div>
        </div>
        """, unsafe_allow_html=True)


with tab2:
    st.subheader("Distribusi Digital Interest Score dengan Threshold Engagement")

    score_data = filtered_df["Digital Interest Score"].dropna()

    fig_score_hist = px.histogram(
        filtered_df,
        x="Digital Interest Score",
        nbins=20,
        title="Digital Interest Score Distribution with Engagement Threshold",
        color_discrete_sequence=["#5B8FF9"]
    )

    fig_score_hist.update_traces(
        marker_opacity=0.75,
        hovertemplate=
        "<b>Score Range:</b> %{x}<br>" +
        "<b>Jumlah User:</b> %{y}<extra></extra>"
    )

    fig_score_hist.add_vrect(
        x0=0,
        x1=45,
        fillcolor="#65789B",
        opacity=0.18,
        line_width=0,
        annotation_text="Low",
        annotation_position="top left"
    )

    fig_score_hist.add_vrect(
        x0=45,
        x1=75,
        fillcolor="#61DDAA",
        opacity=0.15,
        line_width=0,
        annotation_text="Medium",
        annotation_position="top left"
    )

    fig_score_hist.add_vrect(
        x0=75,
        x1=100,
        fillcolor="#5B8FF9",
        opacity=0.16,
        line_width=0,
        annotation_text="High",
        annotation_position="top left"
    )

    fig_score_hist.add_vline(
        x=45,
        line_width=2,
        line_dash="dash",
        line_color="#A8B3CF",
        annotation_text="Low → Medium",
        annotation_position="top"
    )

    fig_score_hist.add_vline(
        x=75,
        line_width=2,
        line_dash="dash",
        line_color="#A8B3CF",
        annotation_text="Medium → High",
        annotation_position="top"
    )

    fig_score_hist.add_vline(
        x=avg_score,
        line_width=3,
        line_dash="dot",
        line_color="#FFB020",
        annotation_text=f"Avg Score: {avg_score:.1f}",
        annotation_position="bottom right"
    )

    fig_score_hist.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Digital Interest Score",
        yaxis_title="Jumlah User",
        xaxis_range=[0, 100],
        bargap=0.05,
        showlegend=False
    )

    st.plotly_chart(fig_score_hist, use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Threshold Interpretation</div>
        <div class="insight-text">
            Engagement Level diklasifikasikan berdasarkan threshold score:
            <b>Low</b> untuk score di bawah 45, <b>Medium</b> untuk score 45–74,
            dan <b>High</b> untuk score 75 ke atas. Rata-rata score saat ini berada
            di angka <b>{avg_score:.1f}</b>, sementara median score berada di angka
            <b>{median_score:.1f}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("Performa Score Berdasarkan Audience Segment")

    score_segment_sorted = score_segment.sort_values(
        "Rata-rata Digital Interest Score",
        ascending=True
    )

    fig_segment_score = px.bar(
        score_segment_sorted,
        x="Rata-rata Digital Interest Score",
        y="Audience Segment",
        text=score_segment_sorted["Rata-rata Digital Interest Score"].round(1),
        orientation="h",
        title="Average Digital Interest Score by Audience Segment",
        color="Audience Segment",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_segment_score.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Audience Segment:</b> %{y}<br>" +
        "<b>Rata-rata Score:</b> %{x:.1f}<extra></extra>"
    )

    fig_segment_score.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Rata-rata Digital Interest Score",
        yaxis_title="Audience Segment",
        xaxis_range=[0, 100],
        showlegend=False,
        height=650
    )

    st.plotly_chart(fig_segment_score, use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Best Performing Segment</div>
        <div class="insight-text">
            <b>{best_segment}</b> memiliki rata-rata score tertinggi sebesar
            <b>{best_segment_score:.1f}</b>. Segmen ini dapat diprioritaskan
            untuk campaign dengan objektif engagement dan conversion.
        </div>
    </div>
    """, unsafe_allow_html=True)


with tab4:
    st.subheader("Engagement Matrix: Minat Digital vs Engagement Level")

    matrix_data = pd.crosstab(
        filtered_df["Minat Digital"],
        filtered_df["Engagement Level"]
    )

    fig_matrix = px.imshow(
        matrix_data,
        text_auto=True,
        aspect="auto",
        title="Engagement Matrix by Digital Interest",
        color_continuous_scale=[
            "#08101E",
            "#12273C",
            "#1D3B59",
            "#5B8FF9"
        ]
    )

    fig_matrix.update_traces(
        hovertemplate=
        "<b>Minat Digital:</b> %{y}<br>" +
        "<b>Engagement Level:</b> %{x}<br>" +
        "<b>Jumlah User:</b> %{z}<extra></extra>"
    )

    fig_matrix.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Engagement Level",
        yaxis_title="Minat Digital"
    )

    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">Matrix Interpretation</div>
        <div class="insight-text">
            Matrix ini membantu mengidentifikasi kategori minat digital yang paling banyak
            menghasilkan audience dengan engagement tinggi. Informasi ini dapat digunakan
            untuk menentukan interest-based campaign priority.
        </div>
    </div>
    """, unsafe_allow_html=True)


with st.expander("Lihat dataset engagement analysis"):
    st.dataframe(filtered_df, use_container_width=True)

render_footer()