import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression

print("📊 Stock Prediction System")

# ✅ Available stocks list
stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "SBIN.NS","HINDUNILVR.NS","ITC.NS","LT.NS","KOTAKBANK.NS",
    "AXISBANK.NS","ASIANPAINT.NS","MARUTI.NS","BAJFINANCE.NS",
    "BHARTIARTL.NS","HCLTECH.NS","ULTRACEMCO.NS","SUNPHARMA.NS",
    "TITAN.NS","WIPRO.NS"
]

# 👉 Show available stocks
print("\nAvailable Stocks:")
for s in stocks:
    print(s)

# 👉 User input
user_stock = input("\nEnter stock name from above list: ").upper()

# Validate stock
if user_stock not in stocks:
    print("❌ Invalid stock name. Please choose from list.")
else:
    try:
        print("\nProcessing:", user_stock)

        # Fetch data
        data = yf.download(user_stock, period="6mo", interval="1d")

        if data.empty or len(data) < 3:
            print("❌ Not enough data")
        else:
            data = data[['Close']].copy()

            data['Prediction'] = data['Close'].shift(-1)
            data = data.dropna()

            X = data[['Close']]
            y = data['Prediction']

            model = LinearRegression()
            model.fit(X, y)

            # Get values
            yesterday = float(data['Close'].iloc[-2])
            today = float(data['Close'].iloc[-1])

            latest_df = pd.DataFrame([[today]], columns=['Close'])
            tomorrow = float(model.predict(latest_df)[0])

            growth = ((tomorrow - today) / today) * 100

            print("\n📈 RESULT:\n")
            print("Stock:", user_stock)
            print("Yesterday:", round(yesterday, 2))
            print("Today:", round(today, 2))
            print("Tomorrow (Predicted):", round(tomorrow, 2))
            print("Growth %:", round(growth, 2))

    except Exception as e:
        print("Error:", e)