"""
Módulo de testes para cli.cli_main:
 - test_invalid_edition: roda run_cli com edição inválida e espera mensagem de erro.  # NOQA
 - test_missing_path: simula get_java_worlds_path retornando None e verifica mensagem de caminho não encontrado.
 - test_menu_called: simula sucesso na detecção de Bedrock e garante que core.menu é invocado com os parâmetros corretos.
"""

import builtins

from cli.cli_main import run_cli


def test_invalid_edition(monkeypatch, capsys):
    """Exibe 'Edição inválida.' quando o input não é 'java' nem 'bedrock'."""
    monkeypatch.setattr(builtins, "input", lambda prompt="": "unknown")
    run_cli()
    captured = capsys.readouterr().out
    assert "Edição inválida" in captured


def test_missing_path(monkeypatch, capsys):
    """Quando get_java_worlds_path retorna None, exibe mensagem de caminho não encontrado."""  # NOQA
    monkeypatch.setattr(builtins, "input", lambda prompt="": "java")
    import cli.cli_main as module

    monkeypatch.setattr(
        module.detect_java, "get_java_worlds_path", lambda: None
    )
    run_cli()
    captured = capsys.readouterr().out
    assert "❌ Caminho não encontrado" in captured


def test_menu_called(monkeypatch):
    """Verifica que core.menu é chamado com path e edição corretos"""
    monkeypatch.setattr(builtins, "input", lambda prompt="": "bedrock")
    import cli.cli_main as module

    # simula caminho válido
    monkeypatch.setattr(
        module.detect_bedrock, "get_bedrock_worlds_path", lambda: "/fake/path"
    )
    called = {}

    def fake_menu(path, edition):
        called["path"] = path
        called["edition"] = edition

    monkeypatch.setattr(module.core, "menu", fake_menu)
    run_cli()
    assert called == {"path": "/fake/path", "edition": "bedrock"}
    run_cli()
    assert called == {"path": "/fake/path", "edition": "bedrock"}
