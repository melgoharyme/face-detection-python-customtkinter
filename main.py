from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


def change_appearance_mode(mode):
    customtkinter.set_appearance_mode(mode)


class FacesRoot(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Indexed Faces")
        self.resizable(0, 0)
        self.configure_and_hide_frame()

    def configure_and_hide_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.second_frame = customtkinter.CTkScrollableFrame(self, width=400, height=400)
        self.second_frame.pack(side="left", expand=0, padx=16, pady=16)
        self.second_frame_title = customtkinter.CTkLabel(self.second_frame, text="Indexed Faces", font=customtkinter.CTkFont(size=20, weight="bold"),)
        self.second_frame_title.grid(row=0, column=0, padx=8, pady=8)
        self.second_frame.grid()

    def display_faces(self, detected_faces):
        for i, (face_pil, face_number) in enumerate(detected_faces):
            max_width, aspect_ratio = 48, 48 / face_pil.width
            new_height = int(face_pil.height * aspect_ratio)
            face_pil = face_pil.resize((max_width, new_height), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(face_pil)
            face_canvas = customtkinter.CTkCanvas(self.second_frame, width=48, height=new_height)
            face_canvas.grid(row=i + 1, column=0, padx=0, pady=8)
            face_canvas.create_image(0, 0, anchor="nw", image=image_tk)
            face_canvas.image = image_tk
            face_label = customtkinter.CTkLabel(self.second_frame, text=f"Face No #{face_number}", font=customtkinter.CTkFont(family="Product Sans", size=14, weight="bold"))
            face_label.grid(row=i + 1, column=1, padx=0, pady=8)


class Root(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Faces Detection")
        self.resizable(0, 0)
        self.selected_image_path = None
        self.configure_sidebar_frame()
        self.configure_main_frame()
        self.toplevel_window = None

    def configure_sidebar_frame(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.pack(side="left", expand="false", fill="y")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Face Recognition", font=customtkinter.CTkFont(family="Product Sans",size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=16, pady=(16, 8))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Upload Image", font=customtkinter.CTkFont(family="Product Sans", size=14, weight="bold"), corner_radius=8, command=self.select_image)
        self.sidebar_button_1.grid(row=1, column=0, columnspan=1, sticky="news", padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Indexed Faces",
                                                        font=customtkinter.CTkFont(family="Product Sans", size=14, weight="bold"), corner_radius=8,
                                                        command=self.detect_faces)
        self.sidebar_button_2.grid(row=2, column=0, columnspan=1, sticky="news", padx=20, pady=10)
        self.sidebar_button_2.grid_remove()
        self.configure_appearance_mode()

    def configure_appearance_mode(self):
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w",
                                                            font=customtkinter.CTkFont(family="Product Sans", size=12)
                                                            , corner_radius=8)
        self.appearance_mode_label.grid(row=5, column=0, columnspan=1, sticky="news", padx=20, pady=(10, 0))
        self.appearance_mode = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], font=customtkinter.CTkFont(family="Product Sans", size=14, weight="bold"), corner_radius=8, command=change_appearance_mode)
        self.appearance_mode.set("System")
        self.appearance_mode.grid(row=6, column=0, columnspan=1, sticky="news", padx=20, pady=(10, 10))

    def configure_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_frame.pack(side="left", padx=0, pady=0, expand="false")
        self.configure_main_labels()
        self.canvas = customtkinter.CTkCanvas(self.main_frame, width=400, height=400)
        self.canvas.grid(row=2, column=0, columnspan=4, sticky="news", padx=16, pady=0)
        self.canvas.grid_remove()
        self.main_button_1 = customtkinter.CTkButton(self.main_frame, text="Detect Faces", font=customtkinter.CTkFont(family="Product Sans", size=16, weight="bold"), corner_radius=8, height=40, command=self.detect_faces)
        self.main_button_1.grid(row=3, column=0, columnspan=4, sticky="news", padx=16, pady=16)
        self.main_button_1.grid_remove()

    def configure_main_labels(self):
        self.main_label_1 = customtkinter.CTkLabel(self.main_frame, text="Upload Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label_1.grid(row=0, column=0, columnspan=4, sticky="news", padx=16, pady=16)
        self.main_label_2 = customtkinter.CTkLabel(self.main_frame, text="Pathes allowed : *.jpg / *.png / *.bmp")
        self.main_label_2.grid(row=1, column=0, columnspan=4, sticky="news", padx=16, pady=16)

    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg;*.png;*.bmp")])
        if file_path:
            self.selected_image_path = file_path
            self.show_image()

    def show_image(self):
        if self.selected_image_path:
            image = Image.open(self.selected_image_path)
            self.adjust_and_show_image(image)

    def adjust_and_show_image(self, image):
        max_width = 400
        if image.width > max_width:
            aspect_ratio = max_width / image.width
            new_height = int(image.height * aspect_ratio)
            image = image.resize((max_width, new_height), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        self.canvas.image = image
        self.canvas.create_image(0, 0, anchor="nw", image=image)
        self.canvas.grid()
        self.main_button_1.grid()

    def detect_faces(self):
        if self.selected_image_path:
            image_cv2 = cv2.imread(self.selected_image_path)
            gray_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(image_cv2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            image_cv2_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_cv2_rgb)
            self.adjust_and_show_image(image_pil)
            detected_faces = [(Image.fromarray(cv2.cvtColor(image_cv2[y:y + h, x:x + w], cv2.COLOR_BGR2RGB)), i + 1) for i, (x, y, w, h) in enumerate(faces)]
            if detected_faces:
                self.show_detected_faces(detected_faces)
                self.sidebar_button_2.grid()

    def show_detected_faces(self, detected_faces):
        if not (self.toplevel_window and self.toplevel_window.winfo_exists()):
            self.toplevel_window = FacesRoot(self)
        else:
            self.toplevel_window.second_frame.grid_remove()
            self.toplevel_window.second_frame_title.grid_remove()
        self.toplevel_window.display_faces(detected_faces)
        self.sidebar_button_2.grid()

    def show_indexed_faces(self):
        self.toplevel_window.second_frame.grid()
        self.toplevel_window.second_frame_title.grid()
        self.sidebar_button_2.grid_remove()


if __name__ == "__main__":
    root = Root()
    root.mainloop()