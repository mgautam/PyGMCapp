from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("hostswindow.kv")
class hostBtn(Button):
    pass

class hostsWindow(FloatLayout):
    pass

from twisted.internet.protocol import DatagramProtocol
class hostsFinder(DatagramProtocol):
    hostswindow=None
    scrman=None
    selectedHost=None

    def __init__(self, _window, _scrman):
         self.scrman = _scrman
         self.hostswindow = _window

    def startProtocol(self):
         self.transport.setBroadcastAllowed(True)

    def sendPing(self, *args):
         pingMsg = self.hostswindow.passwdInput.text
         self.transport.write(pingMsg,('255.255.255.255',9999))
         self.hostswindow.hostsContainer.clear_widgets()

    def datagramReceived(self, data, (host, port)):
         btn=hostBtn(text=host)
         btn.bind(on_touch_down=self.setHostIP)
         btn.bind(on_press=self.nextscreen)
         if data[:4] == "PONG":
             self.hostswindow.hostsContainer.add_widget(btn)

    def setHostIP(self, btn, touch):
        self.selectedHost=btn.text

    def nextscreen(self, args):
        self.transport.loseConnection()
        self.scrman.selectedHostIP=self.selectedHost
        self.scrman.current="findctrlswindow"
