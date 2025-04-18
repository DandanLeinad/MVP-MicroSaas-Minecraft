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


def list_backups(edition=None):
    # Retorna arquivos .zip em diretório de backup da edição
    if edition == "java":
        dir_ = BACKUP_DIR_JAVA
    elif edition == "bedrock":
        dir_ = BACKUP_DIR_BEDROCK
    else:
        dir_ = BACKUP_DIR
    try:
        return [f for f in os.listdir(dir_) if f.lower().endswith(".zip")]
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
    # Lista mundos disponíveis
    worlds = list_worlds(worlds_path)
    if not worlds:
        print("❌ Nenhum mundo encontrado.")
        return
    print("\nMundos disponíveis:")
    for i, w in enumerate(worlds):
        print(f"{i + 1}. {w}")

    # Lista backups existentes na edição
    backups = list_backups(edition)
    print(
        f"\nBackups existentes para edição {edition.capitalize() if edition else ''}:"
    )
    if backups:
        for j, b in enumerate(backups):
            print(f"{j + 1}. {b}")
    else:
        print("(nenhum backup encontrado)")

    idx = input("\nEscolha o número do mundo para backup: ")
    try:
        world_name = worlds[int(idx) - 1]
        make_backup(worlds_path, world_name, edition)
    except (IndexError, ValueError):
        print("Entrada inválida.")
