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

FACE_CASCADE = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascades/haarcascade_frontalface_default.xml'))