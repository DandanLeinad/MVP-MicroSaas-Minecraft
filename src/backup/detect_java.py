import os
import platform


def get_java_worlds_path():
    system = platform.system()
    if system == "Windows":
        path = os.path.expandvars(r"%APPDATA%\.minecraft\saves")
    elif system == "Darwin":
        path = os.path.expanduser(
            "~/Library/Application Support/minecraft/saves"
        )
    elif system == "Linux":
        path = os.path.expanduser("~/.minecraft/saves")
    else:
        raise OSError("Sistema operacional não suportado.")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"❌ Minecraft Java Edition não encontrado ou nenhum mundo salvo em: {path}" # NOQA
        )
    return path
