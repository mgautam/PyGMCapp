#Android app for controlling PSI Goniometers
from twisted.internet import reactor
from networks import RadarScanner, dataHighwayFactory

class DataManager():
    radarbeacon=None
    datahighway=None
    selectedServerIP=None
    selectedCtrlID=None

    uiman=None

    firstUDPCall=True

    def __init__(self, _uiman):
        self.uiman=_uiman
        self.radarbeacon=RadarScanner(self)
        self.datahighway=dataHighwayFactory(self)
        #self.firstUDPCall=True

    def findhosts(self, *args):
        if(self.firstUDPCall):
            reactor.listenUDP(0,self.radarbeacon)
            self.firstUDPCall=False
        self.radarbeacon.sendRadarSignal(self.uiman.beaconwindow.passwdInput.text)

    def addServer(self, host):
        self.uiman.beaconwindow.addServerBtn(host)

    def selectServer(self, _serverip):
        self.selectedServerIP=_serverip
        if(self.datahighway.protocol.transport):
            self.datahighway.protocol.transport.loseConnection()
        reactor.connectTCP(self.selectedServerIP,9999,self.datahighway)

    def findctrls(self, *args):
        self.datahighway.protocol.sendData("hello")

    def updateStatus(self, msg):
        self.uiman.serverwindow.statuslbl.text=msg

    def addController(self, ctrlr):
        self.uiman.serverwindow.addCntrllrBtn(ctrlr)

    def selectController(self, _ctrlid):
        self.selectedCtrlID=_ctrlid
