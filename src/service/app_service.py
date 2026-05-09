class AppService:
    def __init__(self):
        self.name = "Mutation Appraiser"
        self.version = "1.0"
        self.lang = "EN"
        self.author = "smolploom (Plum)"

    def get_title(self):
        return f"{self.name} v{self.version} ({self.lang})"
    def get_author(self):
        return f"{self.author}"
    
    def bind_keys(root, automation_controller, mutation_controller):
        # ----------------------------
        # START
        # ----------------------------
        def start(_=None):
            automation_controller.start()

        # ----------------------------
        # STOP
        # ----------------------------
        def stop(_=None):
            automation_controller.stop()

        # ----------------------------
        # MUTATION KEYBINDS
        # ----------------------------
        def f1(_=None):
            automation_controller.set_click1()

        def f2(_=None):
            automation_controller.set_click2()

        def f3(_=None):
            mutation_controller.start_area_select()  # if you have this wired

        # ----------------------------
        # BINDINGS
        # ----------------------------
        root.bind("p", start)
        root.bind("P", start)

        root.bind("m", stop)
        root.bind("M", stop)

        root.bind("<F1>", f1)
        root.bind("<F2>", f2)
        root.bind("<F3>", f3)