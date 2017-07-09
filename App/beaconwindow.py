from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("beaconwindow.kv")
class hostBtn(Button):
    pass

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
        btn.bind(on_touch_down=self.dataman.setServer)
        btn.bind(on_press=self.uiman.nextscreen)
        self.hostsContainer.add_widget(btn)


