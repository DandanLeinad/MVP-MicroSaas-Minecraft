"""
Módulo de testes para gui.app:
 - test_initial_state: verifica widgets iniciais e variáveis padrão.
 - test_select_edition_empty: sem mundos e backups, listas mostram mensagem apropriada.
 - test_create_backup_no_selection: sem seleção, label_status indica erro.
 - test_create_backup_invalid_desc: seleção válida mas descrição inválida aciona showerror.
 - test_create_backup_success: make_backup com sucesso aciona showinfo e atualiza lista_backups.
 - test_restore_backup_no_selection: sem backup selecionado, label_status indica erro.
 - test_restore_backup_success: restore_backup com sucesso aciona showinfo e atualiza label_status.
"""

import tkinter as tk

import pytest

from backup import core
from gui.app import GuiApp

tkmb = tk
from tkinter import messagebox


@pytest.fixture
def app(monkeypatch):
    """Cria instância de GuiApp com root oculto para testes."""
    gui = GuiApp()
    # Evita mostrar janela
    gui.root.withdraw()
    return gui


def test_initial_state(app):
    """Variáveis e listas iniciais estão vazias e edição padrão é Java."""
    assert app.edicao_var.get() == "java"
    # as listas não foram populadas antes de select_edition
    assert app.list_mundos.size() == 0
    assert app.list_backups.size() == 0


def test_select_edition_empty(app, monkeypatch):
    """Se não houver mundos ou backups, listas indicam mensagem de vazio."""
    # Override detecção de caminhos
    monkeypatch.setattr(core, "list_worlds", lambda path: [])
    monkeypatch.setattr(core, "list_backups", lambda ed: [])
    app._select_edition()
    # Mensagem de nenhum mundo/backups
    assert app.list_mundos.get(0) == "(nenhum mundo encontrado)"
    assert app.list_backups.get(0) == "(nenhum backup encontrado)"
    assert "Listagem para edição Java" in app.label_status["text"]


def test_create_backup_no_selection(app):
    """Sem seleção de mundo, label_status indica erro."""
    app.list_mundos.delete(0, tk.END)
    # garante empty
    app._create_backup()
    assert "❌ Nenhum mundo selecionado." == app.label_status["text"]


def test_create_backup_invalid_desc(app, monkeypatch):
    """Seleção válida mas descrição inválida chama showerror."""
    # Insere um mundo e seleciona
    app.list_mundos.insert(tk.END, "mw")
    app.list_mundos.selection_set(0)
    # mock detect path e desc invalida
    app.desc_entry.insert(0, "inv:|")
    shows = []
    monkeypatch.setattr(
        messagebox, "showerror", lambda title, msg: shows.append((title, msg))
    )
    app._create_backup()
    assert shows and "Descrição contém caracteres inválidos." in shows[0][1]


def test_create_backup_success(app, monkeypatch):
    """make_backup True chama showinfo e lista de backups é atualizada."""
    # setup worlds list and selection
    app.list_mundos.insert(tk.END, "w")
    app.list_mundos.selection_set(0)
    app.desc_entry.insert(0, "tag")
    # mock detect paths
    monkeypatch.setattr(core, "make_backup", lambda p, w, e, d: True)
    monkeypatch.setattr(core, "list_backups", lambda e: [("b.zip", "tag")])
    infos = []
    monkeypatch.setattr(
        messagebox, "showinfo", lambda title, msg: infos.append((title, msg))
    )
    app._create_backup()
    # showinfo foi chamado com sucesso
    assert infos and "criado com sucesso" in infos[0][1]
    # lista_backup atualizada
    assert "b.zip - tag" in app.list_backups.get(0)


def test_restore_backup_no_selection(app):
    """Sem seleção de backup, label_status indica erro."""
    app.list_backups.delete(0, tk.END)
    app._restore_backup()
    assert "❌ Nenhum backup selecionado." == app.label_status["text"]


def test_restore_backup_success(app, monkeypatch):
    """restore_backup True chama showinfo e atualiza label_status."""
    # setup backups list and selection
    app.list_backups.insert(tk.END, "x.zip")
    app.list_backups.selection_set(0)
    monkeypatch.setattr(core, "restore_backup", lambda p, n, e: True)
    infos = []
    monkeypatch.setattr(
        messagebox, "showinfo", lambda title, msg: infos.append((title, msg))
    )
    app._restore_backup()
    assert infos and "restaurado com sucesso" in infos[0][1]
    assert "Restaurar: x.zip" == app.label_status["text"]
    monkeypatch.setattr(
        messagebox, "showinfo", lambda title, msg: infos.append((title, msg))
    )
    app._restore_backup()
    assert infos and "restaurado com sucesso" in infos[0][1]
    assert "Restaurar: x.zip" == app.label_status["text"]
