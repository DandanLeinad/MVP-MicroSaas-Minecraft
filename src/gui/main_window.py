import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minecraft Backup Tool")

    def run(self):
        label = tk.Label(self.root, text="Bem-vindo ao Minecraft Backup Tool")
        label.pack(pady=20)
        self.root.mainloop()
