from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
import time
import threading
import logging
import sys

class PongProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        if datagram[:4] == "PING":
            logger.info("received %r from %s:%d, sending pong" % (datagram, host, port))
            self.transport.write("PONG",(host, port))
        else:
            logger.info("received %r from %s:%d" % (datagram, host, port))


from twisted.internet.protocol import ServerFactory, Protocol

class ServerProtocol(Protocol):
    datatrans=None

    def sendData(self, msg):
        if (self.transport):
             self.transport.write(msg)
             logger.info('{}: Data sent {}'.format(time.time(), msg))
        else:
             logger.warning('No Connection Established yet!')

    def dataReceived(self, data):
        logger.info('{}: Data received {}'.format(time.time(), data))
        self.datatrans.decode(data)

    def connectionMade(self):
        self.datatrans=dataTransformer(self)
        logger.debug('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        logger.info('Lost connection because {}'.format(reason))

class ServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServerProtocol()

import os, errno

def funcwrap(func, *args):
    func(*args)

class dataTransformer():
    server=None
    rdpipe='/tmp/GMCcppipe'
    wrpipe='/tmp/GMCpcpipe'
    handle=0

    def __init__(self, _server):
        self.server=_server
        try:
            os.mkfifo(self.rdpipe)
            os.mkfifo(self.wrpipe)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                logger.error('cannot initialize named pipe')
                raise
        self.handle=0

    def next_handle(self):
        self.handle+=1
        return self.handle

    def decode(self, data):
        try:
            request=json.loads(data)
        except ValueError, err:
            logger.warning("DataTranformer failure: Invalid data format.")
            return
        operation=request.get('cmd')
        op_list=['list_controllers','send_status','motion_cmd']
        if not (operation in op_list):
            self.logger.error('operation does not exist: %r',operation)
            return
        try:
            target = getattr(self,operation)
        except (AttributeError, TypeError):
            self.logger.error('operation is not defined: %r',operation)
            return
        ctrlid=request.get('ctrlid')
        params=request.get('params')
        target(ctrlid,params)

    def list_controllers(self, ctrlid, params):
        msg=json.dumps({'cmd':'controllers_list','ids':['ABCDEF','GHIJKL']})
        self.server.sendData(msg)

    def request_galil_status(self, ctrlid, params):
        datalist=[ctrlid,'send_status']
        datalist.extend(params)
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write(json.dumps(datalist))
            cmdbuf.close()

    def forward_galil_status(self, ctrlid, params):
        with open(self.rdpipe,"r") as responsebuf:
            while True:
                data=responsebuf.readline().strip()
                if len(data)!=0:
                    msg=json.dumps({'cmd':'status_send','ctrlid':ctrlid,'status':data})
                    self.server.sendData(msg)
                else:
                    break

    def send_status(self, ctrlid, params):
        readThread=threading.Thread(target=self.forward_galil_status,args=(ctrlid, params,))
        readThread.daemon=True
        readThread.start()
        self.request_galil_status(ctrlid, params)

    def motion_cmd(self, ctrlid, params):
        datalist=[ctrlid,'motion_cmd']
        try:
            motion=json.loads(params)
        except ValueError, err:
            logger.warning("Motion failure: Invalid motion format.")
            return
        datalist.append(motion["type"])
        datalist.append(motion['distance'])
        with open(self.wrpipe,"w") as cmdbuf:
            cmdbuf.write(json.dumps(datalist))
            cmdbuf.close()

if __name__=='__main__':
    logging.basicConfig(filename='/tmp/gmc_gateway.log',level=logging.DEBUG)
    logger=logging.getLogger('gmc_logger')

    std_hdlr=logging.StreamHandler(sys.stdout)
    std_hdlr.setLevel(logging.DEBUG)
    logger.addHandler(std_hdlr)

    reactor.listenUDP(9999,PongProtocol())
    reactor.listenTCP(9999, ServerFactory())
    reactor.run()
