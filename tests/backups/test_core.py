"""
Módulo de testes para backup.core:
 - test_list_worlds: verifica listagem de mundos existentes (apenas diretórios).  # NOQA
 - test_list_worlds_not_found: retorna lista vazia para caminho inexistente.
 - test_list_backups_empty: sem arquivos de backup, retorna lista vazia.
 - test_list_backups: zips com/s sem metadata retornam (nome, descrição).
 - test_make_and_restore: cria backup e restaura mundo + mvp2.json.
"""

import json
import zipfile

import pytest

from backup.core import list_backups, list_worlds, make_backup, restore_backup


def test_list_worlds(tmp_path):
    """Verifica que list_worlds retorna apenas os diretórios presentes."""
    (tmp_path / "world1").mkdir()
    (tmp_path / "world2").mkdir()
    (tmp_path / "note.txt").write_text("x")
    worlds = list_worlds(str(tmp_path))
    assert set(worlds) == {"world1", "world2"}


def test_list_worlds_not_found():
    """Retorna [] quando o caminho não existe."""
    assert list_worlds("no_path") == []


@pytest.fixture()
def backup_dirs(tmp_path, monkeypatch):
    """Prepara diretórios temporários e override das constantes de backup."""
    base = tmp_path / "backups"
    java = base / "java"
    bedrock = base / "bedrock"
    java.mkdir(parents=True)
    bedrock.mkdir(parents=True)
    monkeypatch.setattr("backup.core.BACKUP_DIR", str(base))
    monkeypatch.setattr("backup.core.BACKUP_DIR_JAVA", str(java))
    monkeypatch.setattr("backup.core.BACKUP_DIR_BEDROCK", str(bedrock))
    return tmp_path


def write_zip(path, name, include_meta=True, desc=None):
    zip_path = path / f"{name}.zip"
    with zipfile.ZipFile(str(zip_path), "w") as z:
        z.writestr("dummy.txt", "data")
        if include_meta:
            meta = {"description": desc or "", "world": name}
            z.writestr("metadata.json", json.dumps(meta))
    return zip_path.name


def test_list_backups_empty(backup_dirs):
    """Sem zips no diretório, list_backups retorna lista vazia."""
    assert list_backups() == []
    assert list_backups("java") == []
    assert list_backups("bedrock") == []


def test_list_backups(backup_dirs):
    """Garante que zips com e sem metadata sejam listados corretamente."""
    base = backup_dirs / "backups"
    java = base / "java"
    bed = base / "bedrock"
    name1 = write_zip(java, "w1", include_meta=True, desc="d1")
    name2 = write_zip(bed, "w2", include_meta=False)
    # listar por edição
    java_b = list_backups("java")
    bed_b = list_backups("bedrock")
    assert (name1, "d1") in java_b
    assert (name2, "") in bed_b


def test_make_and_restore(backup_dirs, monkeypatch, tmp_path):
    """Cria um backup de um mundo e restaura, validando arquivos e metadados."""  # NOQA
    worlds = tmp_path / "worlds"
    worlds.mkdir()
    w = worlds / "mundo"
    w.mkdir()
    f = w / "file.txt"
    f.write_text("hello")
    # backup_dirs já configurou os diretórios
    base = backup_dirs / "backups"
    java = base / "java"
    # executa criação
    assert make_backup(str(worlds), "mundo", edition="java", description="tag")
    zips = list(java.iterdir())
    assert zips, "zip não criado"
    zname = zips[0].name
    with zipfile.ZipFile(str(java / zname), "r") as z:
        assert "mundo/file.txt" in z.namelist()
        meta = json.loads(z.read("metadata.json"))
        assert meta["description"] == "tag"
    # restaura
    dest = tmp_path / "dest"
    dest.mkdir()
    assert restore_backup(str(dest), zname, edition="java")
    assert (dest / "mundo" / "file.txt").exists()
    mf = dest / "mundo" / "mvp2.json"
    assert mf.exists()
    data = json.loads(mf.read_text(encoding="utf-8"))
    assert data["world"] == "mundo"
