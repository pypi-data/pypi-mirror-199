import pychromecast
from MawaqitAPI.constants import ADHAN_URL

class ChromeCast():
    """
    A class to control a Google Chromecast device. To play the adhan
    """
    def __init__(self, friendly_name):
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
        self.cast = chromecasts[0]
        self.cast.wait()
        self.mc = self.cast.media_controller
    
    def set_volume(self, volume):
        self.cast.set_volume(volume)
    
    def play(self, url, media_type):
        self.mc.play_media(url, media_type)
        self.mc.block_until_active()
    
    def pause(self):
        self.mc.pause()
    
    def get_status(self):
        return self.mc.status

if __name__ == "__main__":
    cast = ChromeCast("Living Room speaker")
    cast.set_volume(0.4)
    cast.play(ADHAN_URL, "audio/mp3")
    print(cast.get_status())
    
    

#Living Room speaker