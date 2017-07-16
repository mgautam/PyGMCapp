from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
import time
import threading

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
             print('{}: Data sent {}'.format(time.time(), msg))
        else:
             print('No Connection Established yet!')

    def dataReceived(self, data):
        print('{}: Data received {}'.format(time.time(), data))
        self.datatrans.decode(data)

    def connectionMade(self):
        self.datatrans=dataTransformer(self)
        print('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        print('Lost connection because {}'.format(reason))

class ServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServerProtocol()

import os, errno
class dataTransformer():
    server=None
    rdpipe='/tmp/cppipe'
    wrpipe='/tmp/pcpipe'

    def __init__(self, _server):
        self.server=_server
        try:
            os.mkfifo(self.rdpipe)
            os.mkfifo(self.wrpipe)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                print('cannot initialize named pipe')
                raise

    def decode(self, data):
        try:
            request=json.loads(data)
        except ValueError, err:
            print("DataTranformer failure: Invalid data format.")
            return
        if request['cmd']=='list_controllers':
            self.list_controllers()
        elif request['cmd']=='motion_cmd':
            self.motion_command(request['ctrlid'],request['gccmd'])
        elif request['cmd']=='send_status':
            self.requestgc_status(request['ctrlid'])
            readThread=threading.Thread(target=self.send_status_toApp,args=(request['ctrlid'],))
            readThread.daemon=True
            readThread.start()

    def list_controllers(self):
        msg=json.dumps({'cmd':'controllers_list','ids':['ABCDEF','GHIJKL']})
        self.server.sendData(msg)

    def requestgc_status(self, ctrlid):
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write("send_status")
            cmdbuf.close()

    def send_status_toApp(self, ctrlid):
        with open(self.rdpipe,"r") as responsebuf:
            while True:
                data=responsebuf.readline().strip()
                if len(data)!=0:
                    msg=json.dumps({'cmd':'status_send','ctrlid':ctrlid,'status':data})
                    self.server.sendData(msg)
                else:
                    break

    def motion_command(self, ctrlid, cmd):
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write(cmd)
            cmdbuf.close()

if __name__=='__main__':
    reactor.listenUDP(9999,PongProtocol())
    reactor.listenTCP(9999, ServerFactory())
    reactor.run()
