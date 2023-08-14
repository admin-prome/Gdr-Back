import os
import shutil


def clear_directory(directory_path):
    try:
        # Borra todo el contenido del directorio
        shutil.rmtree(directory_path)
        # Crea el directorio vacío nuevamente
        os.mkdir(directory_path)
        return True
    except Exception as e:
        print("Error:", str(e))
        return False