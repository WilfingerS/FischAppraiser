class AutomationModel:
    def __init__(self):
        self.running = False

        self.click1 = None
        self.click2 = None
        self.area = None

        self.selected = []
        self.mutation_data = []

        self.delay_first = 100
        self.delay_second = 100
        self.delay_third = 400

        self.move_pause = 0.3
        self.roam_radius = 2
        self.tolerance = 2

    # ----------------------------
    # REQUIRED FIX
    # ----------------------------

    def set_click1(self, pos):
        self.click1 = pos

    def set_click2(self, pos):
        self.click2 = pos

    def set_area(self, area):
        self.area = area