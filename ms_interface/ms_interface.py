from typing import Dict, List, Any
import rtmidi
import plistlib
import asyncio
from kle_lib.kle import KLE

class MainStageConcert:
    def __init__(self, fileloc: str, kle: KLE):
        self.kle = kle
        self.loc: str = fileloc + "/Concert.patch/"
        self.data = plistlib.readPlist(self.loc + "data.plist")
        self.banks = self.findBanks()
        self.currentPatch: List[int] = [0,0]
    
    def findBanks(self):
        res: List[MainStagePatchBank] = []
        for bank in self.data["nodes"]:
            res.append(MainStagePatchBank(self, bank))
        return res
    
    def changePatches(self, program=None, bank=None):
        if program != None:
            self.currentPatch[1] = int(program)
        if bank != None:
            self.currentPatch[0] = int(bank)

        #print(self.currentPatch)
        try:
            bankText = self.banks[self.currentPatch[0]].name[:-6][:16]
            programText = self.banks[self.currentPatch[0]].programs[self.currentPatch[1]].name[:-6][:16]
            self.kle.updateText(bankText, programText)
            knobs = self.banks[self.currentPatch[0]].programs[self.currentPatch[1]].controls.knobs
            faders = self.banks[self.currentPatch[0]].programs[self.currentPatch[1]].controls.faders
            print("UPDATING KNOBS")
            for i in range(len(knobs)):
                print(knobs[i].name)
                self.kle.controls.knobs[i].name = knobs[i].name
            print("UPDATING FADERS")
            for i in range(len(faders)):
                print(faders[i].name)
                self.kle.controls.faders[i].name = faders[i].name
        except Exception:
            pass
    def getCurrentPatch(self):
        return self.banks[self.currentPatch[0]].programs[self.currentPatch[1]]

class MainStageSink:
    def __init__(self, concert: MainStageConcert):
        self.mi = rtmidi.MidiIn()
        self.mi.open_virtual_port("ms_sink")
        self.mo = rtmidi.MidiOut()
        self.mo.open_virtual_port("ms_sink")
        self.concert = concert

    async def startLoop(self):
        while True:
            msg = self.mi.get_message()
            if msg != None:
                #print(msg)
                if msg[0][1] == 0x15:
                    self.concert.changePatches(program=msg[0][2])
                if msg[0][1] == 0x16:
                    self.concert.changePatches(bank=(msg[0][2]/2))

    def activateLoop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.startLoop()) 

class MainStagePatchBank:
    def __init__(self, concert: MainStageConcert, name: str):
        self.name = name
        self.concert = concert
        self.loc: str = concert.loc + name + "/"
        self.data = plistlib.readPlist(self.loc + "data.plist")
        self.programs = self.findPrograms()
    
    def findPrograms(self):
        res: List[MainStagePatchProgram] = []
        for program in self.data["nodes"]:
            res.append(MainStagePatchProgram(self.concert, self, program))
        return res

class MainStagePatchProgram:
    def __init__(self, concert: MainStageConcert, bank: MainStagePatchBank, name: str):
        self.name = name
        self.concert = concert
        self.bank = bank
        self.loc: str = bank.loc + name + "/"
        self.data = plistlib.readPlist(self.loc + "data.plist")
        self.controls = MainStagePatchControls(self)

class MainStagePatchControl:
    name = ""
    data: Dict[str, Any] = {}

class MainStagePatchControlFader(MainStagePatchControl):
    pass

class MainStagePatchControlKnob(MainStagePatchControl):
    val = 0

class MainStagePatchControls:
    faders: List[MainStagePatchControlFader] = []
    knobs: List[MainStagePatchControlKnob] = []
    def __init__(self, patch: MainStagePatchProgram):
        self.concert = patch.concert
        self.bank = patch.bank
        self.program = patch
        self.data = patch.data["patch"]["engineNode"]["uiPluginDataDict"]
        self.faders = self.populateFaders()
        self.knobs = self.populateKnobs()

    def populateFaders(self):
        res: List[MainStagePatchControlFader] = []
        for i in range(9):
            try:
                faderdata = self.data["\x01IDENTITY:Fader " + str(i+1)]
                fader = MainStagePatchControlFader()
                fader.data = faderdata
                fader.name = faderdata["storeDict"]["customLabel"]
                res.append(fader)
            except KeyError:
                fader = MainStagePatchControlFader()
                fader.data = {}
                fader.name = "Unassigned (E)"
                res.append(fader)
        return res

    def populateKnobs(self):
        res: List[MainStagePatchControlKnob] = []
        for i in range(9):
            try:
                knobdata = self.data["\x01IDENTITY:Knob " + str(i+1)]
                knob = MainStagePatchControlKnob()
                knob.data = knobdata
                knob.name = knobdata["storeDict"]["customLabel"]
                res.append(knob)
            except KeyError:
                knob = MainStagePatchControlKnob()
                knob.data = {}
                knob.name = "Unassigned"
                res.append(knob)
        return res
            