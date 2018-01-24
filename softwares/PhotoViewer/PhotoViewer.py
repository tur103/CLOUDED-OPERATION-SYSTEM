from PIL import Image
import sys
from photo_constants import *
import glob
import os


class PhotoViewer(object):

    """

    PHOTO VIEWER KEYBOARD MANAGER:
        Space: Start/Stop slide show.
        G: Pain image in Gray/Colorful
        F: Display/Hide face recognition.
        N: Go to Next image.
        P: Go to Previous image.

    """

    def __init__(self):
        self.file_name = sys.argv[1].replace("\\", "/")
        self.image = self.get_image()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.slide_show = False
        self.list_of_photos = self.get_all_photos()
        self.is_gray = False
        self.is_face = False
        self.display_image()

    def resize_image(self):
        image = Image.open(self.file_name)
        image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
        image.save(self.file_name)

    def get_image(self):
        self.resize_image()
        return cv2.imread(self.file_name)

    def set_image_gray(self):
        self.image = cv2.imread(self.file_name, 0)
        self.is_gray = True

    def set_image_colorful(self):
        self.image = cv2.imread(self.file_name, 1)
        self.is_gray = False
        if self.is_face:
            self.is_face = False
            self.find_faces()

    def add_credits(self):
        cv2.putText(self.image, CREDITS1, (40, 560), self.font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(self.image, CREDITS2, (40, 590), self.font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

    def get_all_photos(self):
        photo_folder = os.path.join(os.path.dirname(self.file_name), "*")
        return [x.replace("\\", "/") for x in glob.glob(photo_folder) if x.endswith(tuple(PHOTO_EXTS))]

    def display_image(self):
        while True:
            delay = 0 if not self.slide_show else 4000
            self.add_credits()
            cv2.imshow(PHOTO_TITLE, self.image)
            key = cv2.waitKey(delay)
            print key
            if key == EXIT and not self.slide_show:
                break
            elif key == SPACE:
                self.slide_show = True if not self.slide_show else False
            elif key == GRAY:
                self.set_image_colorful() if self.is_gray else self.set_image_gray()
            elif key == FACE:
                self.find_faces()
            elif key == NEXT:
                self.is_gray = False
                self.is_face = False
                self.next_image()
            elif key == PREVIOUS:
                self.is_gray = False
                self.is_face = False
                self.previous_image()
            if self.slide_show and key == EXIT:
                self.is_gray = False
                self.is_face = False
                self.replace_image()

    def replace_image(self):
        list_length = len(self.list_of_photos)
        index = self.list_of_photos.index(self.file_name) + 1
        index = 0 if index == list_length else index
        self.file_name = self.list_of_photos[index]
        self.image = self.get_image()

    def next_image(self):
        self.replace_image()

    def previous_image(self):
        list_length = len(self.list_of_photos)
        index = self.list_of_photos.index(self.file_name) - 1
        index = list_length - 1 if index < 0 else index
        self.file_name = self.list_of_photos[index]
        self.image = self.get_image()

    def find_faces(self):
        if self.is_face:
            self.image = self.get_image()
            self.is_face = False
            if self.is_gray:
                self.set_image_gray()
        else:
            if self.is_gray:
                self.set_image_colorful()
                self.is_gray = True
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            self.is_face = True


PhotoViewer()
