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

def create_rounded_button(master, text, command):
    button_frame = ttk.Frame(master, relief='solid')
    button_frame.pack(pady=3)

    button = tk.Button(button_frame, text=text, command=command, width=15, relief='flat', fg='black', font=("Arial", 14))
    button.pack(ipadx=10, ipady=10, fill='both')

    button_frame.bind("<Enter>", lambda e: button_frame.configure(relief='groove'))
    button_frame.bind("<Leave>", lambda e: button_frame.configure(relief='solid'))

    return button

# Encapsulation - logic is protected and simplified by keeping attributes private to the class.
class FaceDetectionApp:
    '''Tkinter GUI Application'''

    def __init__(self, master):
        self.master = master
        master.title("Face Detection App")
        master.minsize(500, 300)

        self.title_label = tk.Label(master, text="Face Detection Application", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.description_label = tk.Label(master, text="Detect facial objects in any image!", font=("Arial", 14))
        self.description_label.pack(pady=0)

        self.label = tk.Label(master, text="Upload an Image:")
        self.label.pack(pady=(20, 5))

        self.upload_button = create_rounded_button(master, "Upload Image", self.upload_image)

        self.upload_desc = tk.Label(master, text="Click to select an image from your files.", font=("Arial", 10))
        self.upload_desc.pack()

        self.process_button = create_rounded_button(master, "Detect Faces", self.detect_faces)

        self.process_desc = tk.Label(master, text="Click to detect faces in the uploaded image.", font=("Arial", 10))
        self.process_desc.pack()

        self.image_path = ""

    def upload_image(self):
        """Upload an image and store the path."""
        self.image_path = filedialog.askopenfilename()
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image.")
        else:
            messagebox.showinfo("Info", "Image uploaded successfully!")

    def detect_faces(self):
        """Detect faces in the uploaded image."""
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        
        face_detector = FaceDetector(self.image_path)
        output_path = face_detector.process()

        self.display_image(output_path)

    def display_image(self, output_path):
        """Display the processed image with detected faces."""
        image = Image.open(output_path)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)

        self.result_label = tk.Label(self.master, image=photo)
        self.result_label.image = photo
        self.result_label.pack(pady=(20, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
