import cv2
import os

IMAGE_SIZE = (700, 600)
PHOTO_TITLE = "PHOTO VIEWER"
CREDITS1 = "PHOTO VIEWER 1.0 FROM < CLOUDED OPERATION SYSTEM >"
CREDITS2 = "BY OR ISRAELI"
PHOTO_EXTS = [".jpg", ".png"]

EXIT = -1
SPACE = 32
GRAY = 103
FACE = 102
NEXT = 110
PREVIOUS = 112
RIGHT = 114
LEFT = 108
SAVE = 115
ZOOM = 122
BLUR = 98
EYES = 101
SMILE = 109

ZOOM_SCALING = [[250, 200], [450, 200], [250, 400], [450, 400]]
REGULAR_SCALING = [[0, 0], [700, 0], [0, 600], [700, 600]]
BLUR_TYPE = (5, 5)

FACE_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascades/haarcascade_frontalface_default.xml'))
EYES_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascades/haarcascade_eye.xml'))
SMILE_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascades/haarcascade_smile.xml'))