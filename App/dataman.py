#Android app for controlling PSI Goniometers
import json
from twisted.internet import reactor
from networks import RadarScanner, dataHighwayFactory

class DataManager():
    radarbeacon=None
    datahighway=None
    selectedServerIP=None
    selectedCtrlID=None

    uiman=None

    firstUDPCall=True
    datatrans=None

    def __init__(self, _uiman):
        self.uiman=_uiman
        self.radarbeacon=RadarScanner(self)
        self.datahighway=dataHighwayFactory(self)
        #self.firstUDPCall=True
        self.datatrans=dataTransformer(self.datahighway,self)

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
        self.datatrans.findctrls()

    def updateStatus(self, msg):
        if self.uiman.screenmanager.current=="serverwindow":
            self.uiman.serverwindow.statuslbl.text="Status: "+msg
        else:
        #if self.uiman.screenmanager.current=="controlwindow":
            self.uiman.controlwindow.statuslbl.text="Status: "+msg

    def addController(self, ctrlr):
        self.uiman.serverwindow.addCntrllrBtn(ctrlr)

    def selectController(self, _ctrlid):
        self.selectedCtrlID=_ctrlid
        reactor.callLater(1, self.datatrans.requeststs)

    def updateGCStatus(self, stsarraymsg):
        try:
            stsarray=json.loads(stsarraymsg)
        except ValueError, err:
            self.dataman.updateStatus("DataTransformer failure: Invalid data format.")
            return
        self.uiman.controlwindow.rpa.text=str(stsarray[0])#RPA
        self.uiman.controlwindow.tpa.text=str(stsarray[1])#TPA
        self.uiman.controlwindow.tva.text=str(stsarray[2])#TVA
        self.uiman.controlwindow.tda.text=str(stsarray[3])#TDA
        self.uiman.controlwindow.moa.text=str(stsarray[4])#MOA

    def motioncmd(self, msg):
        self.datatrans.motioncmd(msg)

    def updateLastCMD(self, cmd):
        self.uiman.controlwindow.cmdlbl.text="Last Command: " + cmd

class dataTransformer():
    datahighway=None
    dataman=None

    def __init__(self, _datahighway,_dataman):
        self.datahighway=_datahighway
        self.dataman=_dataman

    def findctrls(self):
        cmd=json.dumps({'cmd':'list_controllers'})
        self.datahighway.protocol.sendData(cmd)

    def requeststs(self):
        cmd=json.dumps({'cmd':'send_status','ctrlid':self.dataman.selectedCtrlID})
        self.datahighway.protocol.sendData(cmd)
        reactor.callLater(1, self.requeststs)


    def motioncmd(self, msg):
        cmd=json.dumps({'cmd':'motion_cmd','ctrlid':self.dataman.selectedCtrlID,'gccmd':msg})
        self.datahighway.protocol.sendData(cmd)

    def decode(self, msg):
        try:
            response=json.loads(msg)
            #self.dataman.updateStatus(response['cmd'])
        except ValueError, err:
            self.dataman.updateStatus("DataTransformer failure: Invalid data format.")
            return
        if response['cmd']=='controllers_list':
            for ctrl in response['ids']:
                self.dataman.addController(ctrl)
        elif response['cmd']=='status_send':
            self.dataman.updateGCStatus(response['status'])
