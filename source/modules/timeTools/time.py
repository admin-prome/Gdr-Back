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


from datetime import datetime

from datetime import datetime

def convertir_formato_fecha(fecha_str=''):
    print('-----------------INICIO DE FORMATEO DE FECHA-----------------')
    print(datetime.now())
    if fecha_str is not None and isinstance(fecha_str, str):
        print(str(fecha_str))
        print(f'Esta es la fecha: {fecha_str}')
        
        # Verifica si la fecha ya está en el formato 'YYYY-MM-DD'
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            print('La fecha ya está en el formato correcto')
            print('-----------------FIN FORMATEO DE FECHA-----------------')
            return fecha_str
        except ValueError:
            pass

        formatos = ['%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d', '%Y %m %d', '%d %m %Y', '%Y-%m-%d']

        for formato in formatos:
            try:
                fecha_obj = datetime.strptime(fecha_str, formato)
                # Si la conversión tiene éxito, formatea la fecha al nuevo formato 'yyyy-MM-dd'
                fecha_formateada = fecha_obj.strftime('%Y-%m-%d')
                print(f'Fecha formateada: {fecha_formateada}')
                return fecha_formateada
            except ValueError:
                pass

        # Si no se encuentra un formato válido, lanza una excepción
        #raise ValueError('Formato de fecha no reconocido')

    fecha_str = ''
    print('No se registraron fechas para formatear')
    print('-----------------FIN FORMATEO DE FECHA-----------------')
    return fecha_str

if __name__ == '__main__':
    print(obtenerFecha())
    print(obtenerFechaHoraBsAs())
    print(convertir_formato_fecha('22/11/1989'))
    print(convertir_formato_fecha('22-11-1989'))
    print(convertir_formato_fecha('18/11/2023'))
    print(convertir_formato_fecha('1989/11/22'))
    print(convertir_formato_fecha('1989-11-22'))
    print(convertir_formato_fecha('1989 01 22'))
    print(convertir_formato_fecha())