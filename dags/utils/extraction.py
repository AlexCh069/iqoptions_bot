from iqoptionapi.stable_api import IQ_Option
import logging
import time
import pandas as pd
from datetime import datetime

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

    
    def ExtraccionData(self,range_days: int) -> pd.DataFrame:
        goal = "EURUSD"             #   Mercado
        end_from_time = time.time() #   Ultima marca de tiempo
        ANS = []

        for i in range(range_days):     # range_days : Cantidad de dias de los que se extraera la data
            data = self.API.get_candles(goal, 60, 1000, end_from_time) # Extraccion de las anteriores 1000 velas desde la marca de tiempo
            ANS = data + ANS
            end_from_time = int(data[0]["from"]) - 1                    # Actualizacion de la nueva marca de tiempo

        data = pd.DataFrame(ANS)
        data.drop(['id','at'], axis=1, inplace=True)

        return data

# API = ConectionApi(gmail=gmail, password=password)      
# candls = API.ExtraccionData(5)
# fecha_actual = datetime.now()

# candls.to_csv(f'./data_csv/{fecha_actual.strftime("%Y-%m-%d_%H-%M")}.csv', index= False)
# print(candls.head(3))