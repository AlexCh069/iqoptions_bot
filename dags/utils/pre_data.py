import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import AverageTrueRange
import os

def calcular_indicadores(df):
    """
    Calcula indicadores técnicos y los estandariza.

    Parámetros:
        df (pd.DataFrame): Debe contener columnas ['open', 'high', 'low', 'close', 'volume']

    Retorna:
        pd.DataFrame: DataFrame original con columnas de indicadores añadidas y estandarizadas.
    """

    # Validación de columnas necesarias
    columnas_requeridas = ['open', 'max', 'min', 'close', 'volume']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna requerida: {col}")

    df = df.copy()

    # RSI
    df['rsi_5'] = RSIIndicator(close=df['close'], window=5).rsi()
    df['rsi_7'] = RSIIndicator(close=df['close'], window=7).rsi()

    # Estocástico
    stoch = StochasticOscillator(high=df['max'], low=df['min'], close=df['close'], window=5, smooth_window=3)
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()

    # ATR
    df['atr_5'] = AverageTrueRange(high=df['max'], low=df['min'], close=df['close'], window=5).average_true_range()

    # Velocidad del precio
    df['price_speed_3'] = df['close'].pct_change(periods=3)
    df['price_speed_5'] = df['close'].pct_change(periods=5)
    
    return df

    
def obtener_ultimo_archivo_creado():
    directorio = "/home/ares/iqoptions_bot/data_csv"     # Carpeta con los datos almacenados
    archivos = [os.path.join(directorio, f) for f in os.listdir(directorio) 
                if os.path.isfile(os.path.join(directorio, f))]
    
    if not archivos:
        return None
    
    ultimo_archivo = max(archivos, key=os.path.getctime)
    return ultimo_archivo