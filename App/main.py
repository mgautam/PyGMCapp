#Android app for controlling PSI Goniometers

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Pinger(DatagramProtocol):
    def __init__(self, App):
        self.app = App

    def startProtocol(self):
        self.transport.setBroadcastAllowed(True)

    def sendPing(self, *args):
        pingMsg = "PING:"
        self.transport.write(pingMsg,('255.255.255.255',9999))#('192.168.1.255',9999))
        #('<broadcast>',9999))
        self.app.label.text += "{}\n".format(pingMsg)

    def datagramReceived(self, data, (host, port)):
        msg = "received %r from %s:%d" % (data, host, port)
        if data[:4] == "PONG":
            self.app.label.text += "{}\n".format(msg)

class PyPSIApp(App):
    label = None
    button = None
    pinger = None

    def setup_gui(self):
        layout = BoxLayout(orientation='vertical')
        self.button = Button(text='Send Ping Msg')
        self.button.bind(on_press=self.pinger.sendPing)
        self.label = Label(text='connecting...\n')
        layout.add_widget(self.button)
        layout.add_widget(self.label)
        return layout

    def build(self):
        self.pinger = Pinger(self)
        reactor.listenUDP(0,self.pinger)
        return self.setup_gui()

if __name__ == '__main__':
    PyPSIApp().run()
