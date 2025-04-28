"""
Módulo gui/app.py:
- Define classe GuiApp para encapsular widgets, callbacks e loop principal.
- Facilita manutenção ao separar lógica da execução.
"""

import tkinter as tk
from tkinter import messagebox

from backup import core, detect_bedrock, detect_java


class GuiApp:
    def __init__(self):
        # Inicializa janela principal
        self.root = tk.Tk()
        self.root.title("Minecraft Backup GUI")
        # Variável para edição selecionada
        self.edicao_var = tk.StringVar(value="java")
        # Construção dos elementos da interface
        self._build_widgets()

    def _build_widgets(self):
        # Widgets de seleção de edição
        tk.Label(self.root, text="Selecione a edição do Minecraft:").pack(
            pady=5
        )
        tk.Radiobutton(
            self.root, text="Java", variable=self.edicao_var, value="java"
        ).pack()
        tk.Radiobutton(
            self.root,
            text="Bedrock",
            variable=self.edicao_var,
            value="bedrock",
        ).pack()
        tk.Button(
            self.root, text="Carregar", command=self._select_edition
        ).pack(pady=10)
        # Frames para listas de mundos e backups
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        # Lista de mundos e campo de descrição
        frame_mundos = tk.LabelFrame(frame, text="Mundos", padx=5, pady=5)
        frame_mundos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.list_mundos = tk.Listbox(frame_mundos, width=30, height=15)
        self.list_mundos.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame_mundos, text="Descrição (opcional):").pack(pady=(5, 0))
        self.desc_entry = tk.Entry(frame_mundos)
        self.desc_entry.pack(fill=tk.X, padx=5)
        tk.Button(
            frame_mundos, text="Criar Backup", command=self._create_backup
        ).pack(pady=5)
        # Lista de backups
        frame_backups = tk.LabelFrame(frame, text="Backups", padx=5, pady=5)
        frame_backups.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0)
        )
        self.list_backups = tk.Listbox(frame_backups, width=30, height=15)
        self.list_backups.pack(fill=tk.BOTH, expand=True)
        tk.Button(
            frame_backups,
            text="Restaurar Backup",
            command=self._restore_backup,
        ).pack(pady=5)
        # Label de status e botão de fechar
        self.label_status = tk.Label(self.root, text="")
        self.label_status.pack(pady=5)
        tk.Button(self.root, text="Fechar", command=self.root.destroy).pack(
            pady=10
        )

    def _select_edition(self):
        """Carrega mundos e backups para a edição selecionada."""
        ed = self.edicao_var.get()
        path = (
            detect_java.get_java_worlds_path()
            if ed == "java"
            else detect_bedrock.get_bedrock_worlds_path()
        )
        # Limpa listas e entradas
        self.list_mundos.delete(0, tk.END)
        self.list_backups.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        # Lista mundos
        self.worlds_list = core.list_worlds(path) if path else []
        if self.worlds_list:
            for folder, display in self.worlds_list:
                self.list_mundos.insert(tk.END, display)
        else:
            self.list_mundos.insert(tk.END, "(nenhum mundo encontrado)")
        # Lista backups
        backups = core.list_backups(ed)
        if backups:
            for fname, desc in backups:
                label = f"{fname} - {desc}" if desc else fname
                self.list_backups.insert(tk.END, label)
        else:
            self.list_backups.insert(tk.END, "(nenhum backup encontrado)")
        self.label_status.config(
            text=f"Listagem para edição {ed.capitalize()}"
        )

    def _create_backup(self):
        """Cria backup do mundo selecionado."""
        sel = self.list_mundos.curselection()
        if not sel:
            self.label_status.config(text="❌ Nenhum mundo selecionado.")
            return
        # mapeia display selecionado para folder_name
        display = self.list_mundos.get(sel)
        world = None
        for folder, disp in getattr(self, "worlds_list", []):
            if disp == display:
                world = folder
                break
        if not world:
            self.label_status.config(text="❌ Mundo inválido selecionado.")
            return
        ed = self.edicao_var.get()
        path = (
            detect_java.get_java_worlds_path()
            if ed == "java"
            else detect_bedrock.get_bedrock_worlds_path()
        )
        desc = self.desc_entry.get().strip()
        if any(c in desc for c in r"\/:*?\"<>|"):
            messagebox.showerror(
                "Erro", "Descrição contém caracteres inválidos."
            )
            return
        ok = core.make_backup(path, world, ed, desc)
        if ok:
            messagebox.showinfo(
                "Sucesso", f"Backup do mundo '{world}' criado com sucesso!"
            )
        else:
            messagebox.showerror(
                "Erro", f"Falha ao criar backup do mundo '{world}'."
            )
        # Atualiza lista de backups
        self.list_backups.delete(0, tk.END)
        for fname, d in core.list_backups(ed):
            label = f"{fname} - {d}" if d else fname
            self.list_backups.insert(tk.END, label)

    def _restore_backup(self):
        """Restaura backup selecionado."""
        sel = self.list_backups.curselection()
        if not sel:
            self.label_status.config(text="❌ Nenhum backup selecionado.")
            return
        entry = self.list_backups.get(sel)
        backup_name = entry.split(" - ", 1)[0]
        ed = self.edicao_var.get()
        path = (
            detect_java.get_java_worlds_path()
            if ed == "java"
            else detect_bedrock.get_bedrock_worlds_path()
        )
        ok = core.restore_backup(path, backup_name, ed)
        if ok:
            messagebox.showinfo(
                "Sucesso", f"Backup '{backup_name}' restaurado com sucesso!"
            )
        else:
            messagebox.showerror(
                "Erro", f"Falha ao restaurar backup '{backup_name}'."
            )
        self.label_status.config(text=f"Restaurar: {backup_name}")

    def run(self):
        # Inicia o loop de eventos da GUI
        self.root.mainloop()


def run_gui():
    app = GuiApp()
    app.run()
