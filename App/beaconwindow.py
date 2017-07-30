from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("beaconwindow.kv")
class hostBtn(Button):
    window=None
    def selectServer(self, ipaddr):
        self.window.dataman.selectServer(ipaddr)
        self.window.uiman.selectserverwindow()

class beaconWindow(FloatLayout):
    dataman=None
    uiman=None

    #def __init__(self, _dataman, _uiman):
    #    self.dataman=_dataman
    #    self.uiman=_uiman

    def clearServersList(self):
        self.hostsContainer.clear_widgets()

    def addServerBtn(self, host):
        btn=hostBtn(text=host)
        btn.window=self
        self.hostsContainer.add_widget(btn)
