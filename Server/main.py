from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class PongProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        if datagram[:4] == "PING":
            print "received %r from %s:%d, sending pong" % (datagram, host, port)
            self.transport.write("PONG",(host, port))
        else:
            print "received %r from %s:%d" % (datagram, host, port)

reactor.listenUDP(9999,PongProtocol())
reactor.run()
