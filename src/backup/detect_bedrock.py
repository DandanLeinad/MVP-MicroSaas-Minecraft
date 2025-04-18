import os
import platform


def get_bedrock_worlds_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser(
            "~\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds"  # NOQA
        )
    else:
        return None  # Bedrock só disponível no Windows (oficialmente)
