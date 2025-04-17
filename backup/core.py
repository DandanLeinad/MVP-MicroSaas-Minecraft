import datetime
import os
import zipfile


def zip_folder(source_folder, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, source_folder)
                zipf.write(filepath, arcname)


def list_worlds(worlds_path):
    return [
        d
        for d in os.listdir(worlds_path)
        if os.path.isdir(os.path.join(worlds_path, d))
    ]


def backup_world(worlds_path, world_name, output_dir="backups_worlds"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    world_path = os.path.join(worlds_path, world_name)
    zip_path = os.path.join(output_dir, f"{world_name}_{timestamp}.zip")
    zip_folder(world_path, zip_path)
    print(f"Backup criado: {zip_path}")


def menu(worlds_path):
    while True:
        print(f"\nMundos encontrados em {worlds_path}")
        worlds = list_worlds(worlds_path)
        for i, name in enumerate(worlds):
            print(f"{i + 1}. {name}")
        print("0. Sair")

        choice = input("Escolha o número do mundo para fazer backup: ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or int(choice) - 1 not in range(len(worlds)):
            print("Escolha inválida.")
            continue

        world_name = worlds[int(choice) - 1]
        backup_world(worlds_path, world_name)
