import streamlit as st
import math

# --- ページ設定（スマホ・PC両対応） ---
st.set_page_config(page_title="VSWR計算", layout="centered")

# --- 見た目のカスタマイズ（CSS） ---
st.markdown("""
    <style>
    .main {
        padding: 10px;
    }
    .stNumberInput label {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #2E86C1;
    }
    /* Pf入力枠（薄赤） */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) input {
        background-color: #fdf2f2 !important;
        border-left: 5px solid #ff4b4b !important;
        font-weight: bold !important;
    }
    /* Pr入力枠（薄青） */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) input {
        background-color: #f2f2fd !important;
        border-left: 5px solid #007bff !important;
        font-weight: bold !important;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        margin-bottom: 20px;
    }
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
    }
    .credit {
        text-align: right;
        font-size: 14px;
        color: #666;
        margin-bottom: -20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title("📡 VSWR計算")

# --- タブ分け ---
tab1, tab2 = st.tabs(["VSWR計算", "波長・ケーブル長計算"])

# --- 1. VSWR計算タブ ---
with tab1:
    st.subheader("📊 VSWR測定・判定")
    
    col1, col2 = st.columns(2)
    with col1:
        # 前進電力 Pf
        pf = st.number_input("前進電力 Pf (W)", value=3.96, format="%.2f")
    with col2:
        # 反射電力 Pr
        pr = st.number_input("反射電力 Pr (W)", value=0.03, format="%.2f")
    
    if pf > 0:
        # VSWRの計算
        rho = math.sqrt(pr / pf)
        vswr = (1 + rho) / (1 - rho) if rho < 1 else float('inf')
        
        # 判定
        is_good = vswr < 1.5
        status = "良" if is_good else "要調整"
        color = "green" if is_good else "red"
        
        st.markdown(f"""
        <div class="result-box">
            <p style="margin-bottom:0;">計算結果</p>
            <h2 style="color:{color}; margin-top:0;">判定：{status}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("VSWR", f"{vswr:.3f}")

        # --- 計算式の表示と凡例 ---
        st.markdown("---")
        st.write("### 📝 VSWR計算式")
        st.latex(r"VSWR = \frac{1 + \sqrt{P_r / P_f}}{1 - \sqrt{P_r / P_f}}")
        
        # 指示の凡例表示
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
            <p style="margin: 0; font-size: 16px;"><strong>【凡例】</strong></p>
            <ul style="margin: 5px 0 0 0; font-size: 15px;">
                <li><strong><span style="color: #ff4b4b;">P<sub>f</sub></span></strong> ：前進電力 (Forward Power)</li>
                <li><strong><span style="color: #007bff;">P<sub>r</sub></span></strong> ：反射電力 (Reflected Power)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Pfには0より大きい値を入力してください。")

# --- 2. 波長・ケーブル長計算タブ ---
with tab2:
    st.subheader("📏 波長(λ)および同軸長計算")
    
    freq = st.number_input("使用周波数 (MHz)", value=71.790, format="%.3f")
    velocity_factor = st.number_input("同軸短縮率 (例: 10D-2Vは0.67)", value=0.67, format="%.2f")

    if freq > 0:
        lambda_free = 300 / freq
        lambda_coax = lambda_free * velocity_factor

        st.markdown("---")
        st.write("### 波長計算結果")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("**1λ**")
            st.write(f"{lambda_free:.3f} m")
            st.write(f"({lambda_coax:.3f} m)")
        with c2:
            st.write("**1/2λ**")
            st.write(f"{lambda_free/2:.3f} m")
            st.write(f"({lambda_coax/2:.3f} m)")
        with c3:
            st.write("**1/4λ**")
            st.write(f"{lambda_free/4:.3f} m")
            st.write(f"({lambda_coax/4:.3f} m)")

        st.markdown("---")
        st.write("### 同軸ケーブル推奨長")
        n = st.number_input("倍数を選択 (n倍)", value=12, step=1)
        recommended_len = (lambda_coax / 2) * n
        st.success(f"推奨ケーブル長 ({n}倍): **{recommended_len:.3f} m**")

# --- 戻るボタン ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.link_button("🏠\n\n戻る", "https://7fjndw39dicdzckugyepb2.streamlit.app/", use_container_width=True)

st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important;
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
