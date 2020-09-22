import tkinter as tk
from tkinter import ttk


class LogWindow:
    def __init__(self, root, presenter):
        self.root = root
        self.presenter = presenter
        self.autoscroll_enable = tk.IntVar()

        window = tk.Toplevel(self.root)
        window.geometry("900x600")
        self.add_toolbar(window)

        self.text_gui = tk.Text(window, height=6, width=40)
        self.text_gui.configure(state=tk.DISABLED)
        vsb = ttk.Scrollbar(window, orient="vertical", command=self.text_gui.yview)
        self.text_gui.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.text_gui.pack(side="left", fill="both", expand=True)
        presenter.attach_log(self.add_log_data)

    def add_toolbar(self, window):
        toolbar = tk.Frame(window, bd=1, relief=tk.RAISED)
        self.autoscroll_button = tk.Checkbutton(
            toolbar, text="Auto Scroll", relief=tk.SOLID, var=self.autoscroll_enable
        )
        self.autoscroll_button.pack(pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def add_log_data(self, chunk):
        self.text_gui.configure(state=tk.NORMAL)
        self.text_gui.insert("end", chunk)
        if self.autoscroll_enable.get() == 1:
            self.text_gui.see("end")
        self.text_gui.configure(state=tk.DISABLED)
