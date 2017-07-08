from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
Builder.load_file("ctrlswindow.kv")
class ctrlsWindow(BoxLayout):
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
         pingMsg = "PING:"
         self.transport.write(pingMsg,('255.255.255.255',9999))
         self.ctrlswindow.ctrlsContainer.clear_widgets()

    def datagramReceived(self, data, (host, port)):
         btn=Button(text=host)
         btn.bind(on_press=self.nextscreen)
         if data[:4] == "PONG":
             self.ctrlswindow.ctrlsContainer.add_widget(btn)

    def nextscreen(self, args):
        self.transport.loseConnection()
        self.scrman.current="controlwindow"
