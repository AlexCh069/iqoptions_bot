from iqoptionapi.stable_api import IQ_Option
import time

gmail = "alex.ch.o573@gmail.com", 
password = "dracarys069"

# Configuración inicial
API = IQ_Option(gmail, password)
API.connect()  # Conexión a la cuenta (PRACTICE/REAL)

def obtener_mercados_turbo_abiertos():
    """Extrae solo los mercados disponibles para opciones binarias Turbo"""
    try:
        # Obtener todos los mercados
        todos_los_mercados = API.get_all_open_time()
        
        # Filtrar solo opciones Turbo abiertas
        mercados_turbo = {
            activo: datos
            for activo, datos in todos_los_mercados["turbo"].items()
            if datos["open"]
        }
        
        return mercados_turbo
        
    except Exception as e:
        print(f"Error al obtener mercados: {str(e)}")
        return {}

# Ejecución
if __name__ == "__main__":
    # Verificar conexión
    if not API.check_connect():
        print("Error de conexión con IQ Option")
    else:
        print("\n=== Mercados Turbo Disponibles ===")
        turbo_abiertos = obtener_mercados_turbo_abiertos()
        
        # Mostrar resultados
        for activo, datos in turbo_abiertos.items():
            print(f"• {activo.replace('turbo-', '')}")
        
        print(f"\nTotal: {len(turbo_abiertos)} mercados Turbo disponibles")