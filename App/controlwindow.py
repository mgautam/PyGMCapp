from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class RelMoveBtn(Button):
    def move_relative(self, distance):
        ctrlwindow=self.parent.parent.parent
        cmdmsg='{"type":"relative","distance":"%s"}' % ( distance)
        ctrlwindow.dataman.motioncmd(cmdmsg)

class RelGoBtn(Button):
    def move_relative(self, distance):
        ctrlwindow=self.parent.parent.parent
        cmdmsg='{"type":"relative","distance":"%s"}' % ( distance)
        ctrlwindow.dataman.motioncmd(cmdmsg)

class AbsMoveBtn(Button):
    def move_absolute(self, distance):
        ctrlwindow=self.parent.parent.parent
        cmdmsg=json.dumps({"type":"absolute","distance":distance})
        ctrlwindow.dataman.motioncmd(cmdmsg)

class AbsGoBtn(Button):
    def move_absolute(self, distance):
        ctrlwindow=self.parent.parent.parent
        cmdmsg=json.dumps({"type":"absolute","distance":distance})
        ctrlwindow.dataman.motioncmd(cmdmsg)


from kivy.lang import Builder
Builder.load_file("controlwindow.kv")
import json
class controlWindow(FloatLayout):
    dataman=None
    uiman=None

    def updateGCStatus(self, stsarraymsg):
        try:
            stsarray=json.loads(stsarraymsg)
        except ValueError, err:
            self.dataman.updateStatus("DataTransformer failure: Invalid data format.")
            return
        self.rpa.text=str(stsarray[0])#RPA
        self.tpa.text=str(stsarray[1])#TPA
        self.tva.text=str(stsarray[2])#TVA
        self.tda.text=str(stsarray[3])#TDA
        self.moa.text=str(stsarray[4])#MOA

