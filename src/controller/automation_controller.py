import threading
import time
import random
import mss
import numpy as np
import pydirectinput
import pyautogui

class AutomationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # ----------------------------
    # START / STOP
    # ----------------------------

    def start(self):
        if self.model.running:
            return
        
        print("Started?")

        if not self.model.click1 or not self.model.click2:
            return
        print("Clicker are there")
        if not self.model.area:
            return
        print("area is there")
        if not self.model.selected:
            return

        self.model.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        print("Stopped?")
        self.model.running = False

    # ----------------------------
    # MAIN LOOP
    # ----------------------------

    def loop(self):
        while self.model.running:

            self._click(self.model.click1)
            time.sleep(self.model.delay_first/1000)

            self._click(self.model.click2)
            time.sleep(self.model.delay_second/1000)

            self._scan_area()

            time.sleep(self.model.delay_third/1000)

    # ----------------------------
    # CLICKING
    # ----------------------------
    def _click(self, pos):
        if not pos:
            return
        x, y = int(pos.x), int(pos.y)
        pydirectinput.moveTo(x, y)
        time.sleep(0.1)
        pydirectinput.click()
        print("clicked")

    # ----------------------------
    # SCANNING (CORE LOGIC)
    # ----------------------------

    def _scan_area(self):
        x1, y1, x2, y2 = self.model.area
        w, h = x2 - x1, y2 - y1

        targets = [
            (m["name"], self._hex_to_rgb(m["color"]))
            for m in self.model.mutation_data
            if m["name"] in self.model.selected
        ]

        if not targets:
            return

        with mss.mss() as sct:
            img = np.array(sct.grab({
                "left": x1,
                "top": y1,
                "width": w,
                "height": h
            }))[:, :, :3]

            r = img[:, :, 0]
            g = img[:, :, 1]
            b = img[:, :, 2]

            tol = self.model.tolerance

            for name, (rt, gt, bt) in targets:
            
                mask = (
                    (abs(r - rt) <= tol) &
                    (abs(g - gt) <= tol) &
                    (abs(b - bt) <= tol)
                )

                if np.any(mask):
                    self.model.running = False

                    # ✔ ONLY safe UI callback (not logic coupling)
                    self.view.show_found(name)

                    return

    # ----------------------------
    # UTIL
    # ----------------------------

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.replace("#", "").replace("0x", "")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # ----------------------------
    # INPUT HANDLERS (UI → STATE)
    # ----------------------------

    def set_click1(self):
        pos = pyautogui.position()
        self.model.click1 = pos
        self.view.update_click1(pos)

    def set_click2(self):
        pos = pyautogui.position()
        self.model.click2 = pos
        self.view.update_click2(pos)

    def start_area_select(self):
        self.view.begin_area_selection(self.set_area)

    def set_area(self, area):
        print("CONTROLLER RECEIVED AREA:", area)
        self.model.set_area(area)          # REQUIRED for automation
        self.view.update_area(area)        # UI update