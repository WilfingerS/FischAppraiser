class MutationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # ----------------------------
    # LOAD / REFRESH
    # ----------------------------

    def load(self):
        data = self.model.get_data(refresh=False)
        self.model.mutations = data
        self.view.set_data(data)

    def refresh(self):
        data = self.model.get_data(refresh=True)
        self.model.mutations = data
        self.view.set_data(data)

    # ----------------------------
    # TOGGLE MUTATIONS
    # ----------------------------

    def toggle_mutation(self, name):
        if name in self.model.selected:
            self.model.selected.remove(name)
        else:
            self.model.selected.append(name)

        self.view.set_selected(self.model.selected)
        self.view.render()

    # ----------------------------
    # AREA SELECTION FLOW (F3)
    # ----------------------------

    def start_area_select(self):
        self.view.begin_area_selection(self.set_area)

    def set_area(self, area):
        """
        Called by View after drag selection completes
        """
        self.model.set_area(area)
        self.view.update_area(area)