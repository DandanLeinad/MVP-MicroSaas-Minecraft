import os
import platform


def get_java_worlds_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser("~\\AppData\\Roaming\\.minecraft\\saves")
    elif system == "Darwin":  # macOS
        return os.path.expanduser(
            "~/Library/Application Support/minecraft/saves"
        )
    elif system == "Linux":
        return os.path.expanduser("~/.minecraft/saves")
    else:
        return None
