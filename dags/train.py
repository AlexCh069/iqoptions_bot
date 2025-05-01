from airflow.decorators import task, dag, setup, teardown
from utils.extraction import ConectionApi
import utils.pre_data as pr
from datetime import datetime, timedelta
import pandas as pd
import os



gmail = "alex.ch.o573@gmail.com", 
password = "dracarys069"

@dag(schedule=timedelta(days=1),
     start_date=datetime(2025,5,1))
def entrenamiento():
    
    @task
    def extractionData(gmail, password):
        API = ConectionApi(gmail=gmail, password=password)
        data = API.ExtraccionData(range_days=5)

        fecha_actual = datetime.now()
        
        current_dir = os.path.dirname(os.path.abspath(__file__)) # Ruta absoluta al directorio actual (donde está train.py)
        output_dir = os.path.join(current_dir, '..', 'data_csv') # Ruta al directorio deseado (data_csv que está un nivel arriba)
        os.makedirs(output_dir, exist_ok=True)  # Crear carpeta si no existe
        # Guardar archivo CSV
        filename = f'{fecha_actual.strftime("%Y-%m-%d_%H-%M")}.csv'
        data.to_csv(os.path.join(output_dir, filename), index=False)

        return 'Data Almacenada'
    
    @task
    def indicadores():
        csv_path = pr.obtener_ultimo_archivo_creado()
        df = pd.read_csv(csv_path)

        return print(df.head(2))
    
    extractionData(gmail,password) >> indicadores()


entrenamiento()

    


