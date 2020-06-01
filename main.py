from ms_interface.ms_interface import MainStageConcert, MainStageSink
from kle_lib.kle import KLE
import asyncio
import threading
import rtmidi
import time
import sys

kle = KLE()

ms_out = rtmidi.MidiOut()
ms_out.open_virtual_port(name="KLE MS")

ms_in = rtmidi.MidiIn()
ms_in.open_virtual_port(name="KLE MS")

concert = MainStageConcert(sys.argv[1], kle)
sink = MainStageSink(concert)

for i in range(8):
    if i<4:
        if (i)/2 == int((i)/2):
            kle.controls.pads[i].rgbLightUp(kle._dawout, 255,0,0)
        else:
            kle.controls.pads[i].rgbLightUp(kle._dawout, 0, 255, 0)
    else:
        if (i)/2 == int((i)/2):
            kle.controls.pads[i].rgbLightUp(kle._dawout, 0, 255, 0)
        else:
            kle.controls.pads[i].rgbLightUp(kle._dawout, 255, 0, 0)


t = threading.Thread(target=sink.activateLoop, args=(asyncio.get_event_loop(),))
t.start()

knobs = [16, 17, 18, 19, 20, 21, 22, 23, 24]
faders = [0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8]
faderout = [73, 75, 79, 72, 80, 81, 82, 83, 85]

print("Ready")

fadermsgdecay = 0
fadermsgno = 0

while True:
    if fadermsgdecay > 0:
        fadermsgdecay -= 1
    if fadermsgdecay == 1:
        time.sleep(.001)
        fader = kle.controls.faders[fadermsgno]
        percent = round((fader.value)/127 * 100, 2)
        kle.updateText(fader.name, str(percent) + "%")
    msg = kle.getMidiMessage()
    if msg != None:
        ms_out.send_message(msg[0])
    msg = kle.getDawMessage()
    if msg != None:
        if msg[0][1] in knobs:
            knob = kle.controls.knobs[knobs.index(msg[0][1])]
            print("mod: " + str(msg[0][2]))
            if msg[0][2] > 64:
                knob.value -= msg[0][2] - 64
                if knob.value < 0:
                    knob.value = 0
            else:
                knob.value += msg[0][2]
                if knob.value > 127:
                    knob.value = 127
            print(knob.value)
            ms_out.send_message([msg[0][0], msg[0][1], knob.value])
            percent = round((knob.value)/127 * 100, 2)
            kle.updateText(knob.name, str(percent) + "%")
        if msg[0][0] in faders:
            fader = kle.controls.faders[faders.index(msg[0][0])]
            ms_out.send_message([0xB0, faderout[faders.index(msg[0][0])], msg[0][2]])
            percent = round((msg[0][2])/127 * 100, 2)
            kle.updateText(fader.name, str(percent) + "%")
            fader.value = msg[0][2]
            fadermsgdecay = 80000
            fadermsgno = faders.index(msg[0][0])
    msg = ms_in.get_message() 
    if msg != None:
        #print(msg)
        if msg[0][1] in knobs:
            knob = kle.controls.knobs[knobs.index(msg[0][1])]
            #print(knob.value)
            if knob.value != msg[0][2]:
                percent = round((msg[0][2])/127 * 100, 2)
                kle.updateText(knob.name, str(percent) + "%")
                knob.value = msg[0][2]
            
        if msg[0][1] in faderout:
            fader = kle.controls.faders[faderout.index(msg[0][1])]
            if fader.value != msg[0][2]:
                percent = round((msg[0][2])/127 * 100, 2)
                kle.updateText(fader.name, str(percent) + "%")
                fader.value = msg[0][2]
