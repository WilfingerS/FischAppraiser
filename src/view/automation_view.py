import tkinter as tk


class AutomationView:
    def __init__(self, parent, app_service):
        self.parent = parent
        self.app_service = app_service
        self.controller = None

        # overlay selection
        self.overlay = None
        self.canvas = None
        self.rect = None

        self.start_x = 0
        self.start_y = 0

        self.area_callback = None
        self.selection_active = False

        # ----------------------------
        # UI STATE LABELS
        # ----------------------------
        self.click1_label = None
        self.click2_label = None
        self.area_label = None

        # delay vars (tk bound)
        self.delay_first_var = tk.StringVar(value="100")
        self.delay_second_var = tk.StringVar(value="100")
        self.delay_third_var = tk.StringVar(value="400")

    def set_controller(self, controller):
        self.controller = controller

    # =========================================================
    # UI BUILD
    # =========================================================

    def build(self):
        self.panel = tk.Frame(self.parent, padx=10, pady=10)
        self.panel.pack(fill="both", expand=True)

        title = tk.Label(
            self.panel,
            text="Automation Control Panel",
            font=("Arial", 14, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        # ----------------------------
        # INSTRUCTIONS
        # ----------------------------
        instructions = tk.Label(
            self.panel,
            text=(
                "How to use:\n"
                "F3 = Set Click 1\n"
                "F4 = Set Click 2\n"
                "F5 = Select Scan Area\n"
                "P = Start Automation\n"
                "M = Stop Automation\n"
            ),
            justify="left"
        )
        instructions.pack(anchor="w", pady=(0, 10))

        # ----------------------------
        # CLICK INFO
        # ----------------------------
        self.click1_label = tk.Label(self.panel, text="Click 1: not set")
        self.click1_label.pack(anchor="w")

        self.click2_label = tk.Label(self.panel, text="Click 2: not set")
        self.click2_label.pack(anchor="w")

        self.area_label = tk.Label(self.panel, text="Scan Area: not set")
        self.area_label.pack(anchor="w", pady=(0, 10))

        # ----------------------------
        # DELAYS
        # ----------------------------
        delay_frame = tk.LabelFrame(self.panel, text="Delays (ms)")
        delay_frame.pack(fill="x", pady=10)

        tk.Label(delay_frame, text="First Click Delay").grid(row=0, column=0, sticky="w")
        tk.Entry(delay_frame, textvariable=self.delay_first_var, width=10).grid(row=0, column=1)

        tk.Label(delay_frame, text="Second Click Delay").grid(row=1, column=0, sticky="w")
        tk.Entry(delay_frame, textvariable=self.delay_second_var, width=10).grid(row=1, column=1)

        tk.Label(delay_frame, text="Scan Delay").grid(row=2, column=0, sticky="w")
        tk.Entry(delay_frame, textvariable=self.delay_third_var, width=10).grid(row=2, column=1)

        # ----------------------------
        # BUTTONS
        # ----------------------------
        btn_frame = tk.Frame(self.panel)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Apply Delays",
            command=self.apply_delays
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Select Area",
            command=self.controller.start_area_select
        ).pack(side="left", padx=5)

    # =========================================================
    # UPDATE UI METHODS
    # =========================================================

    def update_click1(self, pos):
        if self.click1_label:
            self.click1_label.config(text=f"Click 1: {pos}")

    def update_click2(self, pos):
        if self.click2_label:
            self.click2_label.config(text=f"Click 2: {pos}")

    def update_area(self, area):
        if self.area_label:
            self.area_label.config(text=f"Scan Area: {area}")

    # =========================================================
    # DELAY HANDLING
    # =========================================================

    def apply_delays(self):
        try:
            self.controller.model.delay_first = int(self.delay_first_var.get())
            self.controller.model.delay_second = int(self.delay_second_var.get())
            self.controller.model.delay_third = int(self.delay_third_var.get())
        except ValueError:
            print("Invalid delay values")

    # =========================================================
    # AREA SELECTION OVERLAY
    # =========================================================

    def begin_area_selection(self, callback):
        self.area_callback = callback
        self.selection_active = True
        self._create_overlay()

    def _create_overlay(self):
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.25)
        self.overlay.attributes("-topmost", True)
        self.overlay.overrideredirect(True)

        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.overlay.bind("<Button-1>", self._start_drag)
        self.overlay.bind("<B1-Motion>", self._update_drag)
        self.overlay.bind("<ButtonRelease-1>", self._end_drag)
        self.overlay.bind("<Escape>", self._cancel)

    def _start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)

        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2
        )

    def _update_drag(self, event):
        if not self.rect:
            return

        self.canvas.coords(
            self.rect,
            self.start_x,
            self.start_y,
            event.x,
            event.y
        )

    def _end_drag(self, event):
        if not self.selection_active:
            return

        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        self.selection_active = False

        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

        if self.area_callback:
            self.area_callback((x1, y1, x2, y2))

    def _cancel(self, event=None):
        self.selection_active = False

        if self.overlay:
            self.overlay.destroy()
            self.overlay = None