# ORB Backtesting Data Architecture

You're scaling to 500 stocks. Here's how to do it right.

---

## 1. Storage: One Dataset, Multi-Index

**Don't store 500 separate files.** Use a single dataset with `(date, ticker)` as the index.

Why? Because every day you need to compare stocks against each other. With separate files, you'd open 500 files just to pick your top 20. With a multi-index, it's one query.

```python
# This is what you want
df = df.set_index(['date', 'ticker'])

# Get all 500 stocks for Jan 15 in one shot
daily = df.loc['2024-01-15']

# Get just AAPL across all dates
aapl = df.xs('AAPL', level='ticker')
```

---

2. Features: Pre-compute the Fixed Stuff, Calculate the Rest

Pre-compute once and store:
- Opening range high/low (9:30-9:45 is fixed)
- Previous day close
- 20-day average volume (for relative volume denominator)

Calculate during backtest:
- ATR with different periods (7, 14, 20, 30)
- Relative volume thresholds (100%, 150%, 200%)
- Any parameter you're sweeping

Why not pre-compute everything? If you're testing ATR periods 7-30, that's 24 extra columns per stock. Storage bloats, and computing ATR on-the-fly takes milliseconds anyway.

```
# Stored in parquet
STORED = ['or_high', 'or_low', 'prev_close', 'avg_vol_20d']

# Computed fresh each backtest
def run_backtest(df, atr_period=14, rv_threshold=1.0):
    df['atr'] = compute_atr(df, atr_period)  # Fast, vectorized
    df['rel_vol'] = df['volume'] / df['avg_vol_20d']
    df['passes_rv'] = df['rel_vol'] >= rv_threshold


---

## 3. Cross-Sectional: Filter, Rank, Select Top 20

Yes, your approach is correct. Here's the flow:

```
Each trading day at 9:45 AM:
  1. Load all 500 stocks for that day
  2. Apply filters (price > $10, relative volume > 100%, etc.)
  3. Rank survivors by your criteria
  4. Take top 20
  5. Trade only those 20
```

```python
def pick_daily_universe(df, date, top_n=20):
    daily = df.loc[date]

    # Filter
    filtered = daily[
        (daily['close'] >= 10) &
        (daily['close'] <= 500) &
        (daily['rel_vol'] >= 1.0) &
        (daily['or_range_pct'] >= 0.005)
    ]

    # Rank and pick top N
    return filtered.nlargest(top_n, 'rank_score')['ticker'].tolist()
```

The key insight: you're not backtesting 500 stocks. You're backtesting a dynamic universe of ~20 stocks that changes daily.

---

## 4. File Structure: One Parquet Per Year

**Don't do:**
- 500 files (one per ticker) - cross-sectional queries become painful
- 1 giant file (all years) - 10GB+ is unwieldy

**Do this:**
```
data/
  sp500_1min/
    2020.parquet   # ~2GB each
    2021.parquet
    2022.parquet
    2023.parquet
    2024.parquet
```

Each file has all 500 tickers for that year. Parquet handles this well with predicate pushdown:

```python
# Only loads AAPL and MSFT rows, not all 500
df = pd.read_parquet("2024.parquet", filters=[('ticker', 'in', ['AAPL', 'MSFT'])])
```

---

## Quick Answers

| Question | Answer |
|----------|--------|
| Separate or unified? | Unified with (date, ticker) index |
| Pre-compute features? | Only fixed ones. Sweep params = compute live |
| Cross-sectional workflow? | All tickers -> filter -> rank -> top N -> signals |
| File structure? | One parquet per year, all tickers inside |

---

## Starter Code

```python
class ORBData:
    def __init__(self, data_dir="data/sp500_1min"):
        self.data_dir = Path(data_dir)

    def load(self, years):
        dfs = [pd.read_parquet(self.data_dir / f"{y}.parquet") for y in years]
        df = pd.concat(dfs)
        df['date'] = df['timestamp'].dt.date
        return df.set_index(['date', 'ticker']).sort_index()

    def daily(self, df, date):
        return df.loc[date]

# Usage
loader = ORBData()
df = loader.load([2023, 2024])

for date in trading_dates:
    universe = pick_daily_universe(df, date, top_n=20)
    signals = generate_signals(df.loc[date], universe)
```

That's it. Unified storage, hybrid features, daily selection, yearly files.
