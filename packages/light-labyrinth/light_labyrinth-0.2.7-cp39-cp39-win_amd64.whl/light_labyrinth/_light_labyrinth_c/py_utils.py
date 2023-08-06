from sys import platform

def get_os():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "osx"
    elif platform == "win32":
        return "win"
    
def get_dll_ext():
    return "dll" if get_os() == "win" else "so"