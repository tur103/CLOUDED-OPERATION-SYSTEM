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
        self.is_eyes = False
        self.is_smile = False
        self.rotation = 0
        self.zoom = False
        self.blur = False
        self.display_image()

    def resize_image(self):
        """

        Resizing the image for the software size.

        """
        image = Image.open(self.file_name)
        image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
        image.save(self.file_name)

    def get_image(self):
        """

        returning the image file as a cv2 image.

        return:
            cv2.imread: the cv2 image file.

        """
        self.resize_image()
        return cv2.imread(self.file_name)

    def set_image_gray(self):
        """

        Sets the image as black/white.

        """
        self.image = cv2.imread(self.file_name, 0)
        self.is_gray = True

    def set_image_colorful(self):
        """

        Sets the image as colorful.

        """
        self.image = cv2.imread(self.file_name, 1)
        self.is_gray = False
        if self.is_face:
            self.is_face = False
            self.find_faces()
        if self.is_eyes:
            self.is_eyes = False
            self.find_eyes()
        if self.is_smile:
            self.is_smile = False
            self.find_smiles()

    def add_credits(self):
        """

        Prints the credits on the image.

        """
        cv2.putText(self.image, CREDITS1, (40, 560), self.font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(self.image, CREDITS2, (40, 590), self.font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

    def get_all_photos(self):
        """

        Gets all the photos in the specified directory
        to display slide show of them.

        return:
            list: List of all the images in the folder.

        """
        photo_folder = os.path.join(os.path.dirname(self.file_name), "*")
        return [x.replace("\\", "/") for x in glob.glob(photo_folder) if x.endswith(tuple(PHOTO_EXTS))]

    def display_image(self):
        """

        Displaying the image on the screen.

        """
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
                self.rotation = 0
                self.zoom = False
                self.blur = False
            elif key == FACE:
                self.find_faces()
            elif key == EYES:
                self.find_eyes()
            elif key == SMILE:
                self.find_smiles()
            elif key == NEXT:
                self.is_gray = False
                self.is_face = False
                self.is_eyes = False
                self.is_smile = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
                self.next_image()
            elif key == PREVIOUS:
                self.is_gray = False
                self.is_face = False
                self.is_eyes = False
                self.is_smile = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
                self.previous_image()
            elif key == RIGHT:
                self.rotation += 1
                self.rotate_right()
            elif key == LEFT:
                self.rotation -= 1
                self.rotate_left()
            elif key == SAVE:
                self.save_image()
            elif key == ZOOM:
                self.zoom_out() if self.zoom else self.zoom_in()
            elif key == BLUR:
                self.unblur_image() if self.blur else self.blur_image()
            if self.slide_show and key == EXIT:
                self.is_gray = False
                self.is_face = False
                self.is_eyes = False
                self.is_smile = False
                self.rotation = 0
                self.zoom = False
                self.blur = False
                self.replace_image()

    def replace_image(self):
        """

        When in slide show mode, replacing the image
        to the next one in the folder.

        """
        list_length = len(self.list_of_photos)
        index = self.list_of_photos.index(self.file_name) + 1
        index = 0 if index == list_length else index
        self.file_name = self.list_of_photos[index]
        self.image = self.get_image()

    def next_image(self):
        """

        Getting to the next image in the folder.

        """
        self.replace_image()

    def previous_image(self):
        """

        Getting to the previous image in the folder.

        """
        list_length = len(self.list_of_photos)
        index = self.list_of_photos.index(self.file_name) - 1
        index = list_length - 1 if index < 0 else index
        self.file_name = self.list_of_photos[index]
        self.image = self.get_image()

    def rotate_right(self):
        """

        Rotating the image 90 degrees to the right.

        """
        self.rotation = 0 if self.rotation > 3 else self.rotation
        self.image = self.get_image()
        if self.is_gray:
            self.set_image_gray()
        if self.is_face:
            self.is_face = False
            self.find_faces()
        if self.is_eyes:
            self.is_eyes = False
            self.find_eyes()
        if self.is_smile:
            self.is_smile = False
            self.find_smiles()
        if self.zoom:
            self.zoom_in()
        if self.blur:
            self.blur_image()
        for rotaions in range(self.rotation):
            if self.is_gray and not self.is_face:
                rows, cols = self.image.shape
            else:
                rows, cols, type = self.image.shape
            rotation = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)
            self.image = cv2.warpAffine(self.image, rotation, (cols, rows))

    def rotate_left(self):
        """

        Rotating the image 90 degrees to the left.

        """
        self.rotation = 3 if self.rotation < 0 else self.rotation
        self.image = self.get_image()
        if self.is_gray:
            self.set_image_gray()
        if self.is_face:
            self.is_face = False
            self.find_faces()
        if self.is_eyes:
            self.is_eyes = False
            self.find_eyes()
        if self.is_smile:
            self.is_smile = False
            self.find_smiles()
        if self.zoom:
            self.zoom_in()
        if self.blur:
            self.blur_image()
        for rotations in range(4 - self.rotation):
            if self.is_gray and not self.is_face:
                rows, cols = self.image.shape
            else:
                rows, cols, type = self.image.shape
            rotation = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            self.image = cv2.warpAffine(self.image, rotation, (cols, rows))

    def zoom_in(self):
        """

        Zooming in to the image.

        """
        self.zoom = True
        zoom_point_of_view = np.float32(ZOOM_SCALING)
        regular_point_of_view = np.float32(REGULAR_SCALING)
        zooming = cv2.getPerspectiveTransform(zoom_point_of_view, regular_point_of_view)
        self.image = cv2.warpPerspective(self.image, zooming, IMAGE_SIZE)

    def zoom_out(self):
        """

        Zooming out to the image.

        """
        self.zoom = False
        self.image = self.get_image()
        self.rotate_right()

    def blur_image(self):
        """

        Blurring the image.

        """
        self.blur = True
        self.image = cv2.blur(self.image, BLUR_TYPE)

    def unblur_image(self):
        """

        Unblurring the image.

        """
        self.blur = False
        self.image = self.get_image()
        self.rotate_right()

    def save_image(self):
        """

        Saving the image the image with it's changes.

        """
        self.is_face = False
        self.is_eyes = False
        self.is_smile = False
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
        """

        Finding and marking faces in the image.

        """
        if self.is_face:
            self.image = self.get_image()
            self.is_face = False
            self.rotate_right()
        else:
            if self.is_gray:
                self.set_image_colorful()
                self.is_gray = True
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            self.is_face = True

    def find_eyes(self):
        """

        Finding and marking eyes in the image.

        """
        if self.is_eyes:
            self.image = self.get_image()
            self.is_eyes = False
            self.rotate_right()
        else:
            if self.is_gray:
                self.set_image_colorful()
                self.is_gray = True
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = self.image[y:y+h, x:x+w]
                eyes = EYES_CASCADE.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            self.is_eyes = True

    def find_smiles(self):
        """

        Finding and marking smiles in the image.

        """
        if self.is_smile:
            self.image = self.get_image()
            self.is_smile = False
            self.rotate_right()
        else:
            if self.is_gray:
                self.set_image_colorful()
                self.is_gray = True
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = self.image[y:y+h, x:x+w]
                smile = SMILE_CASCADE.detectMultiScale(roi_gray)
                try:
                    ex, ey, ew, eh = smile[0]
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
                except IndexError:
                    pass
            self.is_smile = True


PhotoViewer()
