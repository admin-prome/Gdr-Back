import datetime
import pytz

def obtenerFecha() -> str:
    ahora = datetime.datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    return str(fechaHora)

def obtenerFechaHoraBsAs():
    zona_horaria_buenos_aires = pytz.timezone('America/Argentina/Buenos_Aires')
    ahora = datetime.datetime.now(tz=zona_horaria_buenos_aires)
    fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_hora

