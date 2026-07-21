import customtkinter as ctk
from PIL import Image
import cv2
import threading
from tkinter import filedialog  # For file selection


class OhmegaResistorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ohmega Vision Resistor Reader")
        self.geometry("800x600")
        self.iconbitmap("Tools/OhmegaVision.ico")  # Set your icon path here

        # Bottom fram for author and version
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)
        author_label = ctk.CTkLabel(bottom_frame, text="Developed by nemelion13 - All rights reserved © 2026")
        author_label.pack(side="left", padx=10)
        version_label = ctk.CTkLabel(bottom_frame, text="Version 1.0")
        version_label.pack(side="right", padx=10)
        contact_label = ctk.CTkLabel(bottom_frame, text="Contact: nemelion13@gmail.com")
        contact_label.pack(side="right", padx=10)

        #Frame for video and zoom button
        video_frame = ctk.CTkFrame(self)
        video_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Label to display the image or video stream
        self.video_label = ctk.CTkLabel(video_frame, text="")
        self.video_label.pack(padx=10, pady=10)

        #zoom button
        zoom_frame = ctk.CTkFrame(video_frame)
        zoom_frame.pack(side="top", fill="x", padx=10, pady=10)
        zoom_label = ctk.CTkLabel(zoom_frame, text="Zoom Camera:")
        zoom_label.pack(side="left", padx=10)
        self.zoom_btn = ctk.CTkSlider(zoom_frame, from_=0, to=100, number_of_steps=10, command=self.zoom_image)
        self.zoom_btn.pack(side="left",padx=10)

        # Label to display the result
        result_frame = ctk.CTkFrame(video_frame)
        result_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.result_label = ctk.CTkLabel(result_frame, text="Value: ", font=("Arial", 20))
        self.result_label.pack(pady=10)




        # Frame for the buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="left",fill= "y",padx=10, pady=10)

        # Frame for the camera and capture buttons
        camera_frame = ctk.CTkFrame(button_frame)
        camera_frame.pack(side="top", fill="x", padx=10, pady=10)
        camera_label_frame = ctk.CTkFrame(camera_frame)
        camera_label_frame.pack(side="top", fill="x", padx=10,pady=10)
        camera_img = ctk.CTkImage(light_image=Image.open("Tools/Camera_image.png"), size=(20, 20))
        camera_icon = ctk.CTkLabel(camera_label_frame, image=camera_img, text="")
        camera_icon.pack(side="left", padx=5)
        camera_label = ctk.CTkLabel(camera_label_frame, text="Camera Control", font=("Arial", 16))
        camera_label.pack(side="left", padx=5)


        # Button to start the camera
        self.camera_btn = ctk.CTkButton(camera_frame, text="Start Camera", command=self.start_camera)
        self.camera_btn.pack(side="top", padx=10, pady=10)

        # Button to capture an image from the camera
        self.capture_btn = ctk.CTkButton( camera_frame, text="Capture", command=self.capture_image, state="disabled")
        self.capture_btn.pack(side="top", padx=10, pady=10)

        # Button to open a file
        self.file_btn = ctk.CTkButton(camera_frame, text="Open Image", command=self.open_file)
        self.file_btn.pack(side="top", padx=10, pady=10)

        

        #Frame for settings and help
        settings_frame = ctk.CTkFrame(button_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=10)
        settings_label_frame = ctk.CTkFrame(settings_frame)
        settings_label_frame.pack(side="top", fill="x", padx=10, pady=10)

        settings_img = ctk.CTkImage(light_image=Image.open("Tools/Settings_image.png"), size=(20, 20))
        settings_icon = ctk.CTkLabel(settings_label_frame, image=settings_img, text="")
        settings_icon.pack(side="left", padx=5)
        settings_label = ctk.CTkLabel(settings_label_frame,text="Settings", font=("Arial", 16))
        settings_label.pack(side="left", padx=5)


        # Combo box for appearance mode selection
        appearance_frame = ctk.CTkFrame(settings_frame)
        appearance_frame.pack(side="top", fill="x", pady=10, padx=10)
        appearance_frame_label = ctk.CTkLabel(appearance_frame, text="Appearance Mode:")
        appearance_frame_label.pack(side="left", padx=10)
        self.appearance_mode = ctk.CTkComboBox(appearance_frame, values=["Light", "Dark"], command=self.change_appearance_mode)
        self.appearance_mode.set("Light")
        self.appearance_mode.pack(pady=10)

        # combo box for language
        language_frame = ctk.CTkFrame(settings_frame)
        language_frame.pack(side="top", fill="x", pady=10, padx=10)
        language_frame_label = ctk.CTkLabel(language_frame, text="Language Mode:")
        language_frame_label.pack(side="left", padx=10)
        self.language_box = ctk.CTkComboBox(language_frame, values=["English", "Français"], command=self.change_language)
        self.language_box.set("English")
        language_frame_label.pack(side="left", padx=10)
        self.language_box.pack(pady=10)

        # Frame for help and about
        help_frame = ctk.CTkFrame(button_frame)
        help_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_label_frame = ctk.CTkFrame(help_frame)
        help_label_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_img = ctk.CTkImage(light_image=Image.open("Tools/Help_Support_image.png"), size=(20, 20))
        help_icon = ctk.CTkLabel(help_label_frame, image=help_img, text="")
        help_icon.pack(side="left", padx=5)
        help_label = ctk.CTkLabel(help_label_frame, text="Help & Support", font=("Arial", 16))
        help_label.pack(side="left", padx=5)

        # Frame for help and about buttons
        help_buttons_frame = ctk.CTkFrame(help_frame)
        help_buttons_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_btn = ctk.CTkButton(help_buttons_frame, text="Help", command=self.show_help)
        help_btn.pack(side="left", padx=10, pady=10)
        guide_btn = ctk.CTkButton(help_buttons_frame, text="Guide", command=self.show_guide)
        guide_btn.pack(side="left", padx=10, pady=10)
        #about_btn = ctk.CTkButton(help_buttons_frame, text="About", command=self.show_about)
        #about_btn.pack(side="top", padx=10, pady=10)

        # window for displaying guide for resistor calculation
        self.guide_window = ctk.CTkToplevel(self)
        self.guide_window.title("Resistor Calculation Guide")
        self.guide_window.geometry("600x400")
        #self.guide_window.withdraw()  # Hide the window initially

        # Main frame displaying content
        guide_frame = ctk.CTkFrame(self.guide_window)
        guide_frame.pack(side="top", padx=10, pady=10)
        


        # image to display in the guide window
        guide_img = ctk.CTkImage(light_image=Image.open("Tools/English_guide_image.png"),size=(500, 320))
        guide_label = ctk.CTkLabel(guide_frame, image =guide_img, text=" ")
        guide_label.pack()
        


        # Camera variables
        self.cap = None
        self.running = False
        self.thread = None
        self.current_frame = None  # To store the current frame

    def change_language(self, language):
        """Change the language of the application."""
        # This is a placeholder for actual language change logic.
        # You would typically load different text resources based on the selected language.
        if language == "Français":
            self.result_label.configure(text="Valeur: ")
            self.camera_btn.configure(text="Démarrer la caméra")
            self.capture_btn.configure(text="Capturer")
            self.file_btn.configure(text="Ouvrir l'image")
            self.appearance_mode.set("Mode d'apparence")
            self.language_frame_label.configure(text="Mode de langue:")
            self.appearance_frame_label.configure(text="Mode d'apparence:")
            self.settings_label = ctk.CTkLabel(self.settings_label_frame,text="Paramètres", font=("Arial", 16))

        else:
            self.result_label.configure(text="Value: ")
            self.camera_btn.configure(text="Start Camera")
            self.capture_btn.configure(text="Capture")
            self.file_btn.configure(text="Open Image")

    def change_appearance_mode(self, mode):
        """Change the appearance mode of the application."""
        ctk.set_appearance_mode(mode)


    def open_file(self):
        """Open a dialog to select an image."""
        # Open the file dialog for image files
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            # Read the image with OpenCV
            img = cv2.imread(file_path)
            if img is not None:
                # Display the image in the interface
                self.display_image(img)
                # Start processing
                self.process_image(img)
    def show_guide(self,img):
        pass

    def show_help(self):
        pass

    def zoom_image(self):
        """Zoom in on the current image."""
        if self.current_frame is not None:
            # Resize the image to double its size
            zoomed_img = cv2.resize(self.current_frame, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            self.display_image(zoomed_img)

    def display_image(self, img):
        """Display an image in the video label."""
        # Convert BGR (OpenCV) to RGB (PIL)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Convert to PIL Image
        pil_img = Image.fromarray(img_rgb)
        # Create a CustomTkinter image
        ctk_image = ctk.CTkImage(light_image=pil_img, size=(440, 280))
        # Update the label with the new image
        self.video_label.configure(image=ctk_image)
        self.video_label.image = ctk_image  # Keep a reference

    def start_camera(self):
        """Start the camera stream in a separate thread."""
        if self.running:
            return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Unable to open the camera.")
            return
        self.running = True
        self.capture_btn.configure(state="normal")
        self.camera_btn.configure(text="Stop Camera", command=self.stop_camera)
        self.thread = threading.Thread(target=self.update_camera)
        self.thread.daemon = True
        self.thread.start()

    def stop_camera(self):
        """Stop the camera stream."""
        self.running = False
        if self.cap:
            self.cap.release()
        self.camera_btn.configure(text="Start Camera", command=self.start_camera)
        self.capture_btn.configure(state="disabled")

    def update_camera(self):
        """Video stream update loop."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()  # Keep a copy for capture
                self.display_image(frame)

    def capture_image(self):
        """Capture the current camera image for processing."""
        if self.current_frame is not None:
            self.process_image(self.current_frame)

    def process_image(self, img):
        """
        Main function to analyze the resistor image.
        (To be implemented with the steps below)
        """
        # 1. Image preprocessing
        processed_img = self.preprocess_image(img)

        # 2. Detect and analyze the color bands
        bands = self.detect_color_bands(processed_img)

        # 3. Calculate the resistor value
        if bands:
            resistance_value = self.calculate_resistance(bands)
            self.result_label.configure(text=f"Value: {resistance_value} Ω")
        else:
            self.result_label.configure(text="Value: Not detected")

    def preprocess_image(self, img):
        """Clean the image to make detection easier."""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply a filter to reduce noise while preserving edges
        blurred = cv2.bilateralFilter(gray, 9, 75, 75)
        # Adaptive thresholding to separate the bands from the background
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        return thresh

    def detect_color_bands(self, processed_img):
        """
        Detect the color bands and return a list of their colors.
        This is the hardest part to implement properly.
        """
        # Step 1: Find the contour of the resistor
        # Step 2: Isolate the resistor and straighten it
        # Step 3: For each band, extract its color
        # Step 4: Map the color to a value (black=0, brown=1, etc.)

        # Very simplified example (to be replaced by real logic)
        # For now, return a fictitious list
        return ["brown", "black", "red", "gold"]

    def calculate_resistance(self, bands):
        """Calculate the resistor value from the colors of the bands."""
        # Color-to-digit mapping dictionary
        color_map = {
            "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
            "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
        }
        # For a 4-band resistor: 1st digit, 2nd digit, multiplier, tolerance
        if len(bands) >= 3:
            val1 = color_map.get(bands[0], 0)
            val2 = color_map.get(bands[1], 0)
            multiplier = 10 ** color_map.get(bands[2], 0)
            resistance = (val1 * 10 + val2) * multiplier
            return resistance
        return "Error"


if __name__ == "__main__":
    app = OhmegaResistorApp()
    app.mainloop()