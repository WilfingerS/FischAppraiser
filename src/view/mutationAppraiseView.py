import tkinter as tk
from tkinter import ttk


class MutationAppraiseView:
    def __init__(self, root, controller, app_service):
        self.root = root
        self.controller = controller or None
        self.app_service = app_service

        self.mutations = []
        self.selected = set()

    def build(self):
        self.root.title(self.app_service.get_title())
        self.root.geometry("420x650")

        self.refresh_label = ttk.Label(self.root, text="Last refreshed: never")
        self.refresh_label.pack(pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load", command=self.controller.load).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.controller.refresh).pack(side="left", padx=5)

        self.selected_label = ttk.Label(self.root, text="Selected: None")
        self.selected_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)

        self.frame = ttk.Frame(self.canvas)

        for c in range(3):
            self.frame.columnconfigure(c, weight=1)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ----------------------------
    # VIEW API (called by controller)
    # ----------------------------

    def set_data(self, data):
        self.mutations = data
        self.render()

    def set_refresh_label(self, text):
        self.refresh_label.config(text=text)

    def set_status(self, text):
        self.refresh_label.config(text=text)

    def render(self):
        for w in self.frame.winfo_children():
            w.destroy()

        cols = 3

        for i, m in enumerate(self.mutations):
            btn = tk.Button(
                self.frame,
                text=m["name"],
                width=18
            )

            if m.get("color"):
                btn.config(bg=m["color"])

            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)