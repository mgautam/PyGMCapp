from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("beaconwindow.kv")
class hostBtn(Button):
    window=None
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.window.dataman.selectServer(self.text)
            self.window.uiman.selectserverwindow()
            return True
        return super(hostBtn, self).on_touch_down(touch)

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
