import os
import zipfile
from datetime import datetime

BACKUP_DIR = "backups_worlds"
BACKUP_DIR_BEDROCK = "backups_worlds/bedrock"
BACKUP_DIR_JAVA = "backups_worlds/java"


def list_worlds(worlds_path):
    try:
        return [
            d
            for d in os.listdir(worlds_path)
            if os.path.isdir(os.path.join(worlds_path, d))
        ]
    except FileNotFoundError:
        return []


def make_backup(worlds_path, world_name, edition=None):
    # Seleciona o diretório de backup de acordo com a edição
    if edition == "java":
        backup_dir = BACKUP_DIR_JAVA
    elif edition == "bedrock":
        backup_dir = BACKUP_DIR_BEDROCK
    else:
        backup_dir = BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)
    src = os.path.join(worlds_path, world_name)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(backup_dir, f"{world_name}_{now}.zip")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(src):
            for file in files:
                abs_file = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file, src)
                zipf.write(
                    abs_file, arcname=os.path.join(world_name, rel_path)
                )
    print(f"✅ Backup salvo: {dst}")


def menu(worlds_path, edition=None):
    worlds = list_worlds(worlds_path)
    if not worlds:
        print("❌ Nenhum mundo encontrado.")
        return
    print("\nMundos disponíveis:")
    for i, w in enumerate(worlds):
        print(f"{i + 1}. {w}")

    idx = input("Escolha o número do mundo para backup: ")
    try:
        world_name = worlds[int(idx) - 1]
        make_backup(worlds_path, world_name, edition)
    except (IndexError, ValueError):
        print("Entrada inválida.")
