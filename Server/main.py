from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class PongProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        if datagram[:4] == "PING":
            print "received %r from %s:%d, sending pong" % (datagram, host, port)
            self.transport.write("PONG",(host, port))
        else:
            print "received %r from %s:%d" % (datagram, host, port)


from twisted.internet.protocol import ServerFactory, Protocol

class EchoServerProtocol(Protocol):
    def dataReceived(self, data):
        print('Data received {}'.format(data))
        self.transport.write(data)

    def connectionMade(self):
        print('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        print('Lost connection because {}'.format(reason))

class EchoServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return EchoServerProtocol()

reactor.listenUDP(9999,PongProtocol())
reactor.listenTCP(9999, EchoServerFactory())
reactor.run()
