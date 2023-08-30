import os


def clear_directory(directory_file):
    try:
        os.remove(directory_file)
    
        return True
    except Exception as e:
        print("Error:", str(e))
        return False