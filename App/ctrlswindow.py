from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
Builder.load_file("ctrlswindow.kv")
class ctrlBtn(Button):
    pass

class ctrlsWindow(FloatLayout):
    pass

from twisted.internet.protocol import DatagramProtocol
class ctrlsFinder(DatagramProtocol):
    ctrlswindow=None
    scrman=None

    def __init__(self, _window, _scrman):
         self.scrman = _scrman
         self.ctrlswindow = _window

    def startProtocol(self):
         self.transport.setBroadcastAllowed(True)

    def sendPing(self, *args):
         self.ctrlswindow.iplbl.text=self.scrman.hostIP
         pingMsg = "PING:"
         self.transport.write(pingMsg,('255.255.255.255',9999))
         self.ctrlswindow.ctrlsContainer.clear_widgets()

    def datagramReceived(self, data, (host, port)):
         btn=ctrlBtn(text=host)
         btn.bind(on_press=self.nextscreen)
         if data[:4] == "PONG":
             self.ctrlswindow.ctrlsContainer.add_widget(btn)

    def nextscreen(self, args):
        self.transport.loseConnection()
        self.scrman.current="controlwindow"
