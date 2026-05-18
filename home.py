import streamlit as st
from lib.loaders import load_user_data
from lib.ui import page_config, render_footer


page_config()

df = load_user_data()


st.markdown("""
<style>
.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.subtitle {
    font-size: 15px;
    letter-spacing: 3px;
    color: #8FAADC;
    text-transform: uppercase;
    margin-bottom: 40px;
}

.feature-card {
    background-color: #151B2D;
    border: 1px solid #2A3655;
    border-radius: 16px;
    padding: 28px;
    min-height: 210px;
    margin-bottom: 18px;
}

.feature-card-blue {
    border-top: 4px solid #5B8FF9;
}

.feature-card-purple {
    border-top: 4px solid #8D6FD1;
}

.feature-card-green {
    border-top: 4px solid #61DDAA;
}

.feature-card-orange {
    border-top: 4px solid #FFB020;
}

.card-icon {
    font-size: 34px;
    margin-bottom: 22px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 14px;
}

.card-desc {
    font-size: 15px;
    color: #A8B3CF;
    line-height: 1.6;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 42px;
    margin-bottom: 14px;
}

.home-note {
    background-color: #151B2D;
    border: 1px solid #2A3655;
    border-radius: 16px;
    padding: 22px 24px;
    color: #A8B3CF;
    line-height: 1.6;
    margin-bottom: 28px;
}
</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">HIGO Audience Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Location-Based Audience Profiling & Digital Interest Analytics</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="home-note">
Dashboard ini dirancang untuk membantu memahami karakteristik audience berdasarkan lokasi,
perilaku akses, perangkat, minat digital, dan tingkat engagement. Insight yang dihasilkan dapat
digunakan untuk mendukung strategi campaign yang lebih relevan, tersegmentasi, dan berbasis data.
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-title">Dashboard Modules</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card feature-card-blue">
        <div class="card-icon">👥</div>
        <div class="card-title">Audience Overview</div>
        <div class="card-desc">
            Menampilkan profil utama audience seperti jumlah pengguna, distribusi usia,
            kelompok generasi, serta karakteristik umum pengguna pada berbagai touchpoint.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Buka Audience Overview", use_container_width=True):
        st.switch_page("pages/1_Audience_Overview.py")

with col2:
    st.markdown("""
    <div class="feature-card feature-card-purple">
        <div class="card-icon">💡</div>
        <div class="card-title">Digital Interest Analysis</div>
        <div class="card-desc">
            Menganalisis kategori minat digital audience, distribusi interest,
            score performance, dan peluang interest-based targeting.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Buka Digital Interest Analysis", use_container_width=True):
        st.switch_page("pages/2_Digital_Interest_Analysis.py")


col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="feature-card feature-card-green">
        <div class="card-icon">📍</div>
        <div class="card-title">Location Insight</div>
        <div class="card-desc">
            Memberikan insight performa audience berdasarkan lokasi,
            kontribusi lokasi, serta peluang campaign berbasis area.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Buka Location Insight", use_container_width=True):
        st.switch_page("pages/3_Location_Insight.py")

with col4:
    st.markdown("""
    <div class="feature-card feature-card-orange">
        <div class="card-icon">⚡</div>
        <div class="card-title">Engagement Analysis</div>
        <div class="card-desc">
            Mengelompokkan audience berdasarkan digital interest score,
            engagement level, dan segment performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Buka Engagement Analysis", use_container_width=True):
        st.switch_page("pages/4_Engagement_Analysis.py")


st.markdown("""
<div class="feature-card feature-card-blue">
    <div class="card-icon">📌</div>
    <div class="card-title">Statistical Insight</div>
    <div class="card-desc">
        Menyediakan analisis statistik seperti confidence interval,
        distribusi score, dan tren rata-rata untuk mendukung interpretasi data
        secara lebih terukur.
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Buka Statistical Insight", use_container_width=True):
    st.switch_page("pages/5_Statistical_Insight.py")


st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)

st.markdown("""
Preview data digunakan untuk validasi cepat terhadap struktur informasi audience
yang menjadi basis analisis dashboard.
""")

with st.expander("Lihat dataset"):
    st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Dataset",
    data=csv,
    file_name="higo_audience_data.csv",
    mime="text/csv",
    use_container_width=True
)

render_footer()