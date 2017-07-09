#Android app for controlling PSI Goniometers
from kivy.app import App
from kivy.config import Config
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from dataman import DataManager
from uiman import UIManager

class PyPSIApp(App):
    datamanager=None
    uimanager=None
    def build(self):
        self.datamanager=DataManager(self.uimanager)
        self.uimanager=UIManager(self.datamanager)
        self.datamanager.uiman=self.uimanager
        return self.uimanager.buildwindows()

if __name__ == '__main__':
    Config.set('graphics', 'width',  1920)
    Config.set('graphics', 'height', 1080)
    PyPSIApp().run()
