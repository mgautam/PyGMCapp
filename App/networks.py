from twisted.internet.protocol import DatagramProtocol

class RadarScanner(DatagramProtocol):
    dataman=None

    def __init__(self, _dataman):
        self.dataman = _dataman

    def startProtocol(self):
        self.transport.setBroadcastAllowed(True)

    def sendRadarSignal(self, *args):
        password = args[0];#self.hostswindow.passwdInput.text
        self.transport.write(password,('255.255.255.255',9999))
        self.dataman.uiman.beaconwindow.clearServersList()

    def datagramReceived(self, data, (host, port)):
        if data[:4]=="PONG":
            self.dataman.addServer(host)

from twisted.internet.protocol import ClientFactory,Protocol

class dataHighway(Protocol):
   def connectionMade(self):
        data = 'Hello, Server!'
        self.transport.write(data.encode())
        self.factory.logmsg('Data sent {}'.format(data))

   def dataReceived(self, data):
        self.factory.logmsg('Data received {}'.format(data))

   def connectionLost(self, reason):
        self.factory.logmsg('Lost connection because {}'.format(reason))


class dataHighwayFactory(ClientFactory):
    dataman=None

    def __init__(self, _dataman):
        self.dataman=_dataman

    def startedConnecting(self, connector):
         self.logmsg('Started to connect.')

    def buildProtocol(self, addr):
         self.logmsg('Connected.')
         proto=dataHighway()
         proto.factory=self
         return proto

    def clientConnectionLost(self, connector, reason):
         self.logmsg('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
         self.logmsg('Lost failed. Reason: {}'.format(reason))

    def logmsg(self, msg):
         self.dataman.updateStatus(msg)
