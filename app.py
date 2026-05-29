import streamlit as st
import pandas as pd

# -------------------------------------------
# 2025.10.25 プレイヤー名入力対応版
# -------------------------------------------

# -------------------------
# CSSで number_input の数字を大きく
# -------------------------
st.markdown("""
<style>
input[type=number] {
    font-size: 24px !important;
}

table.dataframe {
    border-collapse: collapse;
    width: 100%;
}

/* 数字セル */
table.dataframe td {
    font-size: 20px;
    text-align: center;
    background-color: #f0fff4;
    color: black;
    padding: 6px 8px;
}

/* 合計行 */
table.dataframe tr:last-child td {
    background-color: #fff3b0;
    font-weight: bold;
}

/* ヘッダー */
table.dataframe th {
    font-size: 16px;
    background-color:#f5deb3;
    text-align: center;
    padding: 6px 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# タイトル表示
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
    <h1 style='font-size:28px; color:#00796b; margin:0; line-height:1;'>
    🏌️‍♂️イーグル会ベット計算機🏌️‍♂️
    </h1>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------
# プレイヤー名入力
# -------------------------
st.subheader("👤 プレイヤー名")

players = [
    st.text_input("プレイヤー1", "菅井"),
    st.text_input("プレイヤー2", "辻"),
    st.text_input("プレイヤー3", "木村"),
    st.text_input("プレイヤー4", "霜田")
]

st.divider()

# -------------------------
# 結果用データフレーム
# -------------------------
categories = ["優勝", "ベスト", "ドラニヤ", "バーディ", "ストローク"]
results = pd.DataFrame(0, index=categories, columns=players)

# -------------------------
# 優勝
# -------------------------
st.subheader("🏆 優勝（1000）")

winner_victory = st.radio("優勝者を選択", players)

for p in players:
    results.loc["優勝", p] = 1000 * 3 if p == winner_victory else -1000

# -------------------------
# ベスト・ドラニヤ・バーディ
# -------------------------
awards = [
    ("ベスト", 200),
    ("ドラニヤ", 300),
    ("バーディ", 500)
]

for cat, value in awards:

    st.subheader(f"{cat}（単価 {value}）")

    inputs = [
        st.number_input(
            f"{p} の {cat} 数",
            min_value=0,
            value=0
        )
        for p in players
    ]

    for i, p in enumerate(players):

        others_sum = sum(inputs) - inputs[i]

        results.loc[cat, p] = (
            (inputs[i] * 3 - others_sum) * value
        )

# -------------------------
# ストローク
# -------------------------
st.subheader("⛳ ストローク（単価100）")

scores = [
    st.number_input(
        f"{p} のスコア",
        min_value=0,
        value=75
    )
    for p in players
]

for i, p in enumerate(players):

    diff_sum = sum(
        scores[i] - scores[j]
        for j in range(len(players))
        if j != i
    )

    results.loc["ストローク", p] = -diff_sum * 100

# -------------------------
# 合計
# -------------------------
results.loc["合計"] = results.sum()

st.divider()

# -------------------------
# 計算結果
# -------------------------
st.subheader("💰 計算結果")

html_table = results.to_html(
    classes='dataframe table',
    border=1,
    justify='center'
)

html_table = html_table.replace(
    '<table border="1" class="dataframe table">',
    '<table border="1" class="dataframe table" style="text-align:center; background-color:#fff8dc; border-radius:10px;">'
)

st.markdown(html_table, unsafe_allow_html=True)
