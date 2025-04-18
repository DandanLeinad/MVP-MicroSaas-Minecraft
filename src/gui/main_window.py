import tkinter as tk

from backup import core, detect_bedrock, detect_java


def run_gui():
    def selecionar_edicao():
        edicao = edicao_var.get()
        if edicao == "java":
            path = detect_java.get_java_worlds_path()
        elif edicao == "bedrock":
            path = detect_bedrock.get_bedrock_worlds_path()
        else:
            label_status.config(text="Edição inválida.")
            return

        if not path:
            label_status.config(
                text="❌ Caminho não encontrado. O Minecraft pode não estar instalado."  # NOQA
            )
            lista_mundos.delete(0, tk.END)  # Limpa a lista de mundos
            return

        mundos = core.list_worlds(path)
        lista_mundos.delete(
            0, tk.END
        )  # Limpa a lista de mundos antes de carregar novos
        if not mundos:
            label_status.config(text="❌ Nenhum mundo encontrado.")
            return

        for mundo in mundos:
            lista_mundos.insert(tk.END, mundo)

        label_status.config(text="Selecione um mundo para criar o backup.")

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

        core.make_backup(path, mundo, edicao)
        label_status.config(
            text=f"✅ Backup do mundo '{mundo}' criado com sucesso!"
        )

    root = tk.Tk()
    root.title("Minecraft Backup GUI")

    tk.Label(root, text="Selecione a edição do Minecraft:").pack(pady=5)

    edicao_var = tk.StringVar(value="java")
    tk.Radiobutton(root, text="Java", variable=edicao_var, value="java").pack()
    tk.Radiobutton(
        root, text="Bedrock", variable=edicao_var, value="bedrock"
    ).pack()

    tk.Button(root, text="Carregar Mundos", command=selecionar_edicao).pack(
        pady=10
    )

    lista_mundos = tk.Listbox(root, width=50, height=10)
    lista_mundos.pack(pady=5)

    tk.Button(root, text="Criar Backup", command=criar_backup).pack(pady=10)

    label_status = tk.Label(root, text="")
    label_status.pack(pady=5)

    tk.Button(root, text="Fechar", command=root.destroy).pack(pady=10)

    root.mainloop()
