import tkinter as tk

from service.app_service import AppService
from service.hotkey_service import HotkeyService

from model.mutation_model import MutationModel
from model.automation_model import AutomationModel

from controller.mutation_controller import MutationController
from controller.automation_controller import AutomationController

from view.mutation_view import MutationView
from view.automation_view import AutomationView


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fisch Appraiser")
    root.geometry("700x600")
    root.attributes("-topmost",True)
    root.attributes("-alpha",.75)
    
    app_service = AppService()

    # ----------------------------
    # LAYOUT
    # ----------------------------

    main = tk.Frame(root)
    main.pack(fill="both", expand=True)
    left = tk.Frame(main)
    left.pack(side="left", fill="both", expand=True)

    right = tk.Frame(main)
    right.pack(side="right", fill="both")

    # ----------------------------
    # MODELS
    # ----------------------------

    mutation_model = MutationModel(app_service.get_title())
    automation_model = AutomationModel()

    # ----------------------------
    # VIEWS
    # ----------------------------

    mutation_view = MutationView(left, app_service)
    automation_view = AutomationView(right, app_service)

    # ----------------------------
    # CONTROLLERS
    # ----------------------------

    mutation_controller = MutationController(mutation_model, mutation_view)
    automation_controller = AutomationController(automation_model, automation_view)

    mutation_view.set_controller(mutation_controller)
    automation_view.set_controller(automation_controller)

    # ----------------------------
    # LOAD DATA
    # ----------------------------

    mutation_controller.load()

    # IMPORTANT: keep automation model synced from mutation model
    automation_model.mutation_data = mutation_model.mutations
    automation_model.selected = mutation_model.selected

    automation_view.build()

    # ----------------------------
    # HOTKEYS (GLOBAL INPUT LAYER)
    # ----------------------------
    hotkeys = HotkeyService(automation_controller, mutation_controller)
    hotkeys.start()

    root.mainloop()