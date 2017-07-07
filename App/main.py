#Android app for controlling PSI Goniometers
from kivy.app import App
from pingwindow import Pinger, pingWindow

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor

class PyPSIApp(App):
    pinger = None
    pingwindow = None

    def build(self):
        self.pingwindow = pingWindow()
        self.pinger = Pinger(self.pingwindow)
        self.pingwindow.button.bind(on_press=self.pinger.sendPing)
        reactor.listenUDP(0,self.pinger)
        return self.pingwindow

if __name__ == '__main__':
    PyPSIApp().run()
