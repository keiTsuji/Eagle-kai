import streamlit as st
import pandas as pd

# -------------------------
# CSSで number_input の数字を大きく
# -------------------------
st.markdown("""
<style>
input[type=number] {
    font-size: 24px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# タイトル表示（装飾あり）
# -------------------------
st.markdown("""
<div style='
    display:flex;
    justify-content:center;
    align-items:center;
    height:120px;
    background-color:#e0f7fa;
    border-radius:15px;
'>
    <h1 style='font-size:28px; color:#00796b; margin:0; line-height:1;'>🏌️‍♂️イーグル会ベット計算機🏌️‍♂️</h1>
</div>
""", unsafe_allow_html=True)


# プレイヤー名入力
st.header("プレイヤー名の入力")
players = [st.text_input(f"プレイヤー{i+1}の名前", f"Player{i+1}") for i in range(4)]

st.divider()

# 結果用のデータフレーム作成
categories = ["優勝", "ベスト", "ドラニヤ", "バーディ", "ストローク"]
results = pd.DataFrame(0, index=categories, columns=players)

# 1️⃣ 優勝
st.subheader("優勝（500円）")
winner_victory = st.radio("優勝の勝者を選択", players)
for p in players:
    results.loc["優勝", p] = 500*3 if p == winner_victory else -500

# 2️⃣ ベスト・ドラニヤ・バーディ
awards = [("ベスト", 200), ("ドラニヤ", 300), ("バーディ", 500)]
for cat, value in awards:
    st.subheader(f"{cat}（単価 {value}円）")
    inputs = [st.number_input(f"{p} の {cat} 数字", min_value=0, value=0) for p in players]

    for i, p in enumerate(players):
        others_sum = sum(inputs) - inputs[i]
        results.loc[cat, p] = (inputs[i]*3 - others_sum) * value

# ストローク
st.subheader("ストローク（単価100円）")
scores = [st.number_input(f"{p} のスコア", min_value=0, value=0) for p in players]

for i, p in enumerate(players):
    diff_sum = sum(scores[i] - scores[j] for j in range(len(players)) if j != i)
    results.loc["ストローク", p] = -diff_sum * 100  # 高スコアはマイナス

# 合計
results.loc["合計"] = results.sum()

st.divider()
st.subheader("💰 計算結果")

# =========================
# ✅ 数字に色をつける関数
# =========================
def color_values(val):
    if val > 0:
        color = '#2e7d32'  # 緑
    elif val < 0:
        color = '#c62828'  # 赤
    else:
        color = '#555555'  # グレー
    return f'color: {color}; font-weight:bold;'

# =========================
# 表示（色付き）
# =========================
st.dataframe(results.style.applymap(color_values).format("{:+,}"))

# CSVダウンロード
csv = results.to_csv(index=True).encode("utf-8-sig")
st.download_button(
    label="📥 結果をCSVでダウンロード",
    data=csv,
    file_name="eagle_bet_result.csv",
    mime="text/csv"
)
