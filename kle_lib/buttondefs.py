from kle_lib.buttons import KLE_Controls, KLE_Button, KLE_Pad, KLE_Knob, KLE_Fader
from typing import List, Dict
import pickle
#
#   KeyLab Essential 61 Defintions
#

class KLE_Controls_List:
    def __init__(self):
        self.buttons: List[KLE_Button] = []
        self.faders: List[KLE_Fader] = []
        self.knobs: List[KLE_Knob] = []
        self.pads: List[KLE_Pad] = []
    def __getstate__(self):
        return self.__dict__.copy()
    def __setstate__(self, dict):
        self.__dict__.update(dict)  
    def convert2dict(self):
        res = KLE_Controls()
        for button in self.buttons:
            print(button)
            res.buttons[button.name] = button
        res.faders = self.faders
        res.knobs = self.knobs
        res.pads = self.pads
        return res

def getControls():
    controls = KLE_Controls_List()
    for i in range(8):
        pad = KLE_Pad()
        pad.padno = i+1
        controls.pads.append(pad)

    for i in range(9):
        knob = KLE_Knob()
        controls.knobs.append(knob)

    for i in range(9):
        fader = KLE_Fader()
        controls.faders.append(fader)

    DAW_Play = KLE_Button()
    DAW_Play.name = "DAW_Play"
    DAW_Play.inDawCode = DAW_Play.lightCode = 0x5E
    controls.buttons.append(DAW_Play)

    DAW_Stop = KLE_Button()
    DAW_Stop.name = "DAW_Stop"
    DAW_Stop.inDawCode = DAW_Stop.lightCode = 0x5D
    controls.buttons.append(DAW_Stop)

    DAW_Record = KLE_Button()
    DAW_Record.name = "DAW_Record"
    DAW_Record.inDawCode = DAW_Record.lightCode = 0x5F
    controls.buttons.append(DAW_Record)

    DAW_Loop = KLE_Button()
    DAW_Loop.name = "DAW_Loop"
    DAW_Loop.inDawCode = DAW_Loop.lightCode = 0x56
    controls.buttons.append(DAW_Loop)

    DAW_Prev = KLE_Button()
    DAW_Prev.name = "DAW_Prev"
    DAW_Prev.inDawCode = DAW_Prev.lightCode = 0x5B
    controls.buttons.append(DAW_Prev)

    DAW_FFW = KLE_Button()
    DAW_FFW.name = "DAW_FFW"
    DAW_FFW.inDawCode = DAW_FFW.lightCode = 0x5C
    controls.buttons.append(DAW_FFW)

    DAW_Save = KLE_Button()
    DAW_Save.name = "DAW_Save"
    DAW_Save.inDawCode = DAW_Save.lightCode = 0x50
    controls.buttons.append(DAW_Save)

    DAW_Undo = KLE_Button()
    DAW_Undo.name = "DAW_Undo"
    DAW_Undo.inDawCode = DAW_Undo.lightCode = 0x51
    controls.buttons.append(DAW_Undo)

    DAW_Punch = KLE_Button()
    DAW_Punch.name = "DAW_Punch"
    DAW_Punch.inDawCode = DAW_Punch.lightCode = 0x57
    controls.buttons.append(DAW_Punch)

    DAW_Metro = KLE_Button()
    DAW_Metro.name = "DAW_Metro"
    DAW_Metro.inDawCode = DAW_Metro.lightCode = 0x59
    controls.buttons.append(DAW_Metro)

    CTRL_Left = KLE_Button()
    CTRL_Left.name = "CTRL_Left"
    CTRL_Left.inDawCode = CTRL_Left.lightCode = 0x62
    controls.buttons.append(CTRL_Left)

    CTRL_Right = KLE_Button()
    CTRL_Right.name = "CTRL_Right"
    CTRL_Right.inDawCode = CTRL_Right.lightCode = 0x63
    controls.buttons.append(CTRL_Right)

    CTRL_Char = KLE_Button()
    CTRL_Char.name = "CTRL_Char"
    CTRL_Char.inDawCode = 0x65
    CTRL_Char.lightCode = 0x16
    CTRL_Char.se = True
    controls.buttons.append(CTRL_Char)

    CTRL_Preset = KLE_Button()
    CTRL_Preset.name = "CTRL_Preset"
    CTRL_Preset.inDawCode = 0x64
    CTRL_Preset.lightCode = 0x17
    CTRL_Preset.se = True
    controls.buttons.append(CTRL_Preset)

    CTRL_Prev = KLE_Button()
    CTRL_Prev.name = "CTRL_Prev"
    CTRL_Prev.inDawCode = 0x30
    CTRL_Prev.lightCode = 0x1B
    CTRL_Prev.se = True
    controls.buttons.append(CTRL_Prev)

    CTRL_Next = KLE_Button()
    CTRL_Next.name = "CTRL_Next"
    CTRL_Next.inDawCode = 0x31
    CTRL_Next.lightCode = 0x1A
    CTRL_Next.se = True
    controls.buttons.append(CTRL_Next)

    CTRL_Bank = KLE_Button()
    CTRL_Bank.name = "CTRL_Bank"
    CTRL_Bank.inDawCode = -0x2
    CTRL_Bank.lightCode = 0x1C
    CTRL_Bank.se = True
    controls.buttons.append(CTRL_Bank)
    print(controls.knobs)
    return controls.convert2dict()