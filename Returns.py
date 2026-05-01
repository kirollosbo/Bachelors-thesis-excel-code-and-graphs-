import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthEnd

# =========================================================
# FYLL I EXAKT 10 ETF:ER PER MÅNAD
# side = "long" eller "short"
# =========================================================
monthly_positions = [  #Viktad 2017 		
#{"month": "2017-01", "ticker": "Ticker name", "side": "long or short"},

# 2017-01 (från 2016-12-29)
{"month": "2017-01", "ticker": "EMB", "side": "long"},
{"month": "2017-01", "ticker": "EWG", "side": "long"},
{"month": "2017-01", "ticker": "CPER", "side": "short"},
{"month": "2017-01", "ticker": "TIP", "side": "long"},
{"month": "2017-01", "ticker": "SCHP", "side": "long"},
{"month": "2017-01", "ticker": "SCJ", "side": "long"},
{"month": "2017-01", "ticker": "IAU", "side": "long"},
{"month": "2017-01", "ticker": "EWZ", "side": "long"},
{"month": "2017-01", "ticker": "AGG", "side": "long"},
{"month": "2017-01", "ticker": "BSV", "side": "long"},

# 2017-02
{"month": "2017-02", "ticker": "FXB", "side": "long"},
{"month": "2017-02", "ticker": "URA", "side": "long"},
{"month": "2017-02", "ticker": "FXA", "side": "long"},
{"month": "2017-02", "ticker": "SLV", "side": "long"},
{"month": "2017-02", "ticker": "USO", "side": "short"},
{"month": "2017-02", "ticker": "ACWI", "side": "long"},
{"month": "2017-02", "ticker": "URTH", "side": "long"},
{"month": "2017-02", "ticker": "EWJ", "side": "long"},
{"month": "2017-02", "ticker": "EWU", "side": "long"},
{"month": "2017-02", "ticker": "FXC", "side": "long"},

# 2017-03
{"month": "2017-03", "ticker": "SPY", "side": "long"},
{"month": "2017-03", "ticker": "IVV", "side": "long"},
{"month": "2017-03", "ticker": "IGIB", "side": "long"},
{"month": "2017-03", "ticker": "BSV", "side": "long"},
{"month": "2017-03", "ticker": "EMB", "side": "long"},
{"month": "2017-03", "ticker": "AGG", "side": "long"},
{"month": "2017-03", "ticker": "SCJ", "side": "long"},
{"month": "2017-03", "ticker": "IBB", "side": "long"},
{"month": "2017-03", "ticker": "FXE", "side": "short"},
{"month": "2017-03", "ticker": "ACWI", "side": "long"},

# 2017-04
{"month": "2017-04", "ticker": "SPY", "side": "short"},
{"month": "2017-04", "ticker": "EWG", "side": "long"},
{"month": "2017-04", "ticker": "UNG", "side": "long"},
{"month": "2017-04", "ticker": "FXF", "side": "long"},
{"month": "2017-04", "ticker": "FXE", "side": "long"},
{"month": "2017-04", "ticker": "IVV", "side": "short"},
{"month": "2017-04", "ticker": "IBB", "side": "short"},
{"month": "2017-04", "ticker": "EWI", "side": "long"},
{"month": "2017-04", "ticker": "EWQ", "side": "long"},
{"month": "2017-04", "ticker": "XBI", "side": "short"},

# 2017-05
{"month": "2017-05", "ticker": "IWM", "side": "long"},
{"month": "2017-05", "ticker": "VTWO", "side": "long"},
{"month": "2017-05", "ticker": "VGK", "side": "long"},
{"month": "2017-05", "ticker": "UUP", "side": "short"},
{"month": "2017-05", "ticker": "SLV", "side": "short"},
{"month": "2017-05", "ticker": "EWA", "side": "short"},
{"month": "2017-05", "ticker": "FXB", "side": "long"},
{"month": "2017-05", "ticker": "FXE", "side": "long"},
{"month": "2017-05", "ticker": "SPY", "side": "long"},
{"month": "2017-05", "ticker": "VTI", "side": "long"},

# 2017-06
{"month": "2017-06", "ticker": "LQD", "side": "long"},
{"month": "2017-06", "ticker": "UNG", "side": "short"},
{"month": "2017-06", "ticker": "IWM", "side": "short"},
{"month": "2017-06", "ticker": "VTWO", "side": "short"},
{"month": "2017-06", "ticker": "USO", "side": "long"},
{"month": "2017-06", "ticker": "FXB", "side": "short"},
{"month": "2017-06", "ticker": "FXI", "side": "long"},
{"month": "2017-06", "ticker": "MCHI", "side": "long"},
{"month": "2017-06", "ticker": "EEM", "side": "long"},
{"month": "2017-06", "ticker": "FXC", "side": "long"},

# 2017-07
{"month": "2017-07", "ticker": "XBI", "side": "long"},
{"month": "2017-07", "ticker": "EWA", "side": "long"},
{"month": "2017-07", "ticker": "IBB", "side": "long"},
{"month": "2017-07", "ticker": "EWC", "side": "long"},
{"month": "2017-07", "ticker": "FXY", "side": "short"},
{"month": "2017-07", "ticker": "FXC", "side": "long"},
{"month": "2017-07", "ticker": "FXA", "side": "long"},
{"month": "2017-07", "ticker": "INDA", "side": "short"},
{"month": "2017-07", "ticker": "TIP", "side": "short"},
{"month": "2017-07", "ticker": "SCHP", "side": "short"},

# 2017-08
{"month": "2017-08", "ticker": "SPY", "side": "long"},
{"month": "2017-08", "ticker": "SHY", "side": "long"},
{"month": "2017-08", "ticker": "EWZ", "side": "long"},
{"month": "2017-08", "ticker": "EWC", "side": "long"},
{"month": "2017-08", "ticker": "EWA", "side": "long"},
{"month": "2017-08", "ticker": "IVV", "side": "long"},
{"month": "2017-08", "ticker": "FXE", "side": "long"},
{"month": "2017-08", "ticker": "FXY", "side": "long"},
{"month": "2017-08", "ticker": "FXF", "side": "short"},
{"month": "2017-08", "ticker": "FXA", "side": "long"},

# 2017-09
{"month": "2017-09", "ticker": "EWU", "side": "short"},
{"month": "2017-09", "ticker": "TLT", "side": "long"},
{"month": "2017-09", "ticker": "AGG", "side": "long"},
{"month": "2017-09", "ticker": "EMB", "side": "long"},
{"month": "2017-09", "ticker": "BSV", "side": "long"},
{"month": "2017-09", "ticker": "EWJ", "side": "short"},
{"month": "2017-09", "ticker": "IEF", "side": "long"},
{"month": "2017-09", "ticker": "QQQ", "side": "short"},
{"month": "2017-09", "ticker": "UUP", "side": "long"},
{"month": "2017-09", "ticker": "UNG", "side": "long"},

# 2017-10
{"month": "2017-10", "ticker": "WEAT", "side": "long"},
{"month": "2017-10", "ticker": "SLV", "side": "short"},
{"month": "2017-10", "ticker": "SCHP", "side": "short"},
{"month": "2017-10", "ticker": "FXF", "side": "short"},
{"month": "2017-10", "ticker": "FXB", "side": "long"},
{"month": "2017-10", "ticker": "FXE", "side": "short"},
{"month": "2017-10", "ticker": "UUP", "side": "long"},
{"month": "2017-10", "ticker": "IGIB", "side": "short"},
{"month": "2017-10", "ticker": "FXI", "side": "short"},
{"month": "2017-10", "ticker": "VWO", "side": "short"},

# 2017-11
{"month": "2017-11", "ticker": "XBI", "side": "short"},
{"month": "2017-11", "ticker": "EWD", "side": "short"},
{"month": "2017-11", "ticker": "EWA", "side": "long"},
{"month": "2017-11", "ticker": "EWZ", "side": "short"},
{"month": "2017-11", "ticker": "INDA", "side": "long"},
{"month": "2017-11", "ticker": "ICLN", "side": "long"},
{"month": "2017-11", "ticker": "EWJ", "side": "long"},
{"month": "2017-11", "ticker": "EWU", "side": "short"},
{"month": "2017-11", "ticker": "EMB", "side": "short"},
{"month": "2017-11", "ticker": "IBB", "side": "short"},

# 2017-12
{"month": "2017-12", "ticker": "FXE", "side": "long"},
{"month": "2017-12", "ticker": "FXY", "side": "long"},
{"month": "2017-12", "ticker": "IAU", "side": "long"},
{"month": "2017-12", "ticker": "FXF", "side": "long"},
{"month": "2017-12", "ticker": "URA", "side": "long"},
{"month": "2017-12", "ticker": "GLD", "side": "long"},
{"month": "2017-12", "ticker": "FXI", "side": "long"},
{"month": "2017-12", "ticker": "MCHI", "side": "long"},
{"month": "2017-12", "ticker": "VWO", "side": "long"},
{"month": "2017-12", "ticker": "EEM", "side": "long"},

]

def get_month_start_end(month_str: str):
    start = pd.Timestamp(f"{month_str}-01")
    end = start + MonthEnd(1)
    return start, end

def get_month_return(ticker: str, month_str: str) -> float:
    start, end = get_month_start_end(month_str)

    data = yf.download(
        ticker,
        start=(start - pd.Timedelta(days=10)).strftime("%Y-%m-%d"), 
        end=(end + pd.Timedelta(days=2)).strftime("%Y-%m-%d"),
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"Ingen data för {ticker} under {month_str}")

    close = data["Close"].dropna()

    # sista priset innan månaden börjar
    prev_close = close[close.index < start]
    if prev_close.empty:
        raise ValueError(f"Kan inte hitta pris före {month_str} för {ticker}")
    prev_close = float(prev_close.iloc[-1])

    # samma idé men säkrar att vi tar sista i månaden
    last_close = close[close.index <= end]
    if last_close.empty:
        raise ValueError(f"Kan inte hitta slutpris i {month_str} för {ticker}")
    last_close = float(last_close.iloc[-1])

    return (last_close / prev_close) - 1


positions_df = pd.DataFrame(monthly_positions)
positions_df["side"] = positions_df["side"].str.lower().str.strip()

required_cols = {"month", "ticker", "side"}
missing = required_cols - set(positions_df.columns)
if missing:
    raise ValueError(f"Saknade kolumner: {missing}")

if not positions_df["side"].isin(["long", "short"]).all():
    invalid = positions_df.loc[~positions_df["side"].isin(["long", "short"]), "side"].unique()
    raise ValueError(f"Ogiltiga värden i 'side': {invalid}")

counts = positions_df.groupby("month")["ticker"].count()
invalid_months = counts[counts != 10]

if not invalid_months.empty:
    raise ValueError(
        "Följande månader har inte exakt 10 ETF:er:\n"
        + invalid_months.to_string()
    )

# 10 ETF:er = 10 % vikt per ETF
positions_df["weight"] = 0.10
results = []


for _, row in positions_df.iterrows():
    month = row["month"]
    ticker = row["ticker"]
    side = row["side"]
    weight = row["weight"]

    raw_return = get_month_return(ticker, month)
    position_return = raw_return if side == "long" else -raw_return
    contribution = position_return * weight

    results.append({
        "month": month,
        "ticker": ticker,
        "side": side,
        "weight": weight,
        "etf_return": raw_return,
        "position_return": position_return,
        "portfolio_contribution": contribution,
    })

results_df = pd.DataFrame(results).sort_values(["month", "ticker"]).reset_index(drop=True)

monthly_portfolio = (
    results_df.groupby("month", as_index=False)["portfolio_contribution"]
    .sum()
    .rename(columns={"portfolio_contribution": "portfolio_return"})
    .sort_values("month")
    .reset_index(drop=True)
)

monthly_portfolio["portfolio_value"] = (1 + monthly_portfolio["portfolio_return"]).cumprod()
monthly_portfolio["cumulative_return"] = monthly_portfolio["portfolio_value"] - 1


pd.set_option("display.float_format", lambda x: f"{x:.2%}")

print("\n=== RESULTAT PER ETF ===")
print(results_df[[
    "month",
    "ticker",
    "side",
    "weight",
    "etf_return",
    "position_return",
    "portfolio_contribution"
]])

print("\n=== PORTFÖLJ PER MÅNAD ===")
print(monthly_portfolio)

total_return = monthly_portfolio["cumulative_return"].iloc[-1]
print(f"\n=== TOTAL AVKASTNING FÖR ÅRET: {total_return:.2%} ===")

# =========================================================
# GRAF
# =========================================================
plt.figure(figsize=(10, 5))
plt.plot(monthly_portfolio["month"], monthly_portfolio["portfolio_value"], marker="o")
plt.xticks(rotation=45)
plt.xlabel("Månad")
plt.ylabel("Portföljvärde")
plt.title("Portföljens utveckling över året")
plt.tight_layout()
plt.show()

results_df.to_csv("resultat.csv", index=False)