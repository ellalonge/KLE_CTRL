import rtmidi
import binascii
import time
import pickle
import kle_lib.buttondefs
from kle_lib.buttons import KLE_Controls, KLE_Button, KLE_Pad, KLE_Knob, KLE_Fader
from typing import List, Dict

HEADER = (0xF0, 0x0, 0x20, 0x6B, 0x7F, 0x42)
LCD_TEXT_HEADER = (0x4, 0x0, 0x60, 0x01)
LCD_TEXT_NEWLINE = (0x0, 0x2)
PAD_LIGHT_HEADER = (0x2, 0x0, 0x16)
BTN_LIGHT_HEADER = (0x2, 0x0, 0x10)
FOOTER = (0xF7,)

def text2sysex(line1, line2): #Convert text 2 hex
    ol1 = ()
    ol2 = ()
    for letter in line1:
        ol1 += (ord(letter),)
    for letter in line2:
        ol2 += (ord(letter),)
    return ol1 + LCD_TEXT_NEWLINE + ol2 + (0x0,)

class KLE:
    def __init__(self, controller_out='Arturia KeyLab Essential 61 DAW Out', controller_in='Arturia KeyLab Essential 61 DAW In', midi_in='Arturia KeyLab Essential 61 MIDI In'):
        self._dawin = rtmidi.MidiIn()
        self._dawin.open_port(self._dawin.get_ports().index(controller_in))
        self._midiin = rtmidi.MidiIn()
        self._midiin.open_port(self._midiin.get_ports().index(midi_in))
        self._dawout = rtmidi.MidiOut()
        self._dawout.open_port(self._dawout.get_ports().index(controller_out))
        self._dawout.send_message((240, 0, 32, 107, 127, 66, 2, 0, 64, 17, 127, 0, 247)) #Pose as Live
        #self.controls = pickle.load(open("kle_lib/controlcache.p", 'rb'))
        self.controls = kle_lib.buttondefs.getControls()
    
    def updateText(self, line1, line2):
        #print(HEADER + text2sysex(line1, line2) + FOOTER)
        self._dawout.send_message(
            HEADER + LCD_TEXT_HEADER + text2sysex(line1, line2) + FOOTER
        )
    
    def vegasPad(self, padno, t=100, speed=50):
        r, g, b = (31, 0, 0)
        for i in range(0, t):
            if(r > 0 and b == 0):
                r-=1
                g+=1
            if(g > 0 and r == 0):
                g-=1
                b+=1
            if(b > 0 and g == 0):
                r+=1
                b-=1
            self.controls.pads[padno].rgbLightUp(self._dawout, r, g, b)
            time.sleep(speed/100)

    def vegasPadAll(self, t=100, speed=50):
        r, g, b = (31, 0, 0)
        for i in range(0, t):
            if(r > 0 and b == 0):
                r-=1
                g+=1
            if(g > 0 and r == 0):
                g-=1
                b+=1
            if(b > 0 and g == 0):
                r+=1
                b-=1
            for j in range(1, 9):
                self.controls.pads[j].rgbLightUp(self._dawout, r, g, b)
            time.sleep(speed/100)

    def vegasPadAll2(self, t=100, speed=50):
        rgb = [(),(),(),(),(),(),(),()]
        for i in range(8):
            rgb[i] = [31-(i), 0, 0]
        for j in range(0, t):
            for i in range(1, 9):
                if(rgb[i-1][0] > 0 and rgb[i-1][2] == 0):
                    rgb[i-1][0]-=1
                    rgb[i-1][1]+=1
                if(rgb[i-1][1] > 0 and rgb[i-1][0] == 0):
                    rgb[i-1][1]-=1
                    rgb[i-1][2]+=1
                if(rgb[i-1][2] > 0 and rgb[i-1][1] == 0):
                    rgb[i-1][0]+=1
                    rgb[i-1][2]-=1
            
                self.controls.pads[i].rgbLightUp(self._dawout, tuple(rgb[i-1]))
            time.sleep(speed/100)

    def close(self):
        self._dawout.send_message((240, 0, 32, 107, 127, 66, 2, 0, 64, 17, 0, 0, 247)) #Remove Live Preset
    
    def getDawMessage(self):
        return self._dawin.get_message()
    
    def getMidiMessage(self):
        return self._midiin.get_message()