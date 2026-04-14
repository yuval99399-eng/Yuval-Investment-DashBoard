# התקנת הספרייה למשיכת נתונים (חובה בקולאב)
!pip install yfinance

import yfinance as yf
import pandas as pd
from datetime import datetime

# רשימת 53 החברות ששרדו במדד מ-1957 (או גלגוליהן המודרניים)
survivors = [
    'MMM', 'ABT', 'ADM', 'MO', 'AEP', 'T', 'BA', 'BMY', 'CPB', 'CAT', 'CVX', 'KO', 'CL', 'COP',
    'ED', 'CSX', 'CVS', 'DE', 'DTE', 'ETN', 'EIX', 'ETR', 'XOM', 'F', 'GE', 'GD', 'GIS',
    'HAL', 'HON', 'HPQ', 'HUM', 'IBM', 'ITW', 'IP', 'JNJ', 'K', 'KMB', 'KR', 'LLY', 'LOW', 
    'MAR', 'MRK', 'MET', 'NSC', 'NUE', 'OXY', 'PEP', 'PFE', 'PPG', 'PG', 'SLB', 'SO', 'SYY'
]

print("מתחיל במשיכת נתונים וניתוח טכני... זה עשוי לקחת רגע.")

# משיכת נתוני סגירה (Close) לשנה האחרונה עבור כל הרשימה
data = yf.download(survivors, period="1y", interval="1d", progress=True)['Close']

results = []

for ticker in survivors:
    if ticker in data.columns:
        # ניקוי ערכים חסרים וחישוב ממוצע נע
        series = data[ticker].dropna()
        if len(series) >= 150:
            current_price = series.iloc[-1]
            ma150 = series.rolling(window=150).mean().iloc[-1]
            diff_percent = ((current_price - ma150) / ma150) * 100
            
            results.append({
                'Ticker': ticker,
                'Price': round(current_price, 2),
                'MA150': round(ma150, 2),
                'Diff %': round(diff_percent, 2),
                'Status': 'Above' if current_price > ma150 else 'Below'
            })

# יצירת DataFrame לסיכום התוצאות
df = pd.DataFrame(results)

# הפרדה לשתי קבוצות
above = df[df['Status'] == 'Above'].sort_values(by='Diff %', ascending=False)
below = df[df['Status'] == 'Below'].sort_values(by='Diff %', ascending=True)

print("\n" + "="*50)
print(f"סיכום: {len(above)} חברות מעל הממוצע, {len(below)} חברות מתחת לממוצע.")
print("="*50)

print("\n--- חברות שנסחרות מעל ממוצע 150 (החזקות ביותר) ---")
print(above[['Ticker', 'Price', 'MA150', 'Diff %']].head(10))

print("\n--- חברות שנסחרות מתחת לממוצע 150 (החלשות ביותר) ---")
print(below[['Ticker', 'Price', 'MA150', 'Diff %']].head(10))
