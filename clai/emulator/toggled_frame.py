#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os

import tkinter as tk
from tkinter import ttk


# pylint: disable=too-many-ancestors,keyword-arg-before-vararg
class ToggledFrame(tk.Frame):
    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=True)

        tk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=True)

        path = os.path.dirname(os.path.abspath(__file__))
        self.expand_more_image = tk.PhotoImage(file=f"{path}/expand_less.gif")
        self.expand_less_image = tk.PhotoImage(file=f"{path}/expand_more.gif")

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, image=self.expand_more_image,
                                             command=self.toggle, variable=self.show, style='TLabel')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(image=self.expand_less_image)
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(image=self.expand_more_image)
