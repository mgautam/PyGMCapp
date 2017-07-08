#Android app for controlling PSI Goniometers
from kivy.app import App
from kivy.config import Config
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from scrman import ScrManBuilder

class PyPSIApp(App):
    screensBuilder=None
    def build(self):
        self.screensBuilder=ScrManBuilder()
        return self.screensBuilder.buildScrMan()

if __name__ == '__main__':
    Config.set('graphics', 'width',  960)
    Config.set('graphics', 'height', 540)
    PyPSIApp().run()
