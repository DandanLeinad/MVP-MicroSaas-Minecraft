import os
import platform
import zipfile
from datetime import datetime
from pathlib import Path

import typer

app = typer.Typer()

# Config: caminhos padrão para Java e Bedrock
if platform.system() == "Windows":
    JAVA_SAVE_PATH = Path(os.getenv("APPDATA")) / ".minecraft" / "saves"
    BEDROCK_SAVE_PATH = (
        Path(os.getenv("LOCALAPPDATA"))
        / "Packages"
        / "Microsoft.MinecraftUWP_8wekyb3d8bbwe"
        / "LocalState"
        / "games"
        / "com.mojang"
        / "minecraftWorlds"
    )
else:
    JAVA_SAVE_PATH = Path.home() / ".minecraft" / "saves"
    BEDROCK_SAVE_PATH = Path.home() / "minecraftWorlds"

BACKUP_PATH = Path.home() / "MinecraftBackups"
BACKUP_PATH.mkdir(exist_ok=True)


def list_worlds(path: Path):
    if not path.exists():
        return []
    return [p for p in path.iterdir() if p.is_dir()]


def zip_world(world_path: Path, backup_type: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = f"{world_path.name}_{backup_type}_{timestamp}.zip"
    zip_path = BACKUP_PATH / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(world_path):
            for file in files:
                filepath = Path(root) / file
                arcname = filepath.relative_to(world_path.parent)
                zipf.write(filepath, arcname)
    return zip_path


@app.command()
def backup(
    edition: str = typer.Option(
        ...,
        prompt="Edição (java/bedrock)",
        help="Escolha entre 'java' ou 'bedrock'",
    )
):
    """Cria um backup de um mundo salvo do Minecraft."""
    if edition.lower() == "java":
        worlds = list_worlds(JAVA_SAVE_PATH)
    elif edition.lower() == "bedrock":
        worlds = list_worlds(BEDROCK_SAVE_PATH)
    else:
        typer.echo("❌ Edição inválida. Use 'java' ou 'bedrock'.")
        raise typer.Exit()

    if not worlds:
        typer.echo("❌ Nenhum mundo encontrado.")
        raise typer.Exit()

    typer.echo("\n🎮 Mundos encontrados:")
    for idx, world in enumerate(worlds, 1):
        typer.echo(f"[{idx}] {world.name}")

    choice = typer.prompt("Escolha o número do mundo", type=int)
    if not (1 <= choice <= len(worlds)):
        typer.echo("❌ Escolha inválida.")
        raise typer.Exit()

    selected_world = worlds[choice - 1]
    backup_file = zip_world(selected_world, edition)
    typer.echo(f"\n✅ Backup criado com sucesso em: {backup_file}")


if __name__ == "__main__":
    app()
