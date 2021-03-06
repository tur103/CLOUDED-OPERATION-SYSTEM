from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
import sys
from shutil import copyfile
import os
from media_constants import *

from pandac.PandaModules import WindowProperties


class MediaPlayer(ShowBase):
    def __init__(self, media_file):
        # Tell Panda3D to use OpenAL, not FMOD
        loadPrcFileData("", AUDIO_LIBRARY)
        self.media_file = media_file
        self.get_video()
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle(MEDIA_TITLE + media_file)
        props.setIconFilename(MEDIA_ICON)
        self.win.requestProperties(props)
        self.display_text()
        self.tex = None
        self.load_texture()
        self.set_fullscreen()
        self.sound = None
        self.synchronize_sound()
        self.set_keys_acceptions()
        self.sound.play()

    def get_video(self):
        """

        Getting the video to the media player folder from it's path
        and generating it's name.

        """
        video_name = self.media_file.split("\\")[-1]
        folder = os.path.dirname(os.path.abspath(__file__))
        copyfile(self.media_file, "\\".join([folder, video_name]))
        self.media_file = video_name

    def add_title(self, text):
        """

        Function to put title on the screen.

        args:
            text (string): The request title.

        """
        return OnscreenText(text=text, style=1, pos=(-0.1, 0.09), scale=.07,
                            parent=self.a2dBottomRight, align=TextNode.ARight,
                            fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))

    # Function to put instructions on the screen.
    def add_instructions(self, pos, msg):
        """

        Function to put instructions on the screen.

        args:
            pos (float): The request position on the screen.
            msg (string): The instruction to display.

        """
        return OnscreenText(text=msg, style=1, fg=(0, 0, 0, 1), shadow=(1, 1, 1, 1),
                            parent=self.a2dTopLeft, align=TextNode.ALeft,
                            pos=(0.08, -pos - 0.04), scale=.06)

    def display_text(self):
        """

        Executing the displaying of the title and
        instructions on the screen.

        """
        self.add_title(TITLE)
        self.add_instructions(PLAY_PAUSE_PLACE, PLAY_PAUSE)
        self.add_instructions(STOP_PLACE, STOP)
        self.add_instructions(SLOW_MOTION_PLACE, SLOW_MOTION)
        self.add_instructions(FAST_FORWARD_PLACE, FAST_FORWARD)
        self.add_instructions(GET_FORWARD_PLACE, GET_FORWARD)
        self.add_instructions(GET_BACK_PLACE, GET_BACK)
        self.add_instructions(VOLUME_UP_PLACE, VOLUME_UP)
        self.add_instructions(VOLUME_DOWN_PLACE, VOLUME_DOWN)

    def load_texture(self):
        """

        Load the texture. We could use loader.loadTexture for this,
        but we want to make sure we get a MovieTexture, since it
        implements synchronizeTo.

        """
        self.tex = MovieTexture(NAME)
        success = self.tex.read(self.media_file)
        assert success, FAILED

    def set_fullscreen(self):
        """

        Set up a fullscreen card to set the video texture on.
        Tell the CardMaker to create texture coordinates that take into
        account the padding region of the texture.
        and place the card in the scene graph and apply the texture to it.

        """
        cm = CardMaker(FULL_SCREEN)
        cm.setFrameFullscreenQuad()
        cm.setUvRange(self.tex)
        card = NodePath(cm.generate())
        card.reparentTo(self.render2d)
        card.setTexture(self.tex)

    def synchronize_sound(self):
        """

        Synchronize the video to the sound.

        """
        self.sound = loader.loadSfx(self.media_file)
        self.tex.synchronizeTo(self.sound)

    def set_keys_acceptions(self):
        """

        Sets the keyboard keys and synchronizes
        them to the actions.

        """
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
        """

        Getting 3 seconds forward in the video.

        """
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            t += 3
            self.sound.stop()
            self.sound.setTime(t)
            self.sound.play()

    def get_back(self):
        """

        Getting 3 seconds backward in the video.

        """
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            t -= 3
            if t < 0:
                t = 0
            self.sound.stop()
            self.sound.setTime(t)
            self.sound.play()

    def volume_up(self):
        """

        Voluming up the sound in the video.

        """
        volume = self.sound.getVolume()
        volume += 20
        self.sound.setVolume(volume)

    def volume_down(self):
        """

        Voluming down the sound in the video.

        """
        volume = self.sound.getVolume()
        volume -= 2
        if volume < 1:
            volume = 1
        self.sound.setVolume(volume)

    def stop(self):
        """

        Stops the video.

        """
        self.sound.stop()
        self.sound.setPlayRate(1.0)
        self.sound.setTime(0)
        self.sound.play()
        self.sound.stop()

    def fast_forward(self):
        """

        Fast forwarding the video.

        """
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
        """

        play or pause the video.

        """
        if self.sound.status() == AudioSound.PLAYING:
            t = self.sound.getTime()
            self.sound.stop()
            self.sound.setTime(t)
        else:
            self.sound.play()

    def slow_motion(self):
        """

        Slow motioning the video.

        """
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
