import requests
import pandas as pd
import csv
import json

# مفتاح API
api_key = "94blYlq8123gTt271njG0jTYaiLPJLTN"
symbol = "AAPL"
start_date = "2024-09-26"
end_date = "2025-01-11"

# URL للحصول على البيانات اليومية
url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={api_key}"

# تنزيل البيانات
response = requests.get(url)
data = response.json()
results = data["results"]


with open("E:\Task6\Stock_data_test.csv", "w", newline="") as csvfile:
    fieldnames = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "change",
        "previous_close",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # كتابة أسماء الأعمدة
    writer.writeheader()

    # المتغير لتتبع الإغلاق السابق
    previous_close = None

    for entry in results:
        date = entry["t"] // 1000  # التحويل إلى Timestamp بالثواني
        open_price = entry.get("o")
        high_price = entry.get("h")
        low_price = entry.get("l")
        close_price = entry.get("c")
        volume = entry.get("v")

        # حساب التغيير
        change = None
        if previous_close is not None:
            change = close_price - previous_close

        # كتابة الصف في الملف
        writer.writerow(
            {
                "date": date,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
                "change": change,
                "previous_close": previous_close,
            }
        )

        # تحديث الإغلاق السابق
        previous_close = close_price


df = pd.read_csv("E:/Task6/Stock_data_test.csv")
df["true_range"] = df.apply(
    lambda row: max(
        row["high"] - row["low"],
        abs(row["high"] - row["previous_close"]),
        abs(row["low"] - row["previous_close"]),
    ),
    axis=1,
)
حساب OBV
df["OBV"] = 0
df.loc[1:, "OBV"] = (
    df.loc[1:, ["close", "previous_close", "volume"]]
    .apply(
        lambda x: (
            x["volume"]
            if x["close"] > x["previous_close"]
            else -x["volume"] if x["close"] < x["previous_close"] else 0
        ),
        axis=1,
    )
    .cumsum()
)
df["OBV_Moving14"] = df["OBV"].rolling(window=14).mean()
# حفظ البيانات مع العمود الجديد
df.to_csv("E:/Task6/Stock_data_test.csv", index=False)
