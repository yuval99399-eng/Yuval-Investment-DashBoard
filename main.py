import streamlit as st
import yfinance as yf
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="S&P 500 Survivors Tracker", layout="wide")

st.title("📊 מעקב חברות ה-S&P 500 המקוריות")
st.markdown("""
אפליקציה זו עוקבת אחרי 53 החברות ששרדו במדד מאז הקמתו ב-1957 ובוחנת את המומנטום שלהן ביחס לממוצע הנע ל-150 יום.
""")

# רשימת הטיקרים
survivors = [
    'MMM', 'ABT', 'ADM', 'MO', 'AEP', 'T', 'BA', 'BMY', 'CPB', 'CAT', 'CVX', 'KO', 'CL', 'COP',
    'ED', 'CSX', 'CVS', 'DE', 'DTE', 'ETN', 'EIX', 'ETR', 'XOM', 'F', 'GE', 'GD', 'GIS',
    'HAL', 'HON', 'HPQ', 'HUM', 'IBM', 'ITW', 'IP', 'JNJ', 'K', 'KMB', 'KR', 'LLY', 'LOW', 
    'MAR', 'MRK', 'MET', 'NSC', 'NUE', 'OXY', 'PEP', 'PFE', 'PPG', 'PG', 'SLB', 'SO', 'SYY'
]

@st.cache_data(ttl=3600)  # שמירת נתונים בזיכרון לשעה כדי למנוע טעינות מיותרות
def get_data():
    data = yf.download(survivors, period="1y", interval="1d")['Close']
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
                    "Diff %": round(((curr - ma) / ma) * 100, 2),
                    "Status": "✅ Above" if curr > ma else "❌ Below"
                })
    return pd.DataFrame(results)

# טעינת הנתונים
with st.spinner('מושך נתונים מ-Yahoo Finance...'):
    df = get_data()

# יצירת מטריקות (Metrics) בצורה יפה
col1, col2, col3 = st.columns(3)
col1.metric("סה\"כ חברות", len(df))
col2.metric("מעל הממוצע", len(df[df['Status'] == "✅ Above"]), delta_color="normal")
col3.metric("מתחת לממוצע", len(df[df['Status'] == "❌ Below"]), delta_color="inverse")

# פיצול לתצוגה בטאבים
tab1, tab2 = st.tabs(["🟢 מעל הממוצע", "🔴 מתחת לממוצע"])

with tab1:
    st.subheader("מניות במומנטום חיובי")
    st.dataframe(df[df['Status'] == "✅ Above"].sort_values("Diff %", ascending=False), use_container_width=True)

with tab2:
    st.subheader("מניות במומנטום שלילי")
    st.dataframe(df[df['Status'] == "❌ Below"].sort_values("Diff %", ascending=True), use_container_width=True)

st.divider()
st.caption("הנתונים נמשכים בזמן אמת באמצעות yfinance.")
