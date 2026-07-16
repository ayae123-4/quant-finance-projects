import yfinance as yf
import numpy as np
import pandas as pd
def charger_prix(ticker, periode='2y'):
    D= yf.download(ticker, period=periode)
    prix=D['Close'].squeeze()
    return prix
    
def signal_SMA(prix, num=20):
    SMA_num=prix.rolling(num).mean()
    signal_brut=np.where(prix>SMA_num,1,np.where(prix<SMA_num,-1,0))
    signal_brut = pd.Series(signal_brut, index=SMA_num.index)
    signal_sma=signal_brut.shift(1)
    return signal_sma

def signal_RSI(prix,fenetre=14, seuil_bas=30, seuil_haut=70):
    delta=prix.diff() 
    gains=delta.clip(lower=0) 
    perte=delta.clip(upper=0).abs() 
    gain_moyen=gains.rolling(fenetre).mean()
    perte_moyenne=perte.rolling(fenetre).mean()
    RS=gain_moyen/perte_moyenne
    RSI=100-(100/(1+RS))
    signal_rsi_brut=np.where(RSI<seuil_bas,1,np.where(RSI>seuil_haut,-1,0)) 
    signal_rsi_brut = pd.Series(signal_rsi_brut, index=RSI.index)
    signal_rsi=signal_rsi_brut.shift(1)
    return signal_rsi

def signal_MACD(prix, moyenne_courte=12, moyenne_longue=26, ligne_signal=9):
    EMA12=prix.ewm(span=moyenne_courte).mean()
    EMA26=prix.ewm(span=moyenne_longue).mean()
    MACD=EMA12-EMA26
    ligne=MACD.ewm(span=ligne_signal).mean()
    signal_MACD_brut=np.where(MACD>ligne,1,np.where(MACD<ligne,-1,0))  
    signal_MACD_brut = pd.Series(signal_MACD_brut, index=MACD.index)
    signal_macd=signal_MACD_brut.shift(1)
    return signal_macd

def signal_BOLLINGER(prix, fenetre=20, k=2):
    SMA20 = prix.rolling(fenetre).mean()
    ecart_type = prix.rolling(fenetre).std()
    bande_haut = SMA20 + k * ecart_type
    bande_bas = SMA20 - k * ecart_type
    signal_brut = np.where(prix < bande_bas, 1, np.where(prix > bande_haut, -1, 0))
    signal_brut = pd.Series(signal_brut, index=prix.index)
    signal_brut = signal_brut.shift(1)
    return signal_brut