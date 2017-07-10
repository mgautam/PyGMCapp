from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("controlwindow.kv")

class controlWindow(FloatLayout):
    dataman=None
    uiman=None

    #gcpos=0
    #def __init__(self, _dataman, _uiman):
    #    self.dataman=_dataman
    #    self.uiman=_uiman

    def moveforward(self,*args):
        self.dataman.updateLastCMD("move forward")
        #gcpos=gcpos+40960
        self.dataman.motioncmd("409600")#str(gcpos))

    def movereverse(self,*args):
        self.dataman.updateLastCMD("move reverse")
        #gcpos=gcpos-40960
        self.dataman.motioncmd("-409600")#str(gcpos))

