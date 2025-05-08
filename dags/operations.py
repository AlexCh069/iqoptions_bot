from airflow.decorators import task, dag, setup, teardown
from utils.extraction import ConectionApi
import utils.pre_data as pr
from datetime import datetime, timedelta
import pandas as pd
import os

gmail = "alex.ch.o573@gmail.com", 
password = "dracarys069"

@dag(schedule=timedelta(seconds=40),
     start_date=datetime(2025,5,1),
     catchup=False)
def request_operation():

    @task(execution_timeout=timedelta(seconds=5))
    def modoOperacion(account_type: bool = True):
        API = ConectionApi(gmail=gmail, password=password)
        modeOp = API.changeCount()
        return modeOp

    @task(execution_timeout=timedelta(seconds=15))
    def RealtimeData(gmail: str, password: str):
        API = ConectionApi(gmail=gmail, password=password)
        data = API.RealCandle()
        return data
    
    @task(multiple_outputs=True)
    def Operation(data):
        Value_decision = list(data.values())[0]
        ent, dec = str(Value_decision['open']).split('.')
        
        # Devolvemos un diccionario con claves descriptivas
        return {
            'resultado': 'Par' if int(dec) % 2 == 0 else 'Impar',
            'decimal': dec,
            'estado': int(dec) % 2 == 0
        }
        
    @task
    def RequestTrading(state: bool):
        if state:
            return 'Operacion Realizada'
        else:
            return 'Operacion rechazada'



    modoOperacion()
    data_cdl = RealtimeData(gmail, password)
    opt = Operation(data_cdl)
    # Accedemos usando la clave 'estado' en lugar del índice 2
    rqt = RequestTrading(opt['estado'])
    
    data_cdl >> opt >> rqt  




request_operation()
    

