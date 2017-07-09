#Android app for controlling PSI Goniometers
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager

from beaconwindow import beaconWindow
from serverwindow import serverWindow

from kivy.lang import Builder
Builder.load_file("scrman.kv")

class ScreenMan(ScreenManager):
    dataman=None

class UIManager():
    dataman=None

    beaconwindow=None
    serverwindow=None
    contrlwindow=None

    screenmanager=None

    def __init__(self, _dataman):
        self.dataman=_dataman

    def buildwindows(self):
        self.beaconwindow = beaconWindow()#self.dataman,self)
        self.beaconwindow.dataman=self.dataman
        self.beaconwindow.uiman=self
        self.beaconwindow.radarbtn.bind(on_press=self.dataman.findhosts)

        self.serverwindow = serverWindow()
        self.serverwindow.dataman=self.dataman
        self.serverwindow.uiman=self
        self.serverwindow.findbtn.bind(on_press=self.dataman.findctrls)

        self.screenmanager = ScreenMan()
        self.screenmanager.dataman=self.dataman
        self.screenmanager.get_screen("beaconwindow").add_widget(self.beaconwindow)
        self.screenmanager.get_screen("serverwindow").add_widget(self.serverwindow)
        return self.screenmanager

    def nextscreen(self, *args):
        self.serverwindow.hostlbl.text=self.dataman.selectedServerIP
        self.screenmanager.current="serverwindow"
