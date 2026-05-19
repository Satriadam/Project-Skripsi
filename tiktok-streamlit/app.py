import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================================
# STYLE SIDEBAR PROFESSIONAL
# =========================================
st.markdown("""
<style>

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #6e1d3a;
    transition: all 0.3s ease;
}

/* COLLAPSE CONTROL */
[data-testid="collapsedControl"] {
    color: white;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    text-align: left;
    padding: 14px 18px;
    font-size: 17px;
    font-weight: 600;
    color: white;
    background-color: transparent;
    border: none;
    border-radius: 0px;
    transition: all 0.25s ease;
}

/* HOVER */
.stButton>button:hover {
    background-color: rgba(255,255,255,0.12);
    transform: translateX(5px);
}

/* ACTIVE STYLE (FULL WIDTH BAR) */
.active button {
    background-color: white !important;
    color: #6e1d3a !important;
    border-left: 5px solid #ff4b4b;
}

/* DIVIDER */
.divider {
    height: 1px;
    background-color: rgba(255,255,255,0.3);
    margin: 6px 0;
}

/* TITLE */
.big-title {
    font-size:42px;
    font-weight:800;
    color:#800000;
}

.section {
    font-size:22px;
    font-weight:700;
    margin-top:20px;
    color:#800000;
}

/* KPI CARD */
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #800000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* BACKGROUND UTAMA */
.main {
    background-color: #f4f6f9;
}

/* SECTION WRAPPER (PEMBUNGKUS BESAR) */
.section-box {
    background-color: #eef1f5;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 25px;
}

/* CARD (ISI) */
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* TITLE */
.card-title {
    font-size:18px;
    font-weight:600;
    margin-bottom:10px;
    color:#800000;
}

            /* CONTAINER BERGARIS (OUTLINED CARD) */
.outline-box {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 20px;
    background-color: white;
}

/* JUDUL DALAM BOX */
.box-title {
    font-size: 16px;
    font-weight: 600;
    color: #800000;
    margin-bottom: 10px;
}

/* SPACING GLOBAL */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADER PROFESSIONAL */
.header-box {
    background: linear-gradient(#6e1d3a,#6e1d3a);
    padding: 25px 30px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    margin-bottom: 25px;
}

.header-title {
    font-size: 28px;
    font-weight: 700;
}

.header-sub {
    font-size: 14px;
    opacity: 0.9;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    df_konten = pd.read_csv("data/hasil_analisis_konten.csv")
    df_agregat = pd.read_csv("data/hasil_clustering_agregat_1tahun.csv")
    return df_konten, df_agregat

df_konten, df_agregat = load_data()

# =========================================
# HEADER FUNCTION (TAMBAHKAN DI SINI)
# =========================================
def render_header(title, subtitle):
    st.markdown(f"""
    <div class="header-box">
        <div class="header-title">{title}</div>
        <div class="header-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
# =========================================
# SIDEBAR PREMIUM
# =========================================
with st.sidebar:

    # LOGO
    col1, col2 = st.columns(2)
    col1.image("assets/logo_kampus.png", width=60)
    col2.image("assets/logo_radar.png", width=70)

    st.markdown("<br>", unsafe_allow_html=True)

    # STATE
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    def nav(label, key):
        if st.session_state.page == key:
            btn_class = "nav-btn active-btn"
        else:
            btn_class = "nav-btn"

        if st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True):
            pass

        if st.button(label, key=key):
            st.session_state.page = key

        st.markdown('</div>', unsafe_allow_html=True)

        # divider
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


    # MENU (ICON CLEAN)
    nav("▣  Dashboard", "dashboard")
    nav("▤  Data Agregat", "agregat")
    nav("▥  Analisis Konten", "konten")
    nav("▦  Strategi & Rekomendasi", "strategi")

menu = st.session_state.page


# =========================================
# ================= DASHBOARD =================
# =========================================
df_agregat['date'] = pd.to_datetime(df_agregat['date'], errors='coerce')

df_agregat['day_name'] = df_agregat['date'].dt.day_name()
df_agregat['month'] = df_agregat['date'].dt.month_name()


if menu == "dashboard":
    render_header(
        "📊 Dashboard Analisis TikTok Radar Sukabumi",
        "Ringkasan performa konten dan insight utama"
    )

    # ================= KPI =================

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
    <div style='background:white;padding:20px;border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);'>
    <b>Total Views</b><br>
    <span style='font-size:22px'>{df_agregat["video_views"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div style='background:white;padding:20px;border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);'>
    <b>Avg Engagement</b><br>
    <span style='font-size:22px'>{df_agregat["engagement_rate"].mean():.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div style='background:white;padding:20px;border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);'>
    <b>Total Konten</b><br>
    <span style='font-size:22px'>{len(df_konten)}</span>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div style='background:white;padding:20px;border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);'>
    <b>Best Engagement</b><br>
    <span style='font-size:22px'>{df_konten["engagement_rate"].max():.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Trend Video Views")
        fig = px.line(df_agregat, x="date", y="video_views")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Trend Engagement Rate")
        fig2 = px.line(df_agregat, x="date", y="engagement_rate")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= ROW 2 =================
    col1, col2 = st.columns(2)

    avg_day = df_agregat.groupby('day_name')['video_views'].mean().reset_index()

    with col1:
        st.markdown("#### 📅 Rata-rata Views per Hari")
        fig3 = px.bar(avg_day, x="day_name", y="video_views")
        st.plotly_chart(fig3, use_container_width=True)

    avg_month = df_agregat.groupby('month')['video_views'].mean().reset_index()

    with col2:
        st.markdown("#### 🗓️ Rata-rata Views per Bulan")
        fig4 = px.bar(avg_month, x="month", y="video_views")
        st.plotly_chart(fig4, use_container_width=True)

    # ================= ROW 3 =================
    st.markdown("#### 🎯 Performa Konten")

    perf = df_konten.groupby("content_type")[["engagement_rate"]].mean()

    fig5 = px.bar(perf, y=perf.index, x="engagement_rate", orientation='h')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# ================= AGREGAT =================
# =========================================
elif menu == "agregat":
    render_header(
        "📈 Data Agregat 1 Tahun",
        "Analisis tren performa berdasarkan waktu"
    )

    # ================= KPI MINI =================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Views", f"{df_agregat['video_views'].sum():,.0f}")
    col2.metric("Avg Engagement", f"{df_agregat['engagement_rate'].mean():.2f}%")
    col3.metric("Total Hari Data", len(df_agregat))

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Trend Video Views")
        fig1 = px.line(df_agregat, x="date", y="video_views")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 📊 Trend Engagement Rate")
        fig2 = px.line(df_agregat, x="date", y="engagement_rate")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= ROW 2 =================
    col1, col2 = st.columns(2)

    avg_day = df_agregat.groupby('day_name')['video_views'].mean().reset_index()

    with col1:
        st.markdown("### 📅 Rata-rata Views per Hari")
        fig3 = px.bar(avg_day, x="day_name", y="video_views")
        st.plotly_chart(fig3, use_container_width=True)

    avg_month = df_agregat.groupby('month')['video_views'].mean().reset_index()

    with col2:
        st.markdown("### 🗓️ Rata-rata Views per Bulan")
        fig4 = px.bar(avg_month, x="month", y="video_views")
        st.plotly_chart(fig4, use_container_width=True)

    # ================= INSIGHT =================
    best_day = df_agregat.loc[df_agregat['video_views'].idxmax()]

    st.markdown("<br>", unsafe_allow_html=True)

    st.success(
        f"Hari dengan performa tertinggi adalah {best_day['date'].date()} "
        f"dengan {best_day['video_views']:,} views"
    )

# =========================================
# ================= KONTEN =================
# =========================================
elif menu == "konten":
    render_header(
        "🎯 Analisis Per Konten",
        "Evaluasi performa berdasarkan kategori dan jenis konten"
    )

    kategori = st.selectbox("Kategori", ["Semua"] + list(df_konten['performance_category'].dropna().unique()))
    content = st.selectbox("Jenis Konten", ["Semua"] + list(df_konten['content_type'].dropna().unique()))

    df_filtered = df_konten.copy()

    if kategori != "Semua":
        df_filtered = df_filtered[df_filtered['performance_category'] == kategori]

    if content != "Semua":
        df_filtered = df_filtered[df_filtered['content_type'] == content]

    # ================= VALIDASI DATA =================
    if df_filtered.empty:
        st.warning("Data tidak tersedia untuk filter yang dipilih")
    else:
        # ================= KPI =================
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Views", f"{df_filtered['video_views'].mean():,.0f}")
        col2.metric("Avg Engagement", f"{df_filtered['engagement_rate'].mean():.2f}%")
        col3.metric("Total Konten", len(df_filtered))

        # ================= HISTOGRAM =================
        fig = px.histogram(df_filtered, x="performance_category", title="Distribusi Performa")
        st.plotly_chart(fig, use_container_width=True)

        # ================= BAR CHART (TAMBAHAN) =================
        st.markdown("### 📊 Performa Rata-rata per Jenis Konten")

        perf = df_filtered.groupby("content_type")[["engagement_rate"]].mean()

        fig5 = px.bar(
            perf,
            y=perf.index,
            x="engagement_rate",
            orientation='h'
        )

        fig5.update_layout(
            xaxis_title="Engagement Rate (%)",
            yaxis_title="Content Type",
            plot_bgcolor="white"
        )

        st.plotly_chart(fig5, use_container_width=True)

        # ================= INSIGHT =================
        st.markdown('<p class="section">Insight & Strategi Cepat</p>', unsafe_allow_html=True)

        # HANDLE kalau tidak ada engagement_total
        if 'engagement_total' in df_konten.columns:
            best = df_konten.loc[df_konten['engagement_total'].idxmax()]
            worst = df_konten.loc[df_konten['engagement_total'].idxmin()]

            st.success(f"Konten terbaik: {best['content_type']} ({best['engagement_total']:,.0f})")
            st.error(f"Konten terburuk: {worst['content_type']} ({worst['engagement_total']:,.0f})")
        else:
            best = df_konten.loc[df_konten['engagement_rate'].idxmax()]
            worst = df_konten.loc[df_konten['engagement_rate'].idxmin()]

            st.success(f"Konten terbaik: {best['content_type']} ({best['engagement_rate']:.2f}%)")
            st.error(f"Konten terburuk: {worst['content_type']} ({worst['engagement_rate']:.2f}%)")


# =========================================
# ================= STRATEGI =================
# =========================================
elif menu == "strategi":

    render_header(
        "🚀 Strategi & Rekomendasi",
        "Insight berbasis data untuk optimasi konten"
    )

    # ===============================
    # PREPROCESS
    # ===============================
    df_agregat['date'] = pd.to_datetime(df_agregat['date'], errors='coerce')
    df_agregat['day_name'] = df_agregat['date'].dt.day_name()
    df_agregat['month'] = df_agregat['date'].dt.month_name()

    # ===============================
    # KPI UTAMA
    # ===============================
    st.markdown("### 📊 Hasil Analisis Performa")

    col1, col2, col3 = st.columns(3)

    best_day_views = df_agregat.groupby('day_name')['video_views'].mean().idxmax()
    best_day_eng = df_agregat.groupby('day_name')['engagement_rate'].mean().idxmax()
    best_month = df_agregat.groupby('month')['video_views'].mean().idxmax()

    col1.metric("Hari Views Tertinggi", best_day_views)
    col2.metric("Hari Engagement Tertinggi", best_day_eng)
    col3.metric("Bulan Terbaik", best_month)

    # ===============================
    # TABEL ANALISIS
    # ===============================
    st.markdown("### 📅 Analisis Hari Terbaik")
    day_perf = df_agregat.groupby('day_name').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean'
    }).sort_values(by='video_views', ascending=False)

    st.dataframe(day_perf)

    st.markdown("### 🗓️ Analisis Bulan Terbaik")
    month_perf = df_agregat.groupby('month').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean'
    }).sort_values(by='video_views', ascending=False)

    st.dataframe(month_perf)

    # ===============================
    # ANALISIS KONTEN
    # ===============================
    st.markdown("### 🎯 Analisis Berdasarkan Konten")

    content_perf = df_konten.groupby('content_type').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean',
        'engagement_total': 'mean' if 'engagement_total' in df_konten.columns else 'engagement_rate'
    })

    st.dataframe(content_perf)

    # ===============================
    # WAKTU UPLOAD
    # ===============================
    if 'upload_category' in df_konten.columns:
        st.markdown("### ⏰ Analisis Waktu Upload")

        time_perf = df_konten.groupby('upload_category').agg({
            'video_views': 'mean',
            'engagement_rate': 'mean'
        })

        st.dataframe(time_perf)

    # ===============================
    # BEST CONTENT
    # ===============================
    best_views = df_konten.groupby('content_type')['video_views'].mean().idxmax()
    best_eng = df_konten.groupby('content_type')['engagement_rate'].mean().idxmax()

        # ===============================
    # STRATEGI OTOMATIS
    # ===============================
    st.markdown("### 🧠 Insight Otomatis & Strategi")

    avg_views = df_agregat['video_views'].mean()
    avg_eng = df_agregat['engagement_rate'].mean()

    st.markdown(f"""
    <div class='outline-box'>

    <b>Kategori performa terbaik:</b> Tinggi <br>
    <b>Hari dominan:</b> {best_day_views} <br>
    <b>Bulan dominan:</b> {best_month} <br><br>

    <b>Rata-rata views:</b> {avg_views:,.0f} <br>
    <b>Rata-rata engagement rate:</b> {avg_eng:.2f}% <br>

    </div>
    """, unsafe_allow_html=True)


    # ===============================
    # REKOMENDASI
    # ===============================
    st.markdown("### 📌 Rekomendasi Strategi")

    if 'upload_category' in df_konten.columns:
        best_time_views = df_konten.groupby('upload_category')['video_views'].mean().idxmax()
        best_time_eng = df_konten.groupby('upload_category')['engagement_rate'].mean().idxmax()
    else:
        best_time_views = "-"
        best_time_eng = "-"

    st.markdown(f"""
    <div class='outline-box'>

    <b>1. Jenis konten terbaik:</b><br>
    - Views: {best_views}<br>
    - Engagement: {best_eng}<br><br>

    <b>2. Waktu upload terbaik:</b><br>
    - Views: {best_time_views}<br>
    - Engagement: {best_time_eng}<br><br>

    <b>3. Hari terbaik:</b><br>
    - Views: {best_day_views}<br>
    - Engagement: {best_day_eng}<br><br>

    <b>4. Rekomendasi:</b><br>
    - Fokus pada konten {best_views}<br>
    - Upload pada waktu {best_time_views}<br>
    - Konsisten di hari {best_day_views}<br>
    - Replikasi pola konten performa tinggi<br>
    - Gunakan hari rendah untuk eksperimen konten<br>

    </div>
    """, unsafe_allow_html=True)
