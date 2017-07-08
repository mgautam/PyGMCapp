#Android app for controlling PSI Goniometers
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager

from twisted.internet import reactor
from hostswindow import hostsFinder, hostsWindow
from ctrlswindow import ctrlsFinder, ctrlsWindow

from kivy.lang import Builder
Builder.load_file("scrman.kv")

class ScreenMan(ScreenManager):
    hostIP=None

class ScrManBuilder():
    screenmanager = None
    logicInstance = None
    uiInstance = None

    def buildHostsFinder(self):
        self.uiInstance = hostsWindow()
        self.logicInstance = hostsFinder(self.uiInstance, self.screenmanager)
        self.uiInstance.button.bind(on_press=self.logicInstance.sendPing)
        reactor.listenUDP(0,self.logicInstance)
        return self.uiInstance

    def buildCtrlsFinder(self):
        self.uiInstance = ctrlsWindow()
        self.logicInstance = ctrlsFinder(self.uiInstance, self.screenmanager)
        self.uiInstance.button.bind(on_press=self.logicInstance.sendPing)
        reactor.listenUDP(0,self.logicInstance)
        return self.uiInstance


    def buildScrMan(self):
        self.screenmanager = ScreenMan()
        self.screenmanager.get_screen("findhostswindow").add_widget(self.buildHostsFinder())
        #self.screenmanager.get_screen("findctrlswindow").on_enter()
        self.screenmanager.get_screen("findctrlswindow").add_widget(self.buildCtrlsFinder())
        return self.screenmanager

