import datetime

def obtenerFecha() -> str:
    ahora = datetime.datetime.now()
    fechaHora = ahora.strftime("%d/%m/%Y %H:%M:%S")
    return str(fechaHora)
