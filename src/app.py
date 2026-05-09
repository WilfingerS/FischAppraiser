import tkinter as tk

from appConfig import AppConfig
from model.mutationService import MutationService
from view.mutationAppraiseView import MutationAppraiseView
from controller.mutationAppraiseController import MutationAppraiseController


if __name__ == "__main__":
    root = tk.Tk()

    app_service = AppConfig()

    model = MutationService(
        user_agent=app_service.get_title()
    )
    
    view = MutationAppraiseView(root, None, app_service)
    controller = MutationAppraiseController(model, view)
    view.controller = controller
    
    view.build()
    root.mainloop()