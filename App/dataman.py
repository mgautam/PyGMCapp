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
    firstTCPCall=True

    def __init__(self, _uiman):
        self.uiman=_uiman
        self.datahighway=dataHighwayFactory(self)
        self.radarbeacon=RadarScanner(self)
        #self.firstUDPCall=True
        #self.firstTCPCall=True

    def findhosts(self, *args):
        if(self.firstUDPCall):
            reactor.listenUDP(0,self.radarbeacon)
            self.firstUDPCall=False
        self.radarbeacon.sendRadarSignal(self.uiman.beaconwindow.passwdInput.text)

    def addServer(self, host):
        self.uiman.beaconwindow.addServerBtn(host)

    def setServer(self, btn, touch):
        self.selectedServerIP=btn.text

    def findctrls(self, *args):
        if(self.firstTCPCall):
            reactor.connectTCP(self.selectedServerIP,9999,self.datahighway)
            self.firstTCPCall=False

    def updateStatus(self, msg):
        self.uiman.serverwindow.statuslbl.text=msg
