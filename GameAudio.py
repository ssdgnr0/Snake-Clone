from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
from panda3d.core import Point3
from panda3d.core import AudioManager

class Audio():

    def __init__(self):
        self.audio_list = ["sound01.wav"]
        self.musicMgr = base.sfxManagerList[0]
        self.music =  loader.loadSfx(self.audio_list[0])
        self.musicMgr.setVolume(0.5)
        self.music.setLoop(True)
        self.music.play()
       
