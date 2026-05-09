from pynput import keyboard


class HotkeyService:
    def __init__(self, automation_controller, mutation_controller):
        self.auto = automation_controller
        self.mut = mutation_controller
        self.listener = None

    def _on_press(self, key):
        #print(key)
        try:
            k = key.char.lower()
        except:
            k = str(key).replace("Key.", "")

        match k:
            case "p":
                self.auto.start()

            case "m":
                self.auto.stop()

            case "f3":
                self.auto.set_click1()

            case "f4":
                self.auto.set_click2()

            case "f5":
                self.auto.start_area_select()

    def start(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()