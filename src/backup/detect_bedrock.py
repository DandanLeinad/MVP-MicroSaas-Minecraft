import os
import platform


def get_bedrock_worlds_path():
    if platform.system() == "Windows":
        path = os.path.expandvars(
            r"%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds" # NOQA
        )
    else:
        raise OSError("Bedrock Edition é suportada apenas no Windows.")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"❌ Minecraft Bedrock Edition não encontrado ou nenhum mundo salvo em: {path}" # NOQA
        )
    return path
