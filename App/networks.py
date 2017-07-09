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
        self.factory.logmsg('Connection Successful.')

    def sendData(self, msg):
        if (self.transport):
            self.transport.write(msg)
            self.factory.logmsg('Data sent {}'.format(msg))
        else:
            self.factory.logmsg('No Connection Established yet!')

    def dataReceived(self, data):
        self.factory.dataman.datatrans.decode(data)

    def connectionLost(self, reason):
        self.factory.logmsg('Lost connection because {}'.format(reason))

class dataHighwayFactory(ClientFactory):
    dataman=None
    protocol=None

    def __init__(self, _dataman):
        self.dataman=_dataman
        self.protocol=dataHighway()
        self.protocol.factory=self
 
    def startedConnecting(self, connector):
         self.logmsg('Started to connect.')

    def buildProtocol(self, addr):
         self.logmsg('Connected.')
         return self.protocol

    def clientConnectionLost(self, connector, reason):
         self.logmsg('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
         self.logmsg('Lost failed. Reason: {}'.format(reason))

    def logmsg(self, msg):
         self.dataman.updateStatus(msg)
