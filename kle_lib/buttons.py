from typing import List, Dict
import pickle

button_types = {
    "Momentary": 0,
    "Toggleable": 1
}

HEADER = (0xF0, 0x0, 0x20, 0x6B, 0x7F, 0x42)
LCD_TEXT_HEADER = (0x4, 0x0, 0x60, 0x01)
LCD_TEXT_NEWLINE = (0x0, 0x2)
PAD_LIGHT_HEADER = (0x2, 0x0, 0x16)
BTN_LIGHT_HEADER = (0x2, 0x0, 0x10)
FOOTER = (0xF7,)

class KLE_Control:
    def __init__(self):
        self.value = 0
    def __getstate__(self):
        return self.__dict__.copy()
    def __setstate__(self, dict):
        self.__dict__.update(dict)

class KLE_Buttons(KLE_Control):
    def __init__(self):
        super().__init__()
        self.type = 0

    def handlePress(self, dawCtrl, *func):
        if self.type == 0:
            self.lightUp(dawCtrl)
            try:
                func[0]
            except IndexError:
                pass
        elif self.type == 1:
            if self.value == 0:
                self.lightUp(dawCtrl)
                self.value = 127
                try:
                    func[0]
                except IndexError:
                    pass
            else:
                self.lightDown(dawCtrl)
                self.value = 0
                try:
                    func[1]
                except IndexError:
                    pass

    def handleDepress(self, dawCtrl, *func):
        if self.type == 0:
            self.lightDown(dawCtrl)
            self.value = 0
        try:
            func[0]
        except IndexError:
            pass

    def lightUp(self, dawCtrl):
        pass
    def lightDown(self, dawCtrl):
        pass

class KLE_Button(KLE_Buttons):
    def __init__(self):
        super().__init__()
        self.name = "Generic Button"
        self.inDawCode = 0
        self.lightCode = 0
        self.se = False
    
    def lightUp(self, dawCtrl):
        if self.se:
            dawCtrl.send_message(HEADER + BTN_LIGHT_HEADER + (self.lightCode, 127) + FOOTER)
        else:
            dawCtrl.send_message((0x90, self.lightCode, 127))

    def lightDown(self, dawCtrl):
        if self.se:
            dawCtrl.send_message(HEADER + BTN_LIGHT_HEADER + (self.lightCode, 0) + FOOTER)
        else:
            dawCtrl.send_message((0x90, self.lightCode, 0))

class KLE_Pad(KLE_Buttons):
    def __init__(self):
        super().__init__()
        self.padno = 0
        self.r, self.g, self.b = (0, 0, 0)

    def changeColour(self, r, g, b):
        self.r, self.g, self.b = (r, g, b)

    def rgbLightUp(self, dawCtrl, r, g, b):
        self.changeColour(r, g, b)
        self.lightUp(dawCtrl)

    def lightUp(self, dawCtrl):
        dawCtrl.send_message(HEADER + PAD_LIGHT_HEADER + (self.padno + 0x6F, int(self.r/255 * 31), int(self.g/255 * 31), int(self.b/255 * 31)) + FOOTER)
    
    def lightDown(self, dawCtrl):
        dawCtrl.send_message(HEADER + PAD_LIGHT_HEADER + (self.padno + 0x6F, 0, 0, 0) + FOOTER)

class KLE_Fader(KLE_Control):
    def __init__(self):
        super().__init__()
        self.name = "Unassigned"

class KLE_Knob(KLE_Control):
    def __init__(self):
        super().__init__()
        self.name = "Unassigned"

class KLE_Controls:
    def __init__(self):
        self.buttons: Dict[str, KLE_Button] = {}
        self.faders: List[KLE_Fader] = []
        self.knobs: List[KLE_Knob] = []
        self.pads: List[KLE_Pad] = []
    def __getstate__(self):
        return self.__dict__.copy()
    def __setstate__(self, dict):
        self.__dict__.update(dict)
