import tkinter as tk


def run_gui():
    root = tk.Tk()
    root.title("Minecraft Backup GUI")

    label = tk.Label(root, text="Bem-vindo ao Backup de Mundos do Minecraft!")
    label.pack(padx=20, pady=20)

    btn = tk.Button(root, text="Fechar", command=root.destroy)
    btn.pack(pady=10)

    root.mainloop()
