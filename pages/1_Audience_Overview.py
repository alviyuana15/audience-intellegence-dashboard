import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

from lib.loaders import load_user_data
from lib.ui import page_config, render_footer
from lib.utils import create_summary_count


page_config()

df = load_user_data()

st.sidebar.title("HIGO Analytics")
st.sidebar.caption("Audience overview control panel")

location_filter = st.sidebar.multiselect(
    "Tipe Lokasi",
    options=sorted(df["Tipe Lokasi"].unique()),
    default=sorted(df["Tipe Lokasi"].unique())
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

filtered_df = df[
    (df["Tipe Lokasi"].isin(location_filter)) &
    (df["Kelompok Usia"].isin(age_group_filter)) &
    (df["Merk HP"].isin(phone_filter))
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
    font-size: 38px;
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


st.markdown('<div class="page-title">Audience Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Executive Summary · Audience Profile · Demographic View</div>',
    unsafe_allow_html=True
)


total_audience = len(filtered_df)
avg_age = filtered_df["Usia"].mean() if total_audience > 0 else 0
dominant_age_group = filtered_df["Kelompok Usia"].mode()[0] if total_audience > 0 else "-"
top_device = filtered_df["Merk HP"].mode()[0] if total_audience > 0 else "-"
unique_locations = filtered_df["Nama Lokasi"].nunique() if total_audience > 0 else 0


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Audience</div>
        <div class="kpi-value">{total_audience:,}</div>
        <div class="kpi-note">pengguna aktif dalam data</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#61DDAA;">
        <div class="kpi-label">Average Age</div>
        <div class="kpi-value">{avg_age:.1f}</div>
        <div class="kpi-note">rata-rata usia pengguna</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#8D6FD1;">
        <div class="kpi-label">Dominant Group</div>
        <div class="kpi-value" style="font-size:30px;">{dominant_age_group}</div>
        <div class="kpi-note">kelompok usia terbesar</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#78D3F8;">
        <div class="kpi-label">Top Device</div>
        <div class="kpi-value" style="font-size:30px;">{top_device}</div>
        <div class="kpi-note">brand perangkat dominan</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:#9270CA;">
        <div class="kpi-label">Locations</div>
        <div class="kpi-value">{unique_locations}</div>
        <div class="kpi-note">lokasi terdeteksi</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


age_group_summary = create_summary_count(filtered_df, "Kelompok Usia")
location_summary = create_summary_count(filtered_df, "Tipe Lokasi")
phone_summary = create_summary_count(filtered_df, "Merk HP")

top_location_type = filtered_df["Tipe Lokasi"].mode()[0] if total_audience > 0 else "-"
young_share = (
    filtered_df["Kelompok Usia"].isin(["Gen Z", "Millennial"]).sum() / total_audience * 100
    if total_audience > 0 else 0
)

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Audience Composition</div>
        <div class="insight-text">
            {young_share:.1f}% audience berasal dari Gen Z dan Millennial,
            menunjukkan basis pengguna yang relatif digital-native.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Location Signal</div>
        <div class="insight-text">
            Tipe lokasi dominan adalah <b>{top_location_type}</b>,
            yang dapat menjadi prioritas awal untuk aktivasi campaign.
        </div>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Device Readiness</div>
        <div class="insight-text">
            Brand perangkat dominan adalah <b>{top_device}</b>,
            memberi indikasi kesiapan audience terhadap mobile-first experience.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="section-title">Audience Breakdown</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "User by Location",
    "Age Distribution",
    "Age Group",
    "Device Brand"
])


with tab1:
    st.subheader("Distribusi User Berdasarkan Tipe Lokasi")

    fig_location = px.bar(
        location_summary,
        x="Tipe Lokasi",
        y="Jumlah User",
        text="Jumlah User",
        title="Jumlah User per Tipe Lokasi",
        color="Tipe Lokasi",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_location.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Tipe Lokasi:</b> %{x}<br>" +
        "<b>Jumlah User:</b> %{y}<extra></extra>"
    )

    fig_location.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Tipe Lokasi",
        yaxis_title="Jumlah User",
        showlegend=False
    )

    st.plotly_chart(fig_location, use_container_width=True)


with tab2:
    st.subheader("Distribusi Usia Pengguna")

    age_values = filtered_df["Usia"].dropna().astype(int)

    fig_age = ff.create_distplot(
        [age_values],
        group_labels=["Usia"],
        bin_size=2,
        show_rug=False,
        colors=["#7FA6E8"]
    )

    fig_age.data[0].marker.color = "#6F8FBF"
    fig_age.data[0].marker.opacity = 0.65
    fig_age.data[1].line.color = "#B8C7E6"
    fig_age.data[1].line.width = 3

    fig_age.update_traces(
        hovertemplate=
        "<b>Usia:</b> %{x}<br>" +
        "<b>Distribusi:</b> %{y:.3f}<extra></extra>"
    )

    fig_age.update_layout(
        title="Distribusi Usia Pengguna",
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Usia",
        yaxis_title="Density",
        bargap=0.06,
        showlegend=False
    )

    st.plotly_chart(fig_age, use_container_width=True)


with tab3:
    st.subheader("Distribusi Kelompok Usia")

    fig_age_group = px.pie(
        age_group_summary,
        names="Kelompok Usia",
        values="Jumlah User",
        title="Proporsi Kelompok Usia",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_age_group.update_traces(
        hovertemplate=
        "<b>Kelompok Usia:</b> %{label}<br>" +
        "<b>Jumlah User:</b> %{value}<br>" +
        "<b>Persentase:</b> %{percent}<extra></extra>"
    )

    fig_age_group.update_layout(
        paper_bgcolor="#050B14",
        font_color="#FFFFFF"
    )

    st.plotly_chart(fig_age_group, use_container_width=True)


with tab4:
    st.subheader("Distribusi Merk HP")

    fig_phone = px.bar(
        phone_summary,
        x="Merk HP",
        y="Jumlah User",
        text="Jumlah User",
        title="Distribusi Merk HP Pengguna",
        color="Merk HP",
        color_discrete_sequence=COLOR_PALETTE
    )

    fig_phone.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Merk HP:</b> %{x}<br>" +
        "<b>Jumlah User:</b> %{y}<extra></extra>"
    )

    fig_phone.update_layout(
        plot_bgcolor="#050B14",
        paper_bgcolor="#050B14",
        font_color="#FFFFFF",
        xaxis_title="Merk HP",
        yaxis_title="Jumlah User",
        showlegend=False
    )

    st.plotly_chart(fig_phone, use_container_width=True)


with st.expander("Lihat dataset audience"):
    st.dataframe(filtered_df, use_container_width=True)

render_footer()