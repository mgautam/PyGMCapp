from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
Builder.load_file("ctrlswindow.kv")
class ctrlBtn(Button):
    pass

class ctrlsWindow(FloatLayout):
    pass

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory,Protocol

class tcpHighway(Protocol):
    def connectionMade(self):
        data = 'Hello, Server!'
        self.transport.write(data.encode())
        self.factory.logmsg('Data sent {}'.format(data))

    def dataReceived(self, data):
        self.factory.logmsg('Data received {}'.format(data))

    def connectionLost(self, reason):
        self.factory.logmsg('Lost connection because {}'.format(reason))

    def nextscreen(self, args):
        self.transport.loseConnection()
        self.scrman.current="controlwindow"


class tcpHighwayFactory(ClientFactory):
    scrman=None
    ctrlswindow=None
    selectedCtrl=None

    def __init__(self, _window, _scrman):
        self.scrman=_scrman
        self.ctrlswindow=_window

    def startedConnecting(self, connector):
        self.logmsg('Started to connect.')

    def buildProtocol(self, addr):
        self.logmsg('Connected.')
        proto=tcpHighway()
        proto.factory=self
        return proto

    def clientConnectionLost(self, connector, reason):
        self.logmsg('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        self.logmsg('Lost failed. Reason: {}'.format(reason))

    def logmsg(self, msg):
        self.ctrlswindow.statuslbl.text=msg


class tcpDataProcessor():
    factory=None

    def __init__(self, _factory):
        self.factory=_factory

    def startReactor(self, args):
        #self.factory.ctrlswindow.statuslbl.text=self.factory.scrman.selectedHostIP
        reactor.connectTCP(self.factory.scrman.selectedHostIP,9999,self.factory)
