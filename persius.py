import pandas as pd
import matplotlib.pyplot as plt

# ====== 1) LOAD DATA ======
# แก้ชื่อไฟล์ตรงนี้
df = pd.read_csv("pertussis_2012_2025.csv")

print(df.head())
print(df.columns)

# ====== 2) FIX DATE COLUMN ======
# แก้ชื่อคอลัมน์วันที่ให้ตรงกับของมึง เช่น 'date' / 'report_date' / 'week' / 'month'
DATE_COL = "date"
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
df = df.dropna(subset=[DATE_COL])

# แก้ชื่อคอลัมน์จำนวนเคส เช่น 'cases' / 'count'
CASE_COL = "cases"

# ====== 3) TREND BY YEAR ======
df["year"] = df[DATE_COL].dt.year
yearly = df.groupby("year")[CASE_COL].sum().reset_index()

plt.figure()
plt.plot(yearly["year"], yearly[CASE_COL], marker="o")
plt.title("Pertussis Cases by Year (2012–2025)")
plt.xlabel("Year")
plt.ylabel("Cases")
plt.grid(True)
plt.tight_layout()
plt.savefig("01_trend_year.png", dpi=200)
plt.show()

# ====== 4) SEASONALITY BY MONTH (ถ้ามีข้อมูลระดับวัน/เดือน) ======
df["month"] = df[DATE_COL].dt.month
monthly_avg = df.groupby("month")[CASE_COL].mean().reset_index()

plt.figure()
plt.plot(monthly_avg["month"], monthly_avg[CASE_COL], marker="o")
plt.title("Average Cases by Month (Seasonality)")
plt.xlabel("Month")
plt.ylabel("Avg cases")
plt.grid(True)
plt.tight_layout()
plt.savefig("02_seasonality_month.png", dpi=200)
plt.show()

# ====== 5) MOVING AVERAGE (ทำ Forecast แบบสถิติ) ======
# รวมเป็นรายเดือนก่อน
df["ym"] = df[DATE_COL].dt.to_period("M").astype(str)
monthly = df.groupby("ym")[CASE_COL].sum().reset_index()
monthly["ym"] = pd.to_datetime(monthly["ym"])
monthly = monthly.sort_values("ym")

monthly["ma_3"] = monthly[CASE_COL].rolling(3).mean()

plt.figure()
plt.plot(monthly["ym"], monthly[CASE_COL], label="Monthly cases")
plt.plot(monthly["ym"], monthly["ma_3"], label="3-mo moving avg")
plt.title("Monthly Cases + Moving Average")
plt.xlabel("Month")
plt.ylabel("Cases")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("03_monthly_ma.png", dpi=200)
plt.show()

# ====== 6) OPTIONAL: AGE GROUP (ถ้ามี) ======
# แก้ชื่อคอลัมน์อายุ/ช่วงอายุ เช่น 'age_group'
AGE_COL = "age_group"
if AGE_COL in df.columns:
age_sum = df.groupby(AGE_COL)[CASE_COL].sum().sort_values(ascending=False)

plt.figure()
age_sum.plot(kind="bar")
plt.title("Cases by Age Group")
plt.xlabel("Age group")
plt.ylabel("Cases")
plt.tight_layout()
plt.savefig("04_age_group.png", dpi=200)
plt.show()

print("Saved graphs: 01_trend_year.png, 02_seasonality_month.png, 03_monthly_ma.png (+04_age_group.png if available)")
