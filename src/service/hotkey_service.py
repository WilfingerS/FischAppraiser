from pynput import keyboard


class HotkeyService:
    def __init__(self, automation_controller, mutation_controller):
        self.auto = automation_controller
        self.mut = mutation_controller
        self.listener = None

    def _on_press(self, key):
        print(key)
        # ----------------------------
        # LETTER KEYS
        # ----------------------------
        try:
            if key.char:
                k = key.char.lower()

                match k:
                    case "p":
                        self.auto.start()

                    case "m":
                        self.auto.stop()

        except AttributeError:
            # ----------------------------
            # FUNCTION KEYS
            # ----------------------------
            match key:

                case keyboard.Key.f3:
                    self.auto.set_click1()

                case keyboard.Key.f4:
                    self.auto.set_click2()

                case keyboard.Key.f5:
                    self.auto.start_area_select()

    def start(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()