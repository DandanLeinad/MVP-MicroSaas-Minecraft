"""
Módulo de testes para backup.detect_java:
 - test_get_java_worlds_path_supported: valida caminhos para Windows, macOS e Linux. # NOQA
 - test_get_java_worlds_path_unsupported: retorna None para SO não suportado.
"""

import platform

import pytest

from backup.detect_java import get_java_worlds_path


@pytest.mark.parametrize(
    "system, expected_suffix",
    [
        ("Windows", "AppData\\Roaming\\.minecraft\\saves"),
        ("Darwin", "Library/Application Support/minecraft/saves"),
        ("Linux", ".minecraft/saves"),
    ],
)
def test_get_java_worlds_path_supported(monkeypatch, system, expected_suffix):
    """Retorna caminho correto de mundos para sistemas suportados."""
    monkeypatch.setattr(platform, "system", lambda: system)
    path = get_java_worlds_path()
    assert path is not None
    assert expected_suffix in path


def test_get_java_worlds_path_unsupported(monkeypatch):
    """Retorna None para sistema operacional não suportado."""
    monkeypatch.setattr(platform, "system", lambda: "UnknownOS")
    assert get_java_worlds_path() is None
    monkeypatch.setattr(platform, "system", lambda: "UnknownOS")
    assert get_java_worlds_path() is None
