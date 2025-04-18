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


def restore_backup(worlds_path, backup_name, edition=None):
    # Restaura o backup selecionado para o diretório de mundos
    if edition == "java":
        backup_dir = BACKUP_DIR_JAVA
    elif edition == "bedrock":
        backup_dir = BACKUP_DIR_BEDROCK
    else:
        backup_dir = BACKUP_DIR
    src = os.path.join(backup_dir, backup_name)
    try:
        with zipfile.ZipFile(src, "r") as zipf:
            zipf.extractall(worlds_path)
        print(f"✅ Backup restaurado: {backup_name} em {worlds_path}")
    except Exception as e:
        print(f"❌ Falha ao restaurar backup: {e}")


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
    # Menu interativo para criar e restaurar backups
    while True:
        # Listagem de mundos
        worlds = list_worlds(worlds_path)
        print("\nMundos disponíveis:")
        if worlds:
            for i, w in enumerate(worlds):
                print(f"  {i + 1}. {w}")
        else:
            print("  (nenhum mundo encontrado)")

        # Listagem de backups
        backups = list_backups(edition)
        print(
            f"\nBackups existentes para edição {edition.capitalize() if edition else ''}:"
        )
        if backups:
            for j, b in enumerate(backups):
                print(f"  {j + 1}. {b}")
        else:
            print("  (nenhum backup encontrado)")

        # Opções do usuário
        print("\nOpções:")
        print("  b - Criar backup de um mundo")
        print("  r - Restaurar um backup")
        print("  0 - Sair")
        choice = input("Escolha uma opção: ").strip().lower()
        if choice == "0":
            break
        elif choice == "b":
            idx = input("Escolha o número do mundo para backup: ")
            try:
                world_name = worlds[int(idx) - 1]
                make_backup(worlds_path, world_name, edition)
            except Exception:
                print("Entrada inválida.")
        elif choice == "r":
            if not backups:
                print("Nenhum backup para restaurar.")
                continue
            idxb = input("Escolha o número do backup para restaurar: ")
            try:
                backup_name = backups[int(idxb) - 1]
                restore_backup(worlds_path, backup_name, edition)
            except Exception:
                print("Entrada inválida.")
        else:
            print("Opção inválida.")
