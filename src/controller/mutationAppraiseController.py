class MutationAppraiseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load(self):
        data = self.model.get_data(refresh=False)
        self.view.set_data(data)
        self.update_refresh()

    def refresh(self):
        if not self.model.can_refresh_today():
            self.view.set_status("Already refreshed today")
            return

        data = self.model.get_data(refresh=True)
        self.view.set_data(data)
        self.update_refresh()

    def update_refresh(self):
        self.view.set_refresh_label(
            "Last refreshed: " + self.model.get_last_refreshed_str()
        )