import tkinter as tk
from tkinter import messagebox

from backup import core, detect_bedrock, detect_java


def run_gui():
    def selecionar_edicao():
        edicao = edicao_var.get()
        # Detecta caminho de mundos
        if edicao == "java":
            path = detect_java.get_java_worlds_path()
        elif edicao == "bedrock":
            path = detect_bedrock.get_bedrock_worlds_path()
        else:
            label_status.config(text="Edição inválida.")
            return
        # Limpa listas
        lista_mundos.delete(0, tk.END)
        lista_backups.delete(0, tk.END)
        desc_entry.delete(0, tk.END)

        # Carrega mundos
        worlds = core.list_worlds(path)
        if worlds:
            for m in worlds:
                lista_mundos.insert(tk.END, m)
        else:
            lista_mundos.insert(tk.END, "(nenhum mundo encontrado)")

        # Carrega backups
        backups_data = core.list_backups(edicao)
        if backups_data:
            for fname, desc in backups_data:
                label = f"{fname} - {desc}" if desc else fname
                lista_backups.insert(tk.END, label)
        else:
            lista_backups.insert(tk.END, "(nenhum backup encontrado)")

        label_status.config(
            text=(
                "Listagem de mundos e backups para edição "
                f"{edicao.capitalize()}"
            )
        )

    def criar_backup():
        selecionado = lista_mundos.curselection()
        if not selecionado:
            label_status.config(text="❌ Nenhum mundo selecionado.")
            return

        mundo = lista_mundos.get(selecionado)
        edicao = edicao_var.get()
        path = (
            detect_java.get_java_worlds_path()
            if edicao == "java"
            else detect_bedrock.get_bedrock_worlds_path()
        )

        # Coleta e valida descrição
        desc = desc_entry.get().strip()
        if any(c in desc for c in r"\/:*?\"<>|"):
            messagebox.showerror(
                "Erro", "Descrição contém caracteres inválidos."
            )
            return

        sucesso = core.make_backup(path, mundo, edicao, desc)
        # Notificação via pop-up
        if sucesso:
            msg = f"Backup do mundo '{mundo}' criado com sucesso!"
            messagebox.showinfo("Sucesso", msg)
        else:
            err_msg = f"Falha ao criar backup do mundo '{mundo}'."
            messagebox.showerror("Erro", err_msg)
        # Atualiza lista de backups com descrições
        lista_backups.delete(0, tk.END)
        for fname, desc in core.list_backups(edicao):
            label = f"{fname} - {desc}" if desc else fname
            lista_backups.insert(tk.END, label)

    def restaurar_backup():
        selecionado = lista_backups.curselection()
        if not selecionado:
            label_status.config(text="❌ Nenhum backup selecionado.")
            return
        entry = lista_backups.get(selecionado)
        # extrai nome do arquivo antes de ' - '
        backup_name = entry.split(" - ", 1)[0]
        edicao = edicao_var.get()
        path = (
            detect_java.get_java_worlds_path()
            if edicao == "java"
            else detect_bedrock.get_bedrock_worlds_path()
        )
        sucesso = core.restore_backup(path, backup_name, edicao)
        # Notificação via pop-up
        if sucesso:
            msg = f"Backup '{backup_name}' restaurado com sucesso!"
            messagebox.showinfo("Sucesso", msg)
        else:
            err_msg = f"Falha ao restaurar backup '{backup_name}'."
            messagebox.showerror("Erro", err_msg)
        label_status.config(text=f"Restaurar backup: {backup_name}")

    root = tk.Tk()
    root.title("Minecraft Backup GUI")

    tk.Label(root, text="Selecione a edição do Minecraft:").pack(pady=5)

    edicao_var = tk.StringVar(value="java")
    tk.Radiobutton(root, text="Java", variable=edicao_var, value="java").pack()
    tk.Radiobutton(
        root, text="Bedrock", variable=edicao_var, value="bedrock"
    ).pack()

    # Botão para carregar mundos e backups
    tk.Button(root, text="Carregar", command=selecionar_edicao).pack(pady=10)

    # Frames para organização lado a lado
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10)

    # Frame de mundos
    frame_mundos = tk.LabelFrame(frame, text="Mundos", padx=5, pady=5)
    frame_mundos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    lista_mundos = tk.Listbox(frame_mundos, width=30, height=15)
    lista_mundos.pack(fill=tk.BOTH, expand=True)
    # Campo opcional de descrição/tag
    tk.Label(frame_mundos, text="Descrição (opcional):").pack(pady=(5, 0))
    desc_entry = tk.Entry(frame_mundos)
    desc_entry.pack(fill=tk.X, padx=5)
    btn_backup = tk.Button(
        frame_mundos, text="Criar Backup", command=criar_backup
    )
    btn_backup.pack(pady=5)

    # Frame de backups
    frame_backups = tk.LabelFrame(frame, text="Backups", padx=5, pady=5)
    frame_backups.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    lista_backups = tk.Listbox(frame_backups, width=30, height=15)
    lista_backups.pack(fill=tk.BOTH, expand=True)
    btn_restore = tk.Button(
        frame_backups, text="Restaurar Backup", command=restaurar_backup
    )
    btn_restore.pack(pady=5)

    label_status = tk.Label(root, text="")
    label_status.pack(pady=5)

    tk.Button(root, text="Fechar", command=root.destroy).pack(pady=10)

    root.mainloop()
