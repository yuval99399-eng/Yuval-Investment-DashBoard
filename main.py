import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# הגדרות דף ועיצוב RTL בסיסי
st.set_page_config(page_title="S&P 500 Survivors Tracker", layout="wide")

# הוספת CSS ליישור לימין (RTL)
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div.stSelectbox > label { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 מעקב חברות ה-S&P 500 - תצוגה גרפית")

# רשימת הטיקרים
survivors = sorted([
    'MMM', 'ABT', 'ADM', 'MO', 'AEP', 'T', 'BA', 'BMY', 'CPB', 'CAT', 'CVX', 'KO', 'CL', 'COP',
    'ED', 'CSX', 'CVS', 'DE', 'DTE', 'ETN', 'EIX', 'ETR', 'XOM', 'F', 'GE', 'GD', 'GIS',
    'HAL', 'HON', 'HPQ', 'HUM', 'IBM', 'ITW', 'IP', 'JNJ', 'K', 'KMB', 'KR', 'LLY', 'LOW', 
    'MAR', 'MRK', 'MET', 'NSC', 'NUE', 'OXY', 'PEP', 'PFE', 'PPG', 'PG', 'SLB', 'SO', 'SYY'
])

# פונקציה למשיכת נתוני טבלה
@st.cache_data(ttl=3600)
def get_summary_data():
    data = yf.download(survivors, period="1y", interval="1d", progress=False)['Close']
    results = []
    for ticker in survivors:
        if ticker in data.columns:
            series = data[ticker].dropna()
            if len(series) >= 150:
                curr = series.iloc[-1]
                ma = series.rolling(window=150).mean().iloc[-1]
                results.append({
                    "Ticker": ticker,
                    "Price": round(curr, 2),
                    "MA150": round(ma, 2),
                    "Status": "✅ Above" if curr > ma else "❌ Below"
                })
    return pd.DataFrame(results)

df_summary = get_summary_data()

# --- חלק 1: בחירת מניה ותצוגת גרף נרות ---
st.subheader("📈 ניתוח טכני בנרות יפניים")
selected_ticker = st.selectbox("בחר מניה מהרשימה לצפייה בגרף:", survivors)

if selected_ticker:
    # משיכת נתונים מלאים לגרף (Open, High, Low, Close)
    hist = yf.download(selected_ticker, period="1y", interval="1d", progress=False)
    
    # חישוב ממוצע נע 150
    hist['MA150'] = hist['Close'].rolling(window=150).mean()
    
    # יצירת גרף עם Plotly
    fig = go.Figure()

    # הוספת נרות יפניים
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
        name='מחיר נרות'
    ))

    # הוספת קו ממוצע נע 150
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['MA150'],
        line=dict(color='orange', width=2),
        name='ממוצע נע 150'
    ))

    # עיצוב הגרף
    fig.update_layout(
        title=f"גרף יומי - {selected_ticker}",
        yaxis_title="מחיר ($)",
        xaxis_title="תאריך",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- חלק 2: טבלת הסטטוס הכללית ---
st.subheader("📋 סטטוס כללי של כל השורדות")
col1, col2 = st.columns(2)

with col1:
    st.write("**חברות מעל ממוצע 150**")
    st.dataframe(df_summary[df_summary['Status'] == "✅ Above"], use_container_width=True)

with col2:
    st.write("**חברות מתחת לממוצע 150**")
    st.dataframe(df_summary[df_summary['Status'] == "❌ Below"], use_container_width=True)
