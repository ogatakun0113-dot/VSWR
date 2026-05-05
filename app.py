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
    /* クレジット表示用のCSS */
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

# --- タブ分け（VSWR計算を左側に配置） ---
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
        
        # 判定（1.5以下を「良」とする）
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
    else:
        st.warning("Pfには0より大きい値を入力してください。")

# --- 2. 波長・ケーブル長計算タブ ---
with tab2:
    st.subheader("📏 波長(λ)および同軸長計算")
    
    # 周波数入力
    freq = st.number_input("使用周波数 (MHz)", value=71.790, format="%.3f")
    # 短縮率入力（10D-2V等の特性）
    velocity_factor = st.number_input("同軸短縮率 (例: 10D-2Vは0.67)", value=0.67, format="%.2f")

    if freq > 0:
        # 自由空間波長 λ = 300 / f
        lambda_free = 300 / freq
        # 同軸内波長 = λ * 短縮率
        lambda_coax = lambda_free * velocity_factor

        st.markdown("---")
        st.write("### 波長計算結果（自由空間 / 同軸内）")
        
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
        st.info("反射波を抑えるため、同軸内1/2λの整数倍が望ましいです。")
        
        # 整数倍の計算
        n = st.number_input("倍数を選択 (n倍)", value=12, step=1)
        recommended_len = (lambda_coax / 2) * n
        
        st.success(f"推奨ケーブル長 ({n}倍): **{recommended_len:.3f} m**")
