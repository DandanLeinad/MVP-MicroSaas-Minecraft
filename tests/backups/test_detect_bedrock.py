"""
Módulo de testes para backup.detect_bedrock:
 - test_get_bedrock_worlds_path_windows: deve retornar caminho de mundos para Bedrock no Windows. # NOQA
 - test_get_bedrock_worlds_path_non_windows: deve retornar None em SO não suportado. # NOQA
"""

import platform

from backup.detect_bedrock import get_bedrock_worlds_path


def test_get_bedrock_worlds_path_windows(monkeypatch):
    """Retorna um caminho válido com 'com.mojang' quando o SO for Windows."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    path = get_bedrock_worlds_path()
    assert path is not None
    assert "com.mojang" in path


def test_get_bedrock_worlds_path_non_windows(monkeypatch):
    """Retorna None quando o SO não for Windows."""
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert get_bedrock_worlds_path() is None
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert get_bedrock_worlds_path() is None
