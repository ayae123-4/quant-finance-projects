# Signal Layer — Systematic Trading System

Four technical indicators (SMA, RSI, MACD, Bollinger Bands) implemented 
from scratch with pandas/numpy, as the signal layer of a modular trading 
system. Built and validated on international data (yfinance) before any 
application to the Casablanca Stock Exchange — clean data first, so that 
any anomaly points to the code, not to missing data.

All signals are shifted by one day to prevent look-ahead bias.

# Functions

`charger_prix(ticker, periode='2y')` — Downloads closing prices from yfinance. Returns a 1D pandas Series.

`signal_SMA(prix, num=20)` — Returns a +1 / -1 / 0 signal based on the price position relative to its simple moving average.

`signal_RSI(prix, fenetre=14, seuil_bas=30, seuil_haut=70)` — Returns a +1 / -1 / 0 signal based on oversold and overbought thresholds (contrarian logic).

`signal_MACD(prix, moyenne_courte=12, moyenne_longue=26, ligne_signal=9)` — Returns a +1 / -1 / 0 signal based on the MACD crossover with its signal line.

`signal_BOLLINGER(prix, fenetre=20, k=2)` — Returns a +1 / -1 / 0 signal when the price exits the adaptive bands (mean-reversion logic).

# Usage

```python
from indicateurs import charger_prix, signal_SMA, signal_RSI, signal_MACD, signal_BOLLINGER

prix = charger_prix('AAPL')
signal = signal_SMA(prix, num=20)
print(signal.value_counts())
```

All indicators take the same input (a price Series) and return the same
output format (+1 / -1 / 0), so they are interchangeable and can be
combined downstream.

# Methodology — look-ahead bias

Every signal is shifted by one day (`.shift(1)`).

An indicator computed at day J uses the closing price of day J, which is
only known after the market closes. The order can therefore not be executed
before the opening of day J+1. Without this shift, the backtest would buy
at a price it could not have obtained, capturing gains that never existed —
producing results that look excellent and are entirely false.

The layers are also kept separate: `charger_prix` (data layer) is
independent from the signal functions. Switching the data source — for
example from yfinance to the Casablanca Stock Exchange — requires changing
one function only, leaving the indicators untouched.