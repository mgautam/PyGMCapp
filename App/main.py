#Android app for controlling PSI Goniometers
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor
from pingwindow import Pinger, pingWindow

class ScreenMan(ScreenManager):
    pass

class PyPSIApp(App):
    screenmanager = None
    pinger = None
    pingwindow = None

    def build(self):
        self.screenmanager = ScreenMan()

        self.pingwindow = pingWindow()
        self.pinger = Pinger(self.pingwindow, self.screenmanager)
        self.pingwindow.button.bind(on_press=self.pinger.sendPing)
        reactor.listenUDP(0,self.pinger)

        self.screenmanager.get_screen("findhostswindow").add_widget(self.pingwindow)
        return self.screenmanager

if __name__ == '__main__':
    PyPSIApp().run()
