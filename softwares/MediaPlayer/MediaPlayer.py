from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
import sys
from shutil import copyfile
import os
from media_constants import *


class MediaPlayer(ShowBase):
    def __init__(self, media_file):
        # Tell Panda3D to use OpenAL, not FMOD
        loadPrcFileData("", AUDIO_LIBRARY)
        self.media_file = media_file
        self.get_video()
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.display_text()
        self.tex = None
        self.load_texture()
        self.set_fullscreen()
        self.sound = None
        self.synchronize_sound()
        self.set_keys_acceptions()
        self.sound.play()

    def get_video(self):
        video_name = self.media_file.split("\\")[-1]
        folder = "\\".join(os.path.dirname(os.path.abspath(__file__)).split("\\")[:-2])
        copyfile(self.media_file, "\\".join([folder, video_name]))
        self.media_file = video_name

    # Function to put title on the screen.
    def add_title(self, text):
        return OnscreenText(text=text, style=1, pos=(-0.1, 0.09), scale=.07,
                            parent=self.a2dBottomRight, align=TextNode.ARight,
                            fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))

    # Function to put instructions on the screen.
    def add_instructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(0, 0, 0, 1), shadow=(1, 1, 1, 1),
                            parent=self.a2dTopLeft, align=TextNode.ALeft,
                            pos=(0.08, -pos - 0.04), scale=.06)

    def display_text(self):
        self.add_title(TITLE)
        self.add_instructions(PLAY_PAUSE_PLACE, PLAY_PAUSE)
        self.add_instructions(STOP_PLACE, STOP)
        self.add_instructions(SLOW_MOTION_PLACE, SLOW_MOTION)
        self.add_instructions(FAST_FORWARD_PLACE, FAST_FORWARD)
        self.add_instructions(GET_FORWARD_PLACE, GET_FORWARD)
        self.add_instructions(GET_BACK_PLACE, GET_BACK)

    def load_texture(self):
        # Load the texture. We could use loader.loadTexture for this,
        # but we want to make sure we get a MovieTexture, since it
        # implements synchronizeTo.
        self.tex = MovieTexture(NAME)
        success = self.tex.read(self.media_file)
        assert success, FAILED

    def set_fullscreen(self):
        # Set up a fullscreen card to set the video texture on.
        cm = CardMaker(FULL_SCREEN)
        cm.setFrameFullscreenQuad()
        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.tex)
        # Now place the card in the scene graph and apply the texture to it.
        card = NodePath(cm.generate())
        card.reparentTo(self.render2d)
        card.setTexture(self.tex)

    def synchronize_sound(self):
        self.sound = loader.loadSfx(self.media_file)
        # Synchronize the video to the sound.
        self.tex.synchronizeTo(self.sound)

    def set_keys_acceptions(self):
        self.accept('m', self.slow_motion)
        self.accept('M', self.slow_motion)
        self.accept('s', self.stop)
        self.accept('S', self.stop)
        self.accept('p', self.play_pause)
        self.accept('P', self.play_pause)
        self.accept('f', self.fast_forward)
        self.accept('F', self.fast_forward)
        self.accept('arrow_right', self.get_forward)
        self.accept('arrow_left', self.get_back)
        self.accept('arrow_up', self.volume_up)
        self.accept('arrow_down', self.volume_down)

    def get_forward(self):
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            t += 3
            self.sound.stop()
            self.sound.setTime(t)
            self.sound.play()

    def get_back(self):
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            t -= 3
            if t < 0:
                t = 0
            self.sound.stop()
            self.sound.setTime(t)
            self.sound.play()

    def volume_up(self):
        volume = self.sound.getVolume()
        volume += 2
        self.sound.setVolume(volume)
        print self.sound.getVolume()

    def volume_down(self):
        volume = self.sound.getVolume()
        volume -= 2
        if volume < 1:
            volume = 1
        self.sound.setVolume(volume)

    def stop(self):
        self.sound.stop()
        self.sound.setPlayRate(1.0)
        self.sound.setTime(0)
        self.sound.play()
        self.sound.stop()

    def fast_forward(self):
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            self.sound.stop()
            if self.sound.getPlayRate() == 1.0:
                self.sound.setPlayRate(1.5)
            else:
                self.sound.setPlayRate(1.0)
            self.sound.setTime(t)
            self.sound.play()

    def play_pause(self):
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            self.sound.stop()
            self.sound.setTime(t)
        else:
            self.sound.play()

    def slow_motion(self):
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            self.sound.stop()
            if self.sound.getPlayRate() == 1.0:
                self.sound.setPlayRate(0.5)
            else:
                self.sound.setPlayRate(1.0)
            self.sound.setTime(t)
            self.sound.play()


player = MediaPlayer(sys.argv[1])
player.run()
