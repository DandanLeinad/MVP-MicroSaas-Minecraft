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

# Diretórios padrão de backups
BACKUP_DIR = "backups_worlds"
BACKUP_DIR_JAVA = "backups_worlds/java"
BACKUP_DIR_BEDROCK = "backups_worlds/bedrock"


class BackupManager:
    """Gerencia criação e restauração de backups de mundos Minecraft"""

    def __init__(self):
        # Diretórios de backup
        self.backup_dir = BACKUP_DIR
        self.backup_dir_java = BACKUP_DIR_JAVA
        self.backup_dir_bedrock = BACKUP_DIR_BEDROCK

    def list_worlds(self, worlds_path):
        """Retorna lista de tuplas (folder_name, display_name) lendo levelname.txt"""
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

    def list_backups(self, edition=None):
        """Retorna arquivos .zip em diretório de backup da edição"""
        if edition == "java":
            dir_ = self.backup_dir_java
        elif edition == "bedrock":
            dir_ = self.backup_dir_bedrock
        else:
            dir_ = self.backup_dir
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

    def make_backup(
        self, worlds_path, world_name, edition=None, description=None
    ):
        """Cria backup com metadata de descrição e retorna status"""
        try:
            # seleciona pasta
            if edition == "java":
                backup_dir = self.backup_dir_java
            elif edition == "bedrock":
                backup_dir = self.backup_dir_bedrock
            else:
                backup_dir = self.backup_dir
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

    def restore_backup(self, worlds_path, backup_name, edition=None):
        """Restaura backup selecionado e salva metadata no mundo"""
        if edition == "java":
            backup_dir = self.backup_dir_java
        elif edition == "bedrock":
            backup_dir = self.backup_dir_bedrock
        else:
            backup_dir = self.backup_dir
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

    def menu(self, worlds_path, edition=None):
        """Menu interativo para criar e restaurar backups"""
        while True:
            # Listagem de mundos
            worlds = self.list_worlds(worlds_path)
            print("\nMundos disponíveis:")
            if worlds:
                for i, (folder, display) in enumerate(worlds):
                    print(f"  {i + 1}. {display}")
            else:
                print("  (nenhum mundo encontrado)")

            # Opções do usuário
            print("\nOpções:")
            print("  b - Criar backup de um mundo")
            print("  r - Restaurar um backup de um mundo")
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
                    if any(c in desc for c in r"\\/:*?\"<>|"):
                        print("❌ Descrição contém caracteres inválidos.")
                    else:
                        self.make_backup(
                            worlds_path, world_name, edition, desc
                        )
                except Exception:
                    print("Entrada inválida.")
            elif choice == "r":
                # Seleciona o mundo para restaurar
                idxw = input(
                    "Escolha o número do mundo para restaurar backup: "
                )
                try:
                    folder, _ = worlds[int(idxw) - 1]
                except Exception:
                    print("Entrada inválida.")
                    continue
                # filtra backups do mundo
                all_backs = self.list_backups(edition)
                backs = [
                    (b, d) for b, d in all_backs if b.startswith(folder + "_")
                ]
                if not backs:
                    print(f"  (nenhum backup encontrado para {folder})")
                    continue
                print("\nBackups disponíveis para o mundo:")
                for j, (b, d) in enumerate(backs):
                    print(f"  {j + 1}. {b} - {d}")
                idxb = input("Escolha o número do backup para restaurar: ")
                try:
                    backup_name = backs[int(idxb) - 1][0]
                    self.restore_backup(worlds_path, backup_name, edition)
                except Exception:
                    print("Entrada inválida.")
            else:
                print("Opção inválida.")


# Instância padrão para uso no módulo
manager = BackupManager()

# Exporta funções para compatibilidade com código existente
list_worlds = manager.list_worlds
list_backups = manager.list_backups
make_backup = manager.make_backup
restore_backup = manager.restore_backup
menu = manager.menu
