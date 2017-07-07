#Android app for controlling PSI Goniometers

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from kivy.lang import Builder
Builder.load_file("pingwindow.kv")

class Pinger(DatagramProtocol):
    pingwindow=None

    def __init__(self, _window):
        self.pingwindow = _window

    def startProtocol(self):
        self.transport.setBroadcastAllowed(True)

    def sendPing(self, *args):
        pingMsg = "PING:"
        self.transport.write(pingMsg,('255.255.255.255',9999))#('192.168.1.255',9999))
        #('<broadcast>',9999))
        self.pingwindow.hostsContainer.clear_widgets()

    def datagramReceived(self, data, (host, port)):
        msg = "%s" % host
        if data[:4] == "PONG":
            self.pingwindow.hostsContainer.add_widget(Button(text=msg))

class pingWindow(BoxLayout):
    pass

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
