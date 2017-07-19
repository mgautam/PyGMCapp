from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
import time
import threading
import logging

class PongProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        if datagram[:4] == "PING":
            logging.info("received %r from %s:%d, sending pong" % (datagram, host, port))
            self.transport.write("PONG",(host, port))
        else:
            logging.info("received %r from %s:%d" % (datagram, host, port))


from twisted.internet.protocol import ServerFactory, Protocol

class ServerProtocol(Protocol):
    datatrans=None

    def sendData(self, msg):
        if (self.transport):
             self.transport.write(msg)
             logging.info('{}: Data sent {}'.format(time.time(), msg))
        else:
             logging.warning('No Connection Established yet!')

    def dataReceived(self, data):
        logging.info('{}: Data received {}'.format(time.time(), data))
        self.datatrans.decode(data)

    def connectionMade(self):
        self.datatrans=dataTransformer(self)
        logging.debug('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        logging.info('Lost connection because {}'.format(reason))

class ServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServerProtocol()

import os, errno

def funcwrap(func, *args):
    func(*args)

class dataTransformer():
    server=None
    rdpipe='/tmp/cppipe'
    wrpipe='/tmp/pcpipe'
    handle=0

    def __init__(self, _server):
        self.server=_server
        try:
            os.mkfifo(self.rdpipe)
            os.mkfifo(self.wrpipe)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                logging.error('cannot initialize named pipe')
                raise
        self.handle=0

    def next_handle(self):
        self.handle+=1
        return self.handle

    def decode(self, data):
        try:
            request=json.loads(data)
        except ValueError, err:
            logging.warning("DataTranformer failure: Invalid data format.")
            return
        operation=request.get('cmd')
        try:
            target = getattr(self,operation)
        except (AttributeError, TypeError):
            self.logging.error('operation does not exist: %r',operation)
            return
        if 'ctrlid' in request:
            params=[request['ctrlid']]
        else:
            params=None
        if 'gccmd' in request:
            params.append(request['gccmd'])

        if params==None:
            funcwrap(target)
        else:
            funcwrap(target,params)

    def list_controllers(self):
        msg=json.dumps({'cmd':'controllers_list','ids':['ABCDEF','GHIJKL']})
        self.server.sendData(msg)

    def request_galil_status(self, ctrlid):
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write("send_status")
            cmdbuf.close()

    def forward_galil_status(self, ctrlid):
        with open(self.rdpipe,"r") as responsebuf:
            while True:
                data=responsebuf.readline().strip()
                if len(data)!=0:
                    msg=json.dumps({'cmd':'status_send','ctrlid':ctrlid,'status':data})
                    self.server.sendData(msg)
                else:
                    break

    def send_status(self, ctrlid):
        readThread=threading.Thread(target=self.forward_galil_status,args=(ctrlid,))
        readThread.daemon=True
        readThread.start()
        self.request_galil_status(ctrlid)

    def motion_cmd(self, (ctrlid, cmd)):
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write(cmd)
            cmdbuf.close()

if __name__=='__main__':
    logging.basicConfig(filename='psi_gateway.log',level=logging.DEBUG)
    reactor.listenUDP(9999,PongProtocol())
    reactor.listenTCP(9999, ServerFactory())
    reactor.run()
