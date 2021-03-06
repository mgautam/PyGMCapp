from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
Builder.load_file("serverwindow.kv")
class ctrlBtn(Button):
    window=None
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.window.dataman.selectController(self.text)
            self.window.uiman.selectcontrolwindow()
            return True
        return super(ctrlBtn, self).on_touch_down(touch)

class serverWindow(FloatLayout):
    dataman=None
    uiman=None

    #def __init__(self, _dataman, _uiman):
    #    self.dataman=_dataman
    #    self.uiman=_uiman

    def clearCtrllrsList(self):
        self.ctrlsContainer.clear_widgets()

    def addCntrllrBtn(self, ctrlr):
        btn=ctrlBtn(text=ctrlr)
        btn.window=self
        self.ctrlsContainer.add_widget(btn)
