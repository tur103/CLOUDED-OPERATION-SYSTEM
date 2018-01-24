from PIL import Image
import sys
from photo_constants import *
import glob
import os
import numpy as np


class PhotoViewer(object):

    """

    PHOTO VIEWER KEYBOARD MANAGER:
        Space: Start/Stop slide show.
        G: Pain image in Gray/Colorful
        F: Display/Hide face recognition.
        N: Go to Next image.
        P: Go to Previous image.
        R: Rotate the image to the Right.
        L: Rotate the image to the Left.
        S: Save the image.
        Z: Zoom In/Out.
        B: Blur/UnBlur the image

    """

    def __init__(self):
        self.file_name = sys.argv[1].replace("\\", "/")
        self.image = self.get_image()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.slide_show = False
        self.list_of_photos = self.get_all_photos()
        self.is_gray = False
        self.is_face = False
        self.rotation = 0
        self.zoom = False
        self.blur = False
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
            if key == EXIT and not self.slide_show:
                break
            elif key == SPACE:
                self.slide_show = True if not self.slide_show else False
            elif key == GRAY:
                self.set_image_colorful() if self.is_gray else self.set_image_gray()
                self.rotation = 0
                self.zoom = False
                self.blur = False
            elif key == FACE:
                self.find_faces()
            elif key == NEXT:
                self.is_gray = False
                self.is_face = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
                self.next_image()
            elif key == PREVIOUS:
                self.is_gray = False
                self.is_face = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
                self.previous_image()
            elif key == RIGHT:
                self.rotation += 1
                self.rotate_right()
                self.is_gray = False
                self.is_face = False
                self.zoom = False
                self.blur = False
            elif key == LEFT:
                self.rotation -= 1
                self.rotate_left()
                self.is_gray = False
                self.is_face = False
                self.zoom = False
                self.blur = False
            elif key == SAVE:
                self.save_image()
            elif key == ZOOM:
                self.zoom_out() if self.zoom else self.zoom_in()
            elif key == BLUR:
                self.unblur_image() if self.blur else self.blur_image()
            if self.slide_show and key == EXIT:
                self.is_gray = False
                self.is_face = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
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

    def rotate_right(self):
        self.rotation = 0 if self.rotation > 3 else self.rotation
        self.image = self.get_image()
        for rotaions in range(self.rotation):
            rows, cols, type = self.image.shape
            rotation = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
            self.image = cv2.warpAffine(self.image, rotation, (cols, rows))

    def rotate_left(self):
        self.rotation = 3 if self.rotation < 0 else self.rotation
        self.image = self.get_image()
        for rotations in range(4 - self.rotation):
            rows, cols, type = self.image.shape
            rotation = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            self.image = cv2.warpAffine(self.image, rotation, (cols, rows))

    def zoom_in(self):
        self.zoom = True
        zoom_point_of_view = np.float32(ZOOM_SCALING)
        regular_point_of_view = np.float32(REGULAR_SCALING)
        zooming = cv2.getPerspectiveTransform(zoom_point_of_view, regular_point_of_view)
        self.image = cv2.warpPerspective(self.image, zooming, IMAGE_SIZE)

    def zoom_out(self):
        self.zoom = False
        self.image = self.get_image()
        self.is_gray = False
        self.is_face = False
        self.rotation = 0
        self.blur = False

    def blur_image(self):
        self.blur = True
        self.image = cv2.blur(self.image, BLUR_TYPE)

    def unblur_image(self):
        self.blur = False
        self.image = self.get_image()
        self.is_gray = False
        self.is_face = False
        self.rotation = 0
        self.zoom = False

    def save_image(self):
        self.image = self.get_image()
        if self.is_gray:
            self.set_image_gray()
        elif self.rotation > 0:
            self.rotate_right()
        if self.zoom:
            self.zoom_in()
        if self.blur:
            self.blur_image()
        cv2.imwrite(self.file_name, self.image)

    def find_faces(self):
        if self.is_face:
            self.image = self.get_image()
            self.rotation = 0
            self.zoom = False
            self.blur = False
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
