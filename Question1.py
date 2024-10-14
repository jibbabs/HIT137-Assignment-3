import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class ImageProcessor:
    '''Base class for image processing'''

    def __init__(self, image_path):
        self.image_path = image_path

    def process(self):
        raise NotImplementedError("Subclasses should implement this!")

# Inheritance - FaceDetector inherits from ImageProcessor, allowing reuse of functionality.
class FaceDetector(ImageProcessor):
    '''Subclass for face detection'''

    def __init__(self, image_path):
        super().__init__(image_path)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Method Overriding - process in FaceDetector implements its own logic, demonstrating a 
    # versatile reuse of class methods for specific cases.
    def process(self):
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        output_path = 'output.png'
        cv2.imwrite(output_path, image)
        return output_path

