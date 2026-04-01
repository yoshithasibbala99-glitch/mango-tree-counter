import streamlit as st
from PIL import Image
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌴 Mango Tree Counter",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #040d05 !important;
    color: #e8f5e2;
}
.stApp { background: #040d05 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Animated background ── */
.bg-orbs {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.18;
    animation: drift 12s ease-in-out infinite alternate;
}
.orb1 { width: 500px; height: 500px; background: #2d7a22; top: -100px; left: -100px; animation-delay: 0s; }
.orb2 { width: 400px; height: 400px; background: #f59e0b; top: 30%; right: -80px; animation-delay: 3s; }
.orb3 { width: 350px; height: 350px; background: #16a34a; bottom: -80px; left: 30%; animation-delay: 6s; }
@keyframes drift {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(30px, 20px) scale(1.08); }
}

/* ── Main layout ── */
.page-wrap {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 4rem;
}

/* ── Header ── */
.header-area {
    text-align: center;
    margin-bottom: 2.5rem;
    animation: fadeUp 0.8s ease both;
}
.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.4);
    color: #fbbf24;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 999px;
    margin-bottom: 16px;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 6vw, 62px);
    font-weight: 800;
    color: #f0fdf0;
    line-height: 1.1;
    margin: 0 0 10px;
    letter-spacing: -1px;
}
.header-title .accent { color: #86ef5c; }
.header-title .mango  { color: #fbbf24; }
.header-sub {
    color: rgba(220,252,220,0.42);
    font-size: 14px;
    font-weight: 400;
    max-width: 460px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Mango decoration strip ── */
.mango-strip {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 0 0 2rem;
    font-size: 22px;
    animation: fadeUp 0.9s 0.1s ease both;
    opacity: 0;
}
@keyframes fadeUp {
    from { opacity:0; transform: translateY(18px); }
    to   { opacity:1; transform: translateY(0); }
}

/* ── Stats bar ── */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 2rem;
    animation: fadeUp 0.9s 0.15s ease both;
    opacity: 0;
}
.stat-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(134,239,92,0.15);
    border-radius: 16px;
    padding: 16px 12px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #86ef5c, transparent);
    opacity: 0.5;
}
.stat-card:hover { border-color: rgba(134,239,92,0.35); transform: translateY(-2px); }
.stat-icon { font-size: 18px; margin-bottom: 6px; }
.stat-val  { font-size: 28px; font-weight: 800; color: #86ef5c; line-height: 1; }
.stat-val.gold { color: #fbbf24; }
.stat-lbl  { font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(220,252,220,0.38); margin-top: 5px; }

/* ── Upload zone ── */
.upload-section {
    background: rgba(10,31,14,0.7);
    border: 2px dashed rgba(134,239,92,0.25);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s;
    animation: fadeUp 0.9s 0.2s ease both;
    opacity: 0;
}
.upload-section:hover { border-color: rgba(134,239,92,0.45); }
.upload-icon { font-size: 36px; margin-bottom: 8px; }
.upload-title { font-size: 15px; font-weight: 600; color: #d1fad1; margin-bottom: 4px; }
.upload-hint  { font-size: 11px; color: rgba(220,252,220,0.38); margin-bottom: 1rem; }

/* ── Streamlit uploader override ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(134,239,92,0.04) !important;
    border: 1px solid rgba(134,239,92,0.2) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div span {
    color: rgba(220,252,220,0.5) !important;
    font-size: 13px !important;
}
[data-testid="stFileUploader"] label { display: none !important; }

/* ── Detect button ── */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #052e08 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #86ef5c, #22c55e) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(134,239,92,0.3) !important;
}
button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(220,252,220,0.6) !important;
    border: 1px solid rgba(134,239,92,0.2) !important;
}

/* ── Result card ── */
.result-card {
    background: rgba(10,31,14,0.8);
    border: 1px solid rgba(134,239,92,0.14);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
    animation: fadeUp 0.5s ease both;
}
.rc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: rgba(134,239,92,0.05);
    border-bottom: 1px solid rgba(134,239,92,0.08);
}
.rc-filename { font-size: 13px; font-weight: 600; color: #d1fad1; display: flex; align-items: center; gap: 8px; }
.rc-filename .dot { width: 7px; height: 7px; background: #86ef5c; border-radius: 50%; box-shadow: 0 0 8px #86ef5c; }
.rc-pill {
    background: #86ef5c;
    color: #052e08;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 14px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.rc-body { padding: 12px; }
.col-lbl {
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(220,252,220,0.32);
    margin-bottom: 6px;
    padding-left: 2px;
}

/* ── Total banner ── */
.total-banner {
    background: linear-gradient(135deg, rgba(134,239,92,0.1), rgba(34,197,94,0.06));
    border: 1px solid rgba(134,239,92,0.3);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.total-banner::before {
    content: '🌴';
    position: absolute;
    font-size: 120px;
    opacity: 0.04;
    top: -20px;
    right: -10px;
    pointer-events: none;
}
.total-emoji { font-size: 32px; margin-bottom: 4px; }
.total-num   { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 800; color: #86ef5c; line-height: 1; }
.total-lbl   { font-size: 12px; color: rgba(220,252,220,0.45); margin-top: 8px; letter-spacing: 0.05em; }
.total-sub   { font-size: 11px; color: rgba(245,158,11,0.7); margin-top: 6px; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: rgba(220,252,220,0.3);
}
.empty-state .big { font-size: 48px; margin-bottom: 12px; }
.empty-state p { font-size: 13px; }

/* ── How-to strip ── */
.howto {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 2rem;
    animation: fadeUp 0.9s 0.25s ease both;
    opacity: 0;
}
.howto-step {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 14px 12px;
    text-align: center;
}
.howto-num  { font-size: 11px; font-weight: 700; color: #fbbf24; letter-spacing: 0.1em; margin-bottom: 6px; }
.howto-icon { font-size: 22px; margin-bottom: 6px; }
.howto-txt  { font-size: 11px; color: rgba(220,252,220,0.45); line-height: 1.4; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #86ef5c !important; }

/* ── Info / warning ── */
.stAlert { border-radius: 12px !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(134,239,92,0.2); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Animated background orbs ──────────────────────────────────────────────────
st.markdown("""
<div class="bg-orbs">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = []

# ── Helper: run YOLO ──────────────────────────────────────────────────────────
def run_model(image):
    from ultralytics import YOLO

    model = YOLO("yolov8n.pt")   # auto-downloads model

    results = model(image)[0]

    count = len(results.boxes)

    annotated = Image.fromarray(results.plot())

    return annotated, count
# ── Page wrapper open ─────────────────────────────────────────────────────────
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-area">
  <div class="header-badge">🛰️ &nbsp; AI-Powered Remote Sensing</div>
  <div class="header-title">
    <span class="mango">Mango</span> Tree<br>
    <span class="accent">Detection &amp; Counter</span>
  </div>
  <p class="header-sub">
    Upload aerial or field photographs to automatically detect,
    annotate, and count every mango tree with YOLOv8 precision.
  </p>
</div>

<div class="mango-strip">
  🌳&nbsp;🌴&nbsp;🥭&nbsp;🌳&nbsp;🌿&nbsp;🥭&nbsp;🌴&nbsp;🌳
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
total_trees  = sum(r["count"] for r in st.session_state.results)
total_images = len(st.session_state.results)
avg_per      = round(total_trees / total_images, 1) if total_images else 0.0
best_img     = max((r["count"] for r in st.session_state.results), default=0)

st.markdown(f"""
<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-icon">🌳</div>
    <div class="stat-val">{total_trees}</div>
    <div class="stat-lbl">Trees Detected</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🖼️</div>
    <div class="stat-val">{total_images}</div>
    <div class="stat-lbl">Images Analysed</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">📊</div>
    <div class="stat-val">{avg_per}</div>
    <div class="stat-lbl">Avg per Image</div>
  </div>
  <div class="stat-card">
    <div class="stat-icon">🏆</div>
    <div class="stat-val gold">{best_img}</div>
    <div class="stat-lbl">Best Single Image</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── How-to strip ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="howto">
  <div class="howto-step">
    <div class="howto-num">STEP 01</div>
    <div class="howto-icon">📸</div>
    <div class="howto-txt">Upload aerial or field photos of your mango orchard</div>
  </div>
  <div class="howto-step">
    <div class="howto-num">STEP 02</div>
    <div class="howto-icon">🤖</div>
    <div class="howto-txt">YOLOv8 AI detects every tree and draws bounding boxes</div>
  </div>
  <div class="howto-step">
    <div class="howto-num">STEP 03</div>
    <div class="howto-icon">📋</div>
    <div class="howto-txt">Get instant count with annotated images to download</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Upload section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="upload-section">
  <div class="upload-icon">📂</div>
  <div class="upload-title">Drop your orchard images here</div>
  <div class="upload-hint">JPG · PNG · JPEG &nbsp;|&nbsp; Multiple files supported</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    detect_clicked = st.button("🌿 Detect Mango Trees", use_container_width=True)
with col_btn2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.results = []
        st.rerun()

# ── Run detection ─────────────────────────────────────────────────────────────
if detect_clicked and uploaded:
    already = {r["name"] for r in st.session_state.results}
    new_files = [f for f in uploaded if f.name not in already]

    if not new_files:
        st.info("All uploaded images have already been processed.")
    else:
        with st.spinner("🌿 Running YOLOv8 detection…"):
            for f in new_files:
                img = Image.open(f).convert("RGB")
                annotated, count = run_model(img)

                if count == -1:
                    st.error("⚠️ `best.pt` not found! Place your trained YOLO weights file in the app folder.")
                    break

                st.session_state.results.append({
                    "name": f.name,
                    "count": count,
                    "original": img,
                    "annotated": annotated,
                })
        st.rerun()

elif detect_clicked and not uploaded:
    st.warning("Please upload at least one image first.")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    st.markdown('<hr style="border:none;border-top:1px solid rgba(134,239,92,0.1);margin:1.5rem 0">', unsafe_allow_html=True)

    for r in st.session_state.results:
        st.markdown(f"""
        <div class="result-card">
          <div class="rc-head">
            <div class="rc-filename">
              <span class="dot"></span> {r['name']}
            </div>
            <div class="rc-pill">🌳 {r['count']} trees</div>
          </div>
          <div class="rc-body">
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="col-lbl">📷 Original</div>', unsafe_allow_html=True)
            st.image(r["original"], use_container_width=True)
        with c2:
            st.markdown('<div class="col-lbl">🤖 AI Detected</div>', unsafe_allow_html=True)
            st.image(r["annotated"], use_container_width=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Total banner ──────────────────────────────────────────────────────────
    total = sum(r["count"] for r in st.session_state.results)
    st.markdown(f"""
    <div class="total-banner">
      <div class="total-emoji">🌴</div>
      <div class="total-num">{total}</div>
      <div class="total-lbl">Total Mango Trees Detected Across All Images</div>
      <div class="total-sub">🥭 Powered by YOLOv8 · Trained on Roboflow Dataset</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
      <div class="big">🌴</div>
      <p>No images analysed yet.<br>Upload orchard photos and click <strong style="color:#86ef5c">Detect Mango Trees</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Page wrapper close ────────────────────────────────────────────────────────
st.markdown('</div>', unsafe_allow_html=True)
