import os
from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np
import pandas as pd
import yfinance as yf

# =========================
# CONFIG
# =========================
TICKERS = [ 
# Aktier 
"SPY", "IVV", "VOO",  # S&P 200 (USA, BRED)
"QQQ", #Nasdaq 100 (USA, teknologi)
"IWM", "VTWO", #Russell 2000 (USA, småbolag)
"FEX", #Eurostoxx 20 (smal Europa), US
"VGK",#Eurostoxx 600 (bred Europa), (US, MSCI Europe nära proxy)
"EWD", #(US, MSCI Sweden) OMX (Sverige, OMXS30/OMXSB)
"EWG", #DAX (Tyskland) (US, MSCI Germany proxy)
"EWQ", #CAC 40 FRANKRIKE, (US, MSCI France proxy)
"EWI", #FTSE MIB (Italien), (US, MSCI Italy proxy)
"EWU",  # FTSE 100 (London), (US, MSCI UK proxy)
"EWJ", #TPX / TOPIX (Tokyo) EWJ (US, MSCI Japan proxy)

# Aktier – breda globala och regionala index
"VTI", "ITOT", #Total Stock Market
"URTH", #MSCI World#
"ACWI", #MSCI ACWI#
"EEM", "VWO", #MSCI Emerging Markets#
"MCHI", "FXI", #MSCI China#
"INDA", #MSCI India#
"EWZ", #MSCI Brazil#
"EWL", #MSCI Switzerland#
"EWC", #MSCI Canada#
"EWA", #MSCI Australia#
"SCJ", #MSCI Japan Small Cap#

# Aktier – sektorer och teman
"VNQ",  #Global REIT#
"IBB", "XBI", #Nasdaq Biotechnology#
"ICLN",  #Global Clean Energy#
 
# Valutor
"UUP", #US Dollar#
"FXE", #Euro#
"FXY", #Japanese Yen
"FXB", #British pound
"FXF", #Swiss Franc
"FXC", # Canadian dollar
"FXA", #aUSTRALIAN dOLLAR

# Räntor – USA total och treasury
"BND", #US Total Bond Market
"SHY", #US Treasury 1–3Y
"IEF", #US Treasury 7–10Y
"TLT", #US Treasury 20+Y
"TIP", "SCHP", #US TIPS (inflationsskydd)

# Räntor – företagsobligationer
"LQD", #US Corporate Bonds
"HYG", "JNK", #US High Yield Bonds

# Räntor – globala obligationer
"AGG", "BNDW", #Global Aggregate Bonds

# Räntor – emerging markets
"EMB", #Emerging Market Bonds

# Räntor – kort löptid och investment grade
"BSV", #Short Term Global Bonds
"IGIB", #Investment Grade Global

# Räntor – floating rate
"FLOT", #Floating Rate Bonds

# Råvaror
"GLD", "IAU", #Guld
"SLV", #sILVER
"USO", #Olja(Crude oil)
"UNG", #Energi
"CPER", #Koppar
"URA", #Uran
"WEAT", #Vete
]

START = "2014-01-01"
END = "2025-12-31"           
INTERVAL = "1d"

OUT_DIR = Path("outputs")
DATA_DIR = Path("data")

# Signal- & modellparametrar
Z_WINDOW = 20
HORIZON = 5         # 10 handelsdagar framåt för facit
LOOKBACK = 60         # senaste 60 dagar (med facit) för ranking
BUY_TH = 0.3
SELL_TH = -0.3

# Trend-signal parametrarvj
MA_SHORT = 20
MA_LONG = 60
DONCHIAN_WINDOW = 20
TSMOM_WINDOW = 20
SLOPE_WINDOW = 20
VOLMOM_WINDOW = 20


def ensure_dirs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

import pandas as pd
import yfinance as yf

def download_ohlcv(ticker: str, start: str, end: str | None, interval: str) -> pd.DataFrame:
    df = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False
    )
    if df is None or df.empty:
        raise ValueError(f"Ingen data för {ticker}.")

    if isinstance(df.columns, pd.MultiIndex):
        wanted = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
        new_cols = []
        for col in df.columns:
            # col kan vara tuple med 2 nivåer
            # välj den nivå som matchar wanted, annars slå ihop
            pick = None
            for part in col:
                if part in wanted:
                    pick = part
                    break
            new_cols.append(pick if pick is not None else "_".join([str(x) for x in col]))
        df.columns = new_cols

    df = df.reset_index()  # Date blir kolumn
    if "Date" not in df.columns:
        if "Datetime" in df.columns:
            df = df.rename(columns={"Datetime": "Date"})
        else:
            raise ValueError("Kunde inte hitta datumkolumn efter download.")

    return df

def rolling_zscore(s: pd.Series, window: int) -> pd.Series:
    m = s.rolling(window=window, min_periods=window).mean()
    sd = s.rolling(window=window, min_periods=window).std(ddof=0)
    z = (s - m) / sd
    z = z.replace([np.inf, -np.inf], np.nan)
    return z

def logret(price: pd.Series) -> pd.Series:
    return np.log(price).diff()

def rolling_regression_slope_logprice(price: pd.Series, window: int) -> pd.Series:
    lp = np.log(price).astype(float)
    x = np.arange(window, dtype=float)
    x_mean = x.mean()
    x_demean = x - x_mean
    denom = np.sum(x_demean**2)

    def slope(arr: np.ndarray) -> float:
        y = arr
        y_mean = y.mean()
        num = np.sum(x_demean * (y - y_mean))
        return num / denom if denom != 0 else np.nan

    return lp.rolling(window).apply(lambda a: slope(np.asarray(a, dtype=float)), raw=False)

def compute_signals_5(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["Date"] = pd.to_datetime(d["Date"])
    d = d.sort_values("Date").reset_index(drop=True)

    # Pris för avkastning: Adj Close om finns annars Close
    if "Adj Close" in d.columns:
        price = d["Adj Close"].astype(float)
        price_name = "product_AdjClose"
    else:
        price = d["Close"].astype(float)
        price_name = "product_Close"

    out = pd.DataFrame({"Date": d["Date"]})
    # behåll OHLCV
    for c in ["Adj Close", "Close", "High", "Low", "Volume"]:
        if c in d.columns:
            out[f"product_{c.replace(' ', '')}"] = pd.to_numeric(d[c], errors="coerce")

    # 1) TSMOM (sign av return över window)
    ret_w = price.pct_change(TSMOM_WINDOW)
    out["tsmom_1m"] = np.sign(ret_w).shift(1)

    # 2) MA spread (MA20/MA60 - 1)
    ma_s = price.rolling(MA_SHORT).mean()
    ma_l = price.rolling(MA_LONG).mean()
    out["ma_spread_20_60"] = ((ma_s / ma_l) - 1.0).shift(1)

    # 3) Donchian breakout (0..1)
    if {"High", "Low"}.issubset(d.columns):
        hi = pd.to_numeric(d["High"], errors="coerce").rolling(DONCHIAN_WINDOW).max()
        lo = pd.to_numeric(d["Low"], errors="coerce").rolling(DONCHIAN_WINDOW).min()
    else:
        hi = price.rolling(DONCHIAN_WINDOW).max()
        lo = price.rolling(DONCHIAN_WINDOW).min()

    width = (hi - lo).replace(0, np.nan)
    out["donchian_breakout_20"] = ((price - lo) / width).shift(1)

    # 4) Regression slope (log price), annualiserad
    slope_per_day = rolling_regression_slope_logprice(price, SLOPE_WINDOW)
    out["reg_slope_logprice_20_ann"] = (slope_per_day * 252.0).shift(1)

    # 5) Vol-adjusted momentum
    lr = logret(price)
    vol = lr.rolling(VOLMOM_WINDOW).std(ddof=0)
    logret_w = np.log(price).diff(VOLMOM_WINDOW)
    denom = (vol * np.sqrt(VOLMOM_WINDOW)).replace(0, np.nan)
    out["vol_adj_mom_1m"] = (logret_w / denom).shift(1)

    return out

def normalize_signals(out: pd.DataFrame, window: int) -> pd.DataFrame:
    d = out.copy()

    signal_cols = [
        "tsmom_1m",
        "ma_spread_20_60",
        "donchian_breakout_20",
        "reg_slope_logprice_20_ann",
        "vol_adj_mom_1m",
    ]

    for c in signal_cols:
        s = pd.to_numeric(d[c], errors="coerce")

        # Rank-normalisering
        rank = s.rolling(window).rank(pct=True)
        norm_signal = (rank - 0.5) * 2   # [-1, 1]

        d[f"{c}_z{window}"] = norm_signal

    return d

@dataclass
class Recommendation:
    ticker: str
    date: pd.Timestamp
    final_signal: float
    decision: str

def compute_weighted_recommendation(
    df_norm: pd.DataFrame,
    price_col: str,
    z_window: int,
    horizon: int,
    lookback: int,
    buy_th: float,
    sell_th: float,
) -> Recommendation:
    d = df_norm.copy()
    d["Date"] = pd.to_datetime(d["Date"])
    d = d.sort_values("Date").reset_index(drop=True)

    # Pris-kolumn (fallback om AdjClose saknas)
    if price_col not in d.columns:
        if "product_Close" in d.columns:
            price_col = "product_Close"
        else:
            raise ValueError("Hittar ingen pris-kolumn (product_AdjClose eller product_Close).")

    # Facit för ranking (men vi behåller hela d för 'sista dagen')
    d["future_price"] = d[price_col].shift(-horizon)
    d["actual_dir"] = np.sign(d["future_price"] - d[price_col])


    # Träning för ranking: endast rader med facit
    train_df = d.dropna(subset=["actual_dir"]).tail(lookback)

    sig_cols = [
        f"tsmom_1m_z20",
        f"ma_spread_20_60_z{z_window}",
        f"donchian_breakout_20_z{z_window}",
        f"reg_slope_logprice_20_ann_z{z_window}",
        f"vol_adj_mom_1m_z{z_window}",
    ]

    # 1) Räkna rätt per signal
    correct_counts = {}
    for col in sig_cols:
        pred_dir = np.sign(pd.to_numeric(train_df[col], errors="coerce"))
        mask = (~pd.isna(pred_dir)) & (pred_dir != 0)
        pred_dir = pred_dir[mask]
        actual_dir = train_df.loc[mask, "actual_dir"]
        correct_counts[col] = int((pred_dir == actual_dir).sum())

    # 2) Vikter (bäst->sämst)
    sorted_cols = sorted(correct_counts.items(), key=lambda x: x[1], reverse=True)
    weights = {col: 1 - 0.1*i for i, (col, _) in enumerate(sorted_cols)}  # Här sker viktnignen. Vill bestämma en bra viktning ist för 5 - i och man lägger 1 om man vill ha likviktning  

    # 3) Dagens signal = sista raden i HELA datasetet
    latest = d.iloc[-1]
    weighted_sum = 0.0
    used_weight_sum = 0.0

    for col in sig_cols:
        v = latest[col]
        if pd.isna(v):
            continue
        s = float(np.sign(v))
        if s == 0:
            continue
        weighted_sum += s * weights[col]
        used_weight_sum += weights[col]

    final_signal = 0.0 if used_weight_sum == 0 else (weighted_sum / used_weight_sum)

    # 4) Beslut
    if final_signal > buy_th:
        decision = "KÖP"
    elif final_signal < sell_th:
        decision = "SÄLJ"
    else:
        decision = "NEUTRAL"

    return Recommendation(
        ticker="",
        date=pd.to_datetime(latest["Date"]),
        final_signal=float(final_signal),
        decision=decision,
    )

def process_one_ticker(ticker: str) -> Recommendation:
    # 1) Download
    df = download_ohlcv(ticker, START, END, INTERVAL)

    # Spara rådata om du vill
    data_path = DATA_DIR / f"{ticker}_data.csv"
    df.to_csv(data_path, index=False)

    # 2) Signals
    raw = compute_signals_5(df)
    raw_path = OUT_DIR / f"{ticker}_signals_raw.csv"
    raw.to_csv(raw_path, index=False)

    # 3) Normalize
    norm = normalize_signals(raw, Z_WINDOW)
    norm_path = OUT_DIR / f"{ticker}_signals_norm.csv"
    norm.to_csv(norm_path, index=False)

    # 4) Recommendation
    rec = compute_weighted_recommendation(
        norm,
        price_col="product_AdjClose",
        z_window=Z_WINDOW,
        horizon=HORIZON,
        lookback=LOOKBACK,
        buy_th=BUY_TH,
        sell_th=SELL_TH,
    )
    rec.ticker = ticker
    return rec

def main():
    ensure_dirs()

    recs = []
    errors = []

    for t in TICKERS:
        try:
            rec = process_one_ticker(t)
            recs.append(rec)
            #print(f" {t}: {rec.decision} (signal={rec.final_signal:.3f})")
        except Exception as e:
            errors.append((t, str(e)))
            print(f"{t}: FEL -> {e}")

    if not recs:
        print("\nInga instrument kunde processas.")
        if errors:
            print("\nFel:")
            #for t, msg in errors:
                #print(f" - {t}: {msg}")
        return

    # Samla resultat
    res_df = pd.DataFrame([{
        "ticker": r.ticker,
        "date": r.date,
        "final_signal": r.final_signal,
        "decision": r.decision,
        "abs_signal": abs(r.final_signal),
    } for r in recs]).sort_values("abs_signal", ascending=False)

    # Top x efter |signal|
    top10 = res_df.head(10).copy() 

    print("\n====================")
    print("TOP 10 rekommendationer (störst |signal|)")
    print("====================")
    print(top10[["ticker", "final_signal", "decision", "date"]].to_string(index=False))

    # Spara sammanställning
    stamp = END.replace("-", "")
    res_df.to_csv(OUT_DIR / "all_recommendations.csv", index=False)
    top10.to_csv(OUT_DIR / "top10_recommendations.csv", index=False)

    if errors:
        print("\n====================")
        print("Instrument som misslyckades")
        print("====================")
        for t, msg in errors:
            print(f"- {t}: {msg}")

if __name__ == "__main__":
    run_dates = ["2016-12-30"] + [
        d.strftime("%Y-%m-%d")
        for d in pd.date_range("2017-01-01", "2018-11-30", freq="M")
    ]

    for d in run_dates:
        END = d
        print(f"\n===== Körning för END = {END} =====")
        main()

    
