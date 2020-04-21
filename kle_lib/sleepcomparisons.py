import time
import rtmidi

mo = rtmidi.MidiOut()
mo.open_port(3)
def domath():
    res = 1333 * 14123
    res *= 134165
    mo.send_message([0x90, 0x1, 127])
    return res

def test(ticks=10):
    history = []
    offset = 0
    for i in range(ticks):
        history.append(time.time())
        time.sleep(1 - offset)
        stime = time.time()
        domath()
        offset = time.time() - stime
    for i in range(len(history)):
        print("Pass " + str(i) + ": " + str(history[i]))

def test2(ticks=10):
    history = []
    stime = time.time()
    history.append(stime)
    for i in range(ticks):
        etime = stime + 1
        domath()
        while time.time() < etime:
            pass
        stime = etime
        history.append(time.time())
    for i in range(len(history)):
        print("Pass " + str(i) + ": " + str(history[i]))
