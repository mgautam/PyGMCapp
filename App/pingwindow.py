from twisted.internet.protocol import DatagramProtocol
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
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
         self.transport.write(pingMsg,('255.255.255.255',9999))
         self.pingwindow.hostsContainer.clear_widgets()

    def datagramReceived(self, data, (host, port)):
         msg = "%s" % host
         if data[:4] == "PONG":
             self.pingwindow.hostsContainer.add_widget(Button(text=msg))

class pingWindow(BoxLayout):
    pass
