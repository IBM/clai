#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from typing import List

from clai.emulator.emulator_docker_bridge import EmulatorDockerBridge
from clai.emulator.log_window import LogWindow
from clai.emulator.toggled_frame import ToggledFrame
from clai.emulator.emulator_presenter import EmulatorPresenter

# pylint: disable=too-many-instance-attributes,protected-access,attribute-defined-outside-init,too-many-public-methods
from clai.server.command_runner.clai_last_info_command_runner import InfoDebug


class ClaiEmulator:

    def __init__(self, emulator_docker_bridge: EmulatorDockerBridge):
        self.presenter = EmulatorPresenter(emulator_docker_bridge,
                                           self.on_skills_ready,
                                           self.on_server_running,
                                           self.on_server_stopped)

    def launch(self):
        self.root = tk.Tk()
        self.root.wait_visibility(self.root)
        self.title_font = Font(size=16, weight='bold')
        self.bold_font = Font(weight='bold')

        self.root.geometry("900x600")

        style = ttk.Style(self.root)
        style.configure("TLable", bg="black")

        self.add_toolbar(self.root)
        self.add_send_command_box(self.root)
        self.add_list_commands(self.root)

        self.root.protocol("WM_DELETE_WINDOW", lambda root=self.root: self.on_closing(root))
        self.root.createcommand('exit', lambda root=self.root: self.on_closing(root))

        self.root.mainloop()

    def on_closing(self, root):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.presenter.stop_server()
            root.destroy()

    def on_skills_ready(self, skills_as_array: List[str]):
        self.selected_skills_dropmenu.configure(state="active")
        self.selected_skills_dropmenu["menu"].delete(0, 'end')

        for skill in skills_as_array[1:-1]:
            name_skill, active = self.clear_text(skill)
            self.selected_skills_dropmenu["menu"].add_command(
                label=name_skill,
                command=tk._setit(self.selected_skills, name_skill))

            if active:
                self.presenter.current_active_skill = self.extract_skill_name(name_skill)[0]
                self.selected_skills.set(name_skill)

    def on_server_running(self):
        self.run_button.configure(image=self.stop_image)
        self.loading_text.set("Starting CLAI. It will take a while")
        self.__listen_messages()

    def on_server_stopped(self):
        self.run_button.configure(image=self.run_image)

    # pylint: disable=unused-argument
    def on_skill_selected(self, *args):
        self.loading_text.set("")
        print(f"new skills {self.selected_skills.get()}")
        skill_name = self.extract_skill_name(self.selected_skills.get())[0]
        self.presenter.select_skill(skill_name)


    def add_detail_label(self, parent: ttk.Frame, title: str, text_value: str, side: str):
        row = ttk.Frame(parent)
        title_label = ttk.Label(parent, text=title, font=self.bold_font, anchor='n', padding=(10, 0, 0, 0))
        title_label.pack(side=side, fill=tk.BOTH)
        row_value = ttk.Label(parent, text=text_value, wraplength=250, anchor='nw')

        if side == tk.LEFT:
            row_value.pack(side=side, fill=tk.BOTH, expand=True)
        else:
            row_value.pack(side=side, fill=tk.BOTH, before=title_label)

        row.pack(side=side, fill=tk.BOTH, expand=True)

    def add_row(self, response: str, info: InfoDebug):
        response = self.clean_message(response)
        toggled_frame = ToggledFrame(self.frame, text=response, relief=tk.RAISED, borderwidth=1)
        toggled_frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        first_row = ttk.Frame(toggled_frame.sub_frame)
        first_row.pack(fill="x", expand=True)
        self.add_detail_label(first_row, "Original:", info.command, side=tk.LEFT)
        self.add_detail_label(first_row, "Id:", info.command_id, side=tk.RIGHT)

        second_row = ttk.Frame(toggled_frame.sub_frame)
        second_row.pack(fill="x", expand=True)
        self.add_detail_label(second_row, 'Description:', self.remove_emoji(info.action_suggested.description), tk.LEFT)
        self.add_detail_label(second_row, 'Confidence:', f'{info.action_suggested.confidence}', tk.RIGHT)
        self.add_detail_label(second_row, 'Force:', f'{info.action_suggested.execute}', tk.RIGHT)

        third_row = ttk.Frame(toggled_frame.sub_frame)
        third_row.pack(fill="x", expand=True)
        self.add_detail_label(third_row, 'Agent:', text_value=info.action_suggested.agent_owner, side=tk.LEFT)
        self.add_detail_label(third_row, 'Sugestion:', text_value=info.action_suggested.suggested_command,
                              side=tk.RIGHT)
        self.add_detail_label(third_row, 'Applied:', text_value=f'{info.already_processed}', side=tk.RIGHT)

        fourth_row = ttk.Frame(toggled_frame.sub_frame)
        fourth_row.pack(fill="x", expand=True)
        process_text = ','.join(list(map(lambda process: process.name, info.processes.last_processes)))
        self.add_detail_label(fourth_row, 'Processes:', text_value=f'{process_text}', side=tk.LEFT)

        post_title_frame = ttk.Frame(toggled_frame.sub_frame)
        post_title_frame.pack(fill='x', expand=True)
        ttk.Label(post_title_frame, text=f'Post execution', anchor='center', font=self.title_font). \
            pack(side=tk.LEFT, padx=10, fill='x', expand=True)

        fifth_row = ttk.Frame(toggled_frame.sub_frame)
        fifth_row.pack(fill="x", expand=True)

        post_description = ""
        post_confidence = 0
        if info.action_post_suggested:
            post_description = info.action_post_suggested.description
            post_confidence = info.action_post_suggested.confidence

        self.add_detail_label(fifth_row, 'Description:', text_value=f'{self.remove_emoji(post_description)}',
                              side=tk.LEFT)
        self.add_detail_label(fifth_row, 'Confidence:', text_value=f'{post_confidence}', side=tk.RIGHT)

        self.root.after(100, self.__scroll_down_after_create)

    def __scroll_down_after_create(self):
        self.canvas.yview_moveto(1.0)

    def add_send_command_box(self, root):
        button_bar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        send_button = tk.Button(button_bar_frame, padx=10, text=u"\u2713", command=self.on_send_click)
        send_button.pack(side=tk.RIGHT, padx=5)
        self.text_input = tk.StringVar()
        send_edit_text = tk.Entry(button_bar_frame, textvariable=self.text_input)
        send_edit_text.bind('<Return>', self.on_enter)
        send_edit_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        button_bar_frame.pack(side=tk.BOTTOM, pady=2, fill=tk.X)

    def add_toolbar(self, root):
        toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.add_play_button(toolbar)
        self.add_refresh_button(toolbar)
        self.add_log_button(toolbar)
        self.add_skills_selector(root, toolbar)
        self.add_loading_progress(toolbar)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def add_skills_selector(self, root, toolbar):
        label = ttk.Label(toolbar, text=u'Skills')
        label.pack(side=tk.LEFT, padx=2)

        self.selected_skills = tk.StringVar(root)
        self.selected_skills.set("")
        self.selected_skills.trace("w", self.on_skill_selected)
        self.selected_skills_dropmenu = tk.OptionMenu(toolbar, self.selected_skills, [])
        self.selected_skills_dropmenu.configure(state="disabled")
        self.selected_skills_dropmenu.pack(side=tk.LEFT, padx=2)

    def add_play_button(self, toolbar):
        path = os.path.dirname(os.path.abspath(__file__))
        self.run_image = tk.PhotoImage(file=f"{path}/run.gif")
        self.stop_image = tk.PhotoImage(file=f"{path}/stop.gif")
        self.run_button = ttk.Button(toolbar, image=self.run_image, command=self.on_run_click)
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)

    def add_refresh_button(self, toolbar):
        path = os.path.dirname(os.path.abspath(__file__))
        self.refresh_image = tk.PhotoImage(file=f"{path}/refresh.png")
        refresh_button = ttk.Button(toolbar, image=self.refresh_image, command=self.on_refresh_click)
        refresh_button.pack(side=tk.LEFT, padx=2, pady=2)

    def add_log_button(self, toolbar):
        path = os.path.dirname(os.path.abspath(__file__))
        self.log_image = tk.PhotoImage(file=f"{path}/refresh.png")
        log_button = ttk.Button(toolbar, image=self.refresh_image, command=self.log_window)
        log_button.pack(side=tk.LEFT, padx=2, pady=2)

    def add_loading_progress(self, toolbar):
        self.loading_text = tk.StringVar()
        loading_label = ttk.Label(toolbar, textvariable=self.loading_text)
        loading_label.pack(side=tk.LEFT, padx=2)

    def log_window(self):
        self.log_window = LogWindow(self.root, self.presenter)

    # pylint: disable=unused-argument
    def on_enter(self, event):
        self.send_command(self.text_input.get())

    def on_send_click(self):
        self.send_command(self.text_input.get())

    @staticmethod
    def clean_message(text: str):
        text = text[text.find('\n'):]
        text = re.sub('[[0-9;]*m', '', text)
        return text[:text.find(']0;') - 3]

    def send_command(self, command):
        self.presenter.send_message(command)
        self.text_input.set("")

    def on_run_click(self):
        if not self.presenter.server_running:
            self.presenter.run_server()
        else:
            self.presenter.stop_server()

    def on_refresh_click(self):
        self.presenter.refresh_files()

    @staticmethod
    def on_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def canvas_resize(self, event, canvas):
        canvas_width = event.width
        canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def add_list_commands(self, root):
        canvas = tk.Canvas(root, borderwidth=0)
        self.frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        self.canvas_frame = canvas.create_window((4, 4), window=self.frame, anchor="nw")

        canvas.bind('<Configure>', lambda event, canvas=canvas: self.canvas_resize(event, canvas))
        self.frame.bind("<Configure>", lambda event, canvas=canvas: self.on_configure(canvas))
        self.frame.bind_all("<MouseWheel>", lambda event, canvas=canvas: canvas.yview_scroll(-1 * event.delta, "units"))
        self.canvas = canvas

    @staticmethod
    def clear_text(skill):
        active = '☑' in skill
        skill_without_tick = skill.replace('☑\x1b[32m ', '').replace('\x1b[0m', '').replace('◻', '').strip()
        return skill_without_tick, active

    @staticmethod
    def extract_skill_name(skill):
        installed = '(Installed)' in skill
        return skill.replace('(Installed)', '').replace('(Not Installed)', '').strip(), installed

    @staticmethod
    def remove_emoji(description):
        if not description:
            return ''

        char_list = [description[j] for j in range(len(description)) if ord(description[j]) in range(65536)]
        description = ''
        for char in char_list:
            description = description + char
        return description

    def __listen_messages(self):
        self.presenter.retrieve_messages(self.add_row)
        self.root.after(3000, self.__listen_messages)
