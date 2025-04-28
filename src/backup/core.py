# para metadata dos backups
import json
import os
import zipfile
from datetime import datetime

# noqa to suppress linting error for missing module
import colorama  # noqa
from colorama import Fore  # noqa

# Inicializa colorama para cores no console
colorama.init(autoreset=True)

BACKUP_DIR = "backups_worlds"
BACKUP_DIR_BEDROCK = "backups_worlds/bedrock"
BACKUP_DIR_JAVA = "backups_worlds/java"


def list_worlds(worlds_path):
    """Retorna lista de tuplas (folder_name, display_name) lendo levelname.txt."""
    try:
        result = []
        for d in os.listdir(worlds_path):
            full = os.path.join(worlds_path, d)
            if not os.path.isdir(full):
                continue
            name = d
            display = d
            # tenta ler display name em levelname.txt
            level_file = os.path.join(full, "levelname.txt")
            try:
                with open(level_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        display = text
            except Exception:
                pass
            result.append((name, display))
        return result
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
        backups = []
        for fname in os.listdir(dir_):
            if not fname.lower().endswith(".zip"):
                continue
            desc = ""
            try:
                with zipfile.ZipFile(os.path.join(dir_, fname), "r") as z:
                    if "metadata.json" in z.namelist():
                        data = json.loads(z.read("metadata.json"))
                        desc = data.get("description", "")
            except Exception:
                pass
            backups.append((fname, desc))
        return backups
    except FileNotFoundError:
        return []


def restore_backup(worlds_path, backup_name, edition=None):
    # Restaura o backup selecionado e salva metadata dentro da pasta do mundo
    if edition == "java":
        backup_dir = BACKUP_DIR_JAVA
    elif edition == "bedrock":
        backup_dir = BACKUP_DIR_BEDROCK
    else:
        backup_dir = BACKUP_DIR
    src = os.path.join(backup_dir, backup_name)
    try:
        with zipfile.ZipFile(src, "r") as zipf:
            # lê metadata antes de extrair
            metadata = {}
            if "metadata.json" in zipf.namelist():
                metadata = json.loads(zipf.read("metadata.json"))
            # extrai todos os demais arquivos
            for member in zipf.namelist():
                if member == "metadata.json":
                    continue
                zipf.extract(member, worlds_path)
            # salva metadata dentro da pasta do mundo como mvp2.json
            world = metadata.get("world")
            if world:
                dest = os.path.join(worlds_path, world, "mvp2.json")
                with open(dest, "w", encoding="utf-8") as mf:
                    json.dump(metadata, mf, ensure_ascii=False, indent=2)
        msg = f"✅ Backup restaurado: {backup_name}"
        print(Fore.GREEN + msg)
        return True
    except Exception as e:
        err = f"❌ Falha ao restaurar backup: {e}"
        print(Fore.RED + err)
        return False


def make_backup(worlds_path, world_name, edition=None, description=None):
    # Cria backup com metadata de descrição e retorna status
    try:
        # seleciona pasta
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
                    arc = os.path.join(world_name, rel_path)
                    zipf.write(abs_file, arcname=arc)
            # adiciona metadata.json dentro do zip
            meta = {
                "world": world_name,
                "edition": edition,
                "timestamp": now,
                "description": description or "",
            }
            zipf.writestr("metadata.json", json.dumps(meta))
        ok = f"✅ Backup salvo: {dst}"
        print(Fore.GREEN + ok)
        return True
    except Exception as e:
        err = f"❌ Falha ao criar backup: {e}"
        print(Fore.RED + err)
        return False


def menu(worlds_path, edition=None):
    # Menu interativo para criar e restaurar backups
    while True:
        # Listagem de mundos
        worlds = list_worlds(worlds_path)
        print("\nMundos disponíveis:")
        if worlds:
            for i, (folder, display) in enumerate(worlds):
                print(f"  {i + 1}. {display}")
        else:
            print("  (nenhum mundo encontrado)")

        # Listagem de backups
        backups = list_backups(edition)
        title = (
            "\nBackups existentes para edição "
            f"{edition.capitalize() if edition else ''}:"
        )
        print(title)
        if backups:
            for j, (b, desc) in enumerate(backups):
                print(f"  {j + 1}. {b} - {desc}")
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
                folder, _ = worlds[int(idx) - 1]
                world_name = folder
                # descrição opcional
                desc = input("Descrição/tag (opcional): ").strip()
                # valida caracteres inválidos
                if any(c in desc for c in r"\/:*?\"<>|"):
                    print("❌ Descrição contém caracteres inválidos.")
                else:
                    make_backup(worlds_path, world_name, edition, desc)
            except Exception:
                print("Entrada inválida.")
        elif choice == "r":
            if not backups:
                print("Nenhum backup para restaurar.")
                continue
            idxb = input("Escolha o número do backup para restaurar: ")
            try:
                backup_name = backups[int(idxb) - 1][0]
                restore_backup(worlds_path, backup_name, edition)
            except Exception:
                print("Entrada inválida.")
        else:
            print("Opção inválida.")
