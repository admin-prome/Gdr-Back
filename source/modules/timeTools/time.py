import pytz
from datetime import datetime

def obtenerFecha() -> str:
    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    return str(fechaHora)

def obtenerFechaHoraBsAs():
    zona_horaria_buenos_aires = pytz.timezone('America/Argentina/Buenos_Aires')
    ahora = datetime.now(tz=zona_horaria_buenos_aires)
    fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_hora



def convertir_formato_fecha(fecha_str):
    # Intenta detectar el formato 'dd/MM/yyyy'
    try:
        fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
    except ValueError:
        # Si falla, intenta con el formato 'yyyy-MM-dd'
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            print('El formato de fecha no fue reconocido')
            # Si ambos intentos fallan, lanza una excepción
            #raise ValueError('Formato de fecha no reconocido')
            return ''
    # Formatea la fecha al nuevo formato 'yyyy-MM-dd'
    fecha_formateada = fecha_obj.strftime('%Y-%m-%d')

    return fecha_formateada