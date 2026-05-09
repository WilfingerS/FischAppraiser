import tkinter as tk


class MutationView:
    def __init__(self, parent, app_service):
        self.parent = parent
        self.app_service = app_service
        self.controller = None

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        self.mutations = []
        self.selected = []
        self.row_widgets = {}
    # ----------------------------
    # CONTROLLER LINK
    # ----------------------------
    def set_controller(self, controller):
        self.controller = controller
    # ----------------------------
    # DATA
    # ----------------------------
    def set_data(self, data):
        self.mutations = data
        self.widget_build()
        self.render()

    def set_selected(self, selected):
        self.selected = selected

    # ----------------------------
    # UI BUILD
    # ----------------------------

    def widget_build(self):
        for w in self.frame.winfo_children():
            w.destroy()

        self.row_widgets = {}

        cols = 2

        for i, m in enumerate(self.mutations):
            name = m["name"]
            color = m.get("color")

            row = i // cols
            col = i % cols

            cell = tk.Frame(self.frame)
            cell.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            btn = tk.Button(
                cell,
                text=name,
                width=18,
                command=lambda n=name: self.controller.toggle_mutation(n)
            )

            if color:
                btn.config(bg=color)

            btn.grid(row=0, column=0)

            check = tk.Label(cell, text="☐", font=("Arial", 16), width=2)
            check.grid(row=0, column=1)

            self.row_widgets[name] = {
                "check": check
            }


    # ----------------------------
    # RENDER
    # ----------------------------

    def render(self):
        for name, widgets in self.row_widgets.items():
            widgets["check"].config(
                text="☑" if name in self.selected else "☐"
            )