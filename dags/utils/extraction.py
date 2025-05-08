from iqoptionapi.stable_api import IQ_Option
import logging
import time
import pandas as pd
from datetime import datetime
from .pre_data import calcular_indicadores

# Configurar logging
logging.basicConfig(level=logging.INFO)

gmail = "alex.ch.o573@gmail.com", 
password = "dracarys069"


class ConectionApi:

    def __init__(self, gmail, password):
        self.gmail = gmail
        self.password = password
        self.API = IQ_Option(self.gmail, self.password)
        self.API.connect()

        if self.API.check_connect():
            self.conection_state = True
        else:
            print('conexcion fallida')

    def changeCount(self, account_type:bool = True):
        if account_type: 
            self.API.change_balance("PRACTICE")
            balance = self.API.get_balance()
            return f"Modo PRACTICE. Balance actual: {balance}"

        else:
            self.API.change_balance("REAL")
            balance = self.API.get_balance()
            return f"Modo REAL. Balance actual: {balance}"

    def ExtraccionData(self,range_days: int) -> pd.DataFrame:
        goal = "EURUSD"             #   Mercado
        end_from_time = time.time() #   Ultima marca de tiempo
        ANS = []

        for i in range(2*range_days):     # range_days : Cantidad de dias de los que se extraera la data
            data = self.API.get_candles(goal, 30, 1000, end_from_time) # Extraccion de las anteriores 1000 velas desde la marca de tiempo
            ANS = data + ANS
            end_from_time = int(data[0]["from"]) - 1                    # Actualizacion de la nueva marca de tiempo

        data = pd.DataFrame(ANS)

        # Reorganizacion de data 
        data['from_dt'] = pd.to_datetime(data['from'], unit='s')
        data['to_dt'] = pd.to_datetime(data['to'], unit='s')
        data.drop(['id','at','from','to'], axis=1, inplace=True)
        data = data[['from_dt','to_dt','open','close','min','max','volume']]

        # Calculo de indicadores
        data_more_indicators = calcular_indicadores(data)

        return data_more_indicators
    
    def RealCandle(self):
        
        goal = "EURUSD"
        time_frame = 60

        st_cdl = self.API.start_candles_stream(goal, time_frame, 1)
        rt_cdl = self.API.get_realtime_candles(goal, time_frame)

        return rt_cdl
    
    # En tu archivo utils/extraction.py, modifica la función OperationIQ:

    def OperationIQ(self, activo, direccion, monto, expiracion):
        chequeo = self.API.buy(monto, activo, direccion, expiracion)
        
        # Verifica primero si chequeo es un diccionario
        if isinstance(chequeo, dict):
            if chequeo.get("status"):  # Usamos .get() para evitar KeyError
                print(f"Operación exitosa! ID: {chequeo['id']}")
                return chequeo['id'], True
            else:
                print(f"Error en operación: {chequeo.get('message', 'Sin mensaje de error')}")
                return None, False
        elif isinstance(chequeo, tuple):
            # Si es una tupla, asumimos que el primer elemento es el estado
            if chequeo[0]:  # Accedemos por índice
                print(f"Operación exitosa! Datos: {chequeo}")
                return chequeo[1], True  # Ajusta según la estructura real
            else:
                print(f"Error en operación (tupla): {chequeo}")
                return None, False
        else:
            print(f"Tipo de respuesta inesperado: {type(chequeo)}")
            return None, False

        


    
   



# API = ConectionApi(gmail=gmail, password=password)      
# candls = API.ExtraccionData(5)
# fecha_actual = datetime.now()

# candls.to_csv(f'./data_csv/{fecha_actual.strftime("%Y-%m-%d_%H-%M")}.csv', index= False)
# print(candls.head(3))