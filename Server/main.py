from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json

class PongProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        if datagram[:4] == "PING":
            print "received %r from %s:%d, sending pong" % (datagram, host, port)
            self.transport.write("PONG",(host, port))
        else:
            print "received %r from %s:%d" % (datagram, host, port)


from twisted.internet.protocol import ServerFactory, Protocol

class ServerProtocol(Protocol):
    datatrans=None

    def sendData(self, msg):
        if (self.transport):
             self.transport.write(msg)
             print('Data sent {}'.format(msg))
        else:
             print('No Connection Established yet!')

    def dataReceived(self, data):
        print('Data received {}'.format(data))
        self.datatrans.decode(data)

    def connectionMade(self):
        self.datatrans=dataTransformer(self)
        print('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        print('Lost connection because {}'.format(reason))

class ServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServerProtocol()

class dataTransformer():
    server=None
    def __init__(self, _server):
        self.server=_server

    def decode(self, data):
        request=json.loads(data)
        if request['cmd']=='list_controllers':
            self.list_controllers()

    def list_controllers(self):
        msg=json.dumps({'cmd':'controllers_list','ids':['ABCDEF','GHIJKL']})
        self.server.sendData(msg)

if __name__=='__main__':
    reactor.listenUDP(9999,PongProtocol())
    reactor.listenTCP(9999, ServerFactory())
    reactor.run()
