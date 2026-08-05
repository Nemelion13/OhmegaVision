import customtkinter as ctk
from PIL import Image
import cv2
import threading
from tkinter import filedialog  # For file selection
from ultralytics import YOLO


class ResistorColoredBandsModel():
    def __init__(self):

        self.model = YOLO("runs/detect/yolo26n_resistor_color_bands_detection/weights/best.pt")  # Load the trained YOLOv8 model
        
RCBM = ResistorColoredBandsModel()
class OhmegaResistorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ohmega Vision Resistor Reader")
        self.geometry("850x600")
        self.iconbitmap("Tools/OhmegaVision.ico")  # Set your icon path here

        # Bottom fram for author and version
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)
        self.author_label = ctk.CTkLabel(self.bottom_frame, text="Developed by nemelion13 - All rights reserved © 2026")
        self.author_label.pack(side="left", padx=10)
        self.version_label = ctk.CTkLabel(self.bottom_frame, text="Version 1.0")
        self.version_label.pack(side="right", padx=10)
        self.contact_label = ctk.CTkLabel(self.bottom_frame, text="Contact: nemelion13@gmail.com")
        self.contact_label.pack(side="right", padx=10)

        #Frame for video and zoom button
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Confidence threshold control on the left side of the video frame
        self.confidence_frame = ctk.CTkFrame(self.video_frame)
        self.confidence_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)
        self.confidence_label = ctk.CTkLabel(self.confidence_frame, text="Confidence")
        self.confidence_label.pack(side="top", padx=10, pady=(10, 5))
        self.confidence_threshold = 0.28
        self.confidence_slider = ctk.CTkSlider(
            self.confidence_frame,
            from_=0.05,
            to=0.95,
            number_of_steps=90,
            orientation="vertical",
            command=self.update_confidence_threshold
        )
        self.confidence_slider.set(self.confidence_threshold)
        self.confidence_slider.pack(side="top", fill="y", padx=10, pady=(5, 0))
        self.confidence_value_label = ctk.CTkLabel(self.confidence_frame, text=f"{self.confidence_threshold:.2f}")
        self.confidence_value_label.pack(side="top", pady=(5, 10))

        # Label to display the image or video stream
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(side="left", padx=10, pady=10)

        

        # Label to display the result
        self.result_frame = ctk.CTkFrame(self.video_frame)
        self.result_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.result_label = ctk.CTkLabel(self.result_frame, text="Value: ", font=("Arial", 20))
        self.result_label.pack(pady=10)




        # Frame for the buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side="left",fill= "y",padx=10, pady=10)

        # Frame for the camera and capture buttons
        self.camera_frame = ctk.CTkFrame(self.button_frame)
        self.camera_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.camera_label_frame = ctk.CTkFrame(self.camera_frame)
        self.camera_label_frame.pack(side="top", fill="x", padx=10,pady=10)
        camera_img = ctk.CTkImage(light_image=Image.open("Tools/Camera_image.png"), size=(20, 20))
        camera_icon = ctk.CTkLabel(self.camera_label_frame, image=camera_img, text="")
        camera_icon.pack(side="left", padx=5)
        self.camera_label = ctk.CTkLabel(self.camera_label_frame, text="Camera Control", font=("Arial", 16))
        self.camera_label.pack(side="left", padx=5)


        # Button container for camera controls
        self.camera_button_frame = ctk.CTkFrame(self.camera_frame)
        self.camera_button_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.camera_btn = ctk.CTkButton(self.camera_button_frame, text="Start Camera", command=self.start_camera)
        self.camera_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Button to capture an image from the camera
        self.capture_btn = ctk.CTkButton(self.camera_button_frame, text="Capture", command=self.capture_image, state="disabled")
        self.capture_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Button to open a file
        self.file_btn = ctk.CTkButton(self.camera_button_frame, text="Open Image", command=self.open_file)
        self.file_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Button to clean the video/image display
        self.clean_btn = ctk.CTkButton(self.camera_button_frame, text="Clean", command=self.clean_display)
        self.clean_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.camera_button_frame.grid_columnconfigure(0, weight=1)
        self.camera_button_frame.grid_columnconfigure(1, weight=1)

        #zoom button
        self.zoom_frame = ctk.CTkFrame(self.camera_frame)
        self.zoom_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.zoom_label = ctk.CTkLabel(self.zoom_frame, text="Zoom Camera:")
        self.zoom_label.pack(side="left", padx=10)
        self.zoom_btn = ctk.CTkSlider(self.zoom_frame, from_=1.0, to=8.0, number_of_steps=70, command=self.zoom_video)
        self.zoom_btn.set(1.0)
        self.zoom_btn.pack(side="left", padx=10)
        self.zoom_value_label = ctk.CTkLabel(self.zoom_frame, text="1.0x")
        self.zoom_value_label.pack(side="left", padx=10)

        

        #Frame for settings and help
        settings_frame = ctk.CTkFrame(self.button_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.settings_frame_label = ctk.CTkFrame(settings_frame)
        self.settings_frame_label.pack(side="top", fill="x", padx=10, pady=10)

        settings_img = ctk.CTkImage(light_image=Image.open("Tools/Settings_image.png"), size=(20, 20))
        settings_icon = ctk.CTkLabel(self.settings_frame_label, image=settings_img, text="")
        settings_icon.pack(side="left", padx=5)
        self.settings_label = ctk.CTkLabel(self.settings_frame_label,text="Settings", font=("Arial", 16))
        self.settings_label.pack(side="left", padx=5)


        # Combo box for appearance mode selection
        appearance_frame = ctk.CTkFrame(settings_frame)
        appearance_frame.pack(side="top", fill="x", pady=10, padx=10)
        self.appearance_frame_label = ctk.CTkLabel(appearance_frame, text="Appearance Mode:")
        self.appearance_frame_label.pack(side="left", padx=10)
        self.appearance_mode = ctk.CTkComboBox(appearance_frame, values=["Light", "Dark"], command=self.change_appearance_mode)
        self.appearance_mode.set("Light")
        self.appearance_mode.pack(pady=10)

        # combo box for language
        language_frame = ctk.CTkFrame(settings_frame)
        language_frame.pack(side="top", fill="x", pady=10, padx=10)
        self.language_frame_label = ctk.CTkLabel(language_frame, text="Language Mode:")
        self.language_frame_label.pack(side="left", padx=10)
        self.language_box = ctk.CTkComboBox(language_frame, values=["English", "Français"], command=self.change_language)
        self.language_box.set("English")
        self.language_box.pack(pady=10)

        # combo box for camera index
        camera_index_frame = ctk.CTkFrame(settings_frame)
        camera_index_frame.pack(side="top",fill="x",pady=10,padx=10)
        self.camera_index_frame_label = ctk.CTkLabel(camera_index_frame,text="Camera Index:")
        self.camera_index_frame_label.pack(side="left",padx=10)
        self.camera_index_box = ctk.CTkComboBox(camera_index_frame,values=[f"{i}" for i in range(11)]) 
        self.camera_index_box.set("0")
        self.camera_index_box.pack(pady=10)  
        

        # Frame for help and about
        help_frame = ctk.CTkFrame(self.button_frame)
        help_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_label_frame = ctk.CTkFrame(help_frame)
        help_label_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_img = ctk.CTkImage(light_image=Image.open("Tools/Help_Support_image.png"), size=(20, 20))
        help_icon = ctk.CTkLabel(help_label_frame, image=help_img, text="")
        help_icon.pack(side="left", padx=5)
        self.help_label = ctk.CTkLabel(help_label_frame, text="Help & Support", font=("Arial", 16))
        self.help_label.pack(side="left", padx=5)

        # Frame for help and about buttons
        help_buttons_frame = ctk.CTkFrame(help_frame)
        help_buttons_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.help_btn = ctk.CTkButton(help_buttons_frame, text="Help", command=lambda: self.open_top_window("Help", self.language_box.get()), fg_color="red")
        self.help_btn.pack(side="left", padx=10, pady=10)
        self.guide_btn = ctk.CTkButton(help_buttons_frame, text="Guide", command=lambda: self.open_top_window("Guide", self.language_box.get()), fg_color="red")
        self.guide_btn.pack(side="left", padx=10, pady=10)
        #about_btn = ctk.CTkButton(help_buttons_frame, text="About", command=self.show_about)
        #about_btn.pack(side="top", padx=10, pady=10)


        # Camera variables
        self.cap = None
        self.running = False
        self.thread = None
        self.current_frame = None  # To store the current frame
        self.zoom_factor = 1.0

    def update_confidence_threshold(self, value):
        """Update the confidence threshold and immediately reprocess the current frame."""
        self.confidence_threshold = float(value)
        self.confidence_value_label.configure(text=f"{self.confidence_threshold:.2f}")

        if self.current_frame is not None:
            self.process_image(self.current_frame)

    def open_top_window(self, title,language):
        """Open a new top-level window with the given title and content."""
        top_window = ctk.CTkToplevel(self)
        top_window.title(title)
        top_window.geometry("600x400")
        if language == "Français":
            if title == "Help":
                content = "Aide: \n\n1. Démarrez la caméra ou ouvrez une image.\n2. Capturez l'image du composant.\n3. L'application analysera l'image et affichera la valeur de la résistance."
                help_label = ctk.CTkLabel(top_window, text=content, font=("Arial", 14))
                help_label.pack(pady=20, padx=20)
            elif title == "Guide":
                # image to display in the guide window
                guide_img = ctk.CTkImage(light_image=Image.open("Tools/French_guide_image.png"),size=(500, 320))
                guide_label = ctk.CTkLabel(top_window, image =guide_img, text=" ")
                guide_label.pack()
                content = "Guide: \n\n1. Ouvrez l'application.\n2. Démarrez la caméra ou ouvrez une image.\n3. Capturez l'image du composant.\n4. L'application analysera l'image et affichera la valeur de la résistance."
        else:
            if title == "Help":
                content = "Help: \n\n1. Start the camera or open an image.\n2. Capture the component's image.\n3. The application will analyze the image and display the resistor value."
                help_label = ctk.CTkLabel(top_window, text=content, font=("Arial", 14))
                help_label.pack(pady=20, padx=20)
            elif title == "Guide":
                # image to display in the guide window
                guide_img = ctk.CTkImage(light_image=Image.open("Tools/English_guide_image.png"),size=(500, 320))
                guide_label = ctk.CTkLabel(top_window, image =guide_img, text=" ")
                guide_label.pack()
                content = "Guide: \n\n1. Open the application.\n2. Start the camera or open an image.\n3. Capture the component's image.\n4. The application will analyze the image and display the resistor value."
    # Language change function
    translations = {
        "English": {
            "Value": "Value: ",
            "Start Camera": "Start Camera",
            "Capture": "Capture",
            "Open Image": "Open Image",
            "Appearance Mode": "Appearance Mode:",
            "Language Mode": "Language Mode:",
            "Settings": "Settings",
            "Help & Support": "Help & Support",
            "Camera Control" : "Camera Control",
            "Help": "Help", 
            "Clean" :"Clean",
            # colors
            "black": "Black",
            "brown": "Brown",
            "red": "Red",
            "orange": "Orange",
            "yellow": "Yellow",
            "green": "Green",
            "blue": "Blue",
            "violet": "Violet",
            "gray": "Gray",
            "white": "White",
            "gold": "Gold",
            "silver": "Silver"
        },
        "Français": {
            "Value": "Valeur: ",
            "Start Camera": "Démarrer la caméra",
            "Capture": "Capturer",
            "Open Image": "Ouvrir l'image",
            "Appearance Mode": "Mode d'apparence:",
            "Language Mode": "Mode de langue:",
            "Settings": "Paramètres",
            "Help & Support": "Aide et Assistance",
            "Camera Control" : "Contrôle de la caméra",
            "Help": "Aide",
            "Clean" : "Nettoyer",
            # colors in French
            "black": "Noir",
            "brown": "Marron",
            "red": "Rouge",
            "orange": "Orange",
            "yellow": "Jaune",
            "green": "Vert",
            "blue": "Bleu",
            "violet": "Violet",
            "gray": "Gris",
            "white": "Blanc",
            "gold": "Or",
            "silver": "Argent"
        }
    }

    def change_language(self, language):
        """Change the language of the application."""
        if language in self.translations:
            self.result_label.configure(text=self.translations[language]["Value"])
            self.camera_btn.configure(text=self.translations[language]["Start Camera"])
            self.capture_btn.configure(text=self.translations[language]["Capture"])
            self.file_btn.configure(text=self.translations[language]["Open Image"])
            self.appearance_frame_label.configure(text=self.translations[language]["Appearance Mode"])
            self.language_frame_label.configure(text=self.translations[language]["Language Mode"])
            self.settings_label.configure(text=self.translations[language]["Settings"])
            self.help_label.configure(text=self.translations[language]["Help & Support"])
            self.camera_label.configure(text=self.translations[language]["Camera Control"])
            self.help_btn.configure(text=self.translations[language]["Help"])
            self.clean_btn.configure(text=self.translations[language]["Clean"])
            # Update other labels and buttons as needed
            

    def change_appearance_mode(self, mode):
        """Change the appearance mode of the application."""
        ctk.set_appearance_mode(mode)
    
    #def change_camera_index(self,index):
        #"""Change the index of the camera for cv2.VideoCapture(index)"""
        


    def open_file(self):
        """Open a dialog to select an image."""
        # Open the file dialog for image files
        file_path = filedialog.askopenfilename(
            title="Select an image of a resistor",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            # Read the image with OpenCV
            img = cv2.imread(file_path)
           
            if img is not None:
                self.current_frame = img.copy()
                # Start processing
                self.process_image(self.current_frame)
                
    def show_guide(self,img):
        pass

    def show_help(self):
        pass

    def zoom_video(self, value):
        """Update the current zoom factor from the slider."""
        self.zoom_factor = max(1.0, float(value))
        if hasattr(self, 'zoom_value_label'):
            self.zoom_value_label.configure(text=f"{self.zoom_factor:.1f}x")

    def display_image(self, img):
        """Display an image in the video label."""
        if self.zoom_factor != 1.0:
            h, w = img.shape[:2]
            new_h = int(h / self.zoom_factor)
            new_w = int(w / self.zoom_factor)
            start_y = max(0, (h - new_h) // 2)
            start_x = max(0, (w - new_w) // 2)
            cropped = img[start_y:start_y + new_h, start_x:start_x + new_w]
            img = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
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
        camera_index = int(self.camera_index_box.get())
        self.cap = cv2.VideoCapture(camera_index,cv2.CAP_DSHOW)
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
            self.cap = None
        self.camera_btn.configure(text="Start Camera", command=self.start_camera)
        self.capture_btn.configure(state="disabled")

    def clean_display(self):
        """Stop camera and clear the video/image display."""
        if self.running:
            self.stop_camera()
        self.current_frame = None
        self.video_label.configure(image="", text="")
        self.video_label.image = None
        self.zoom_factor = 1.0
        self.zoom_btn.set(1.0)
        self.zoom_value_label.configure(text="1.0x")

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
        # Step 1 : Process the image to enhance detection (e.g., resizing, filtering)
        results = RCBM.model(img, conf=self.confidence_threshold)  # Run the YOLO model on the image
        result = results[0]  # Get the first result

        # Step 2 : Get the annotated image with bounding boxes
        annotated_img = result.plot()  # Get the annotated image with bounding boxes
        self.display_image(annotated_img)  # Display the annotated image

        # Step 3 : Extract the detected color bands from the results
        boxes = result.boxes # Get bounding boxes
        detected_bands = []
        for box in boxes:
            cls_id = int(box.cls[0].item())  # Get class ID
            color_name = RCBM.model.names[cls_id].lower()  # Get color name from model

            if color_name !='resistor':
                x_min = box.xyxy[0][0].item()
                detected_bands.append((x_min,color_name))

        # Step 4 : Sort the detected bands based on their x-coordinates (left to right)
        detected_bands.sort(key=lambda x: x[0])
        print(detected_bands) #for debugging
        sorted_bands = [band[1] for band in detected_bands]  # Sort by x-coordinate

        # Step 5 : Calculate the resistance value based on the detected bands
        if sorted_bands:
            resistance_value = self.calculate_resistance(sorted_bands)
            self.result_label.configure(text=f"Value: {resistance_value} Ω")
        else:
            self.result_label.configure(text="Value: Not detected") 

    

    #def preprocess_image(self, img):
       # """Clean the image to make detection easier."""
        # Convert to grayscale
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply a filter to reduce noise while preserving edges
        #blurred = cv2.bilateralFilter(gray, 9, 75, 75)
        # Adaptive thresholding to separate the bands from the background
        #thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        #return thresh

  

    def calculate_resistance(self, bands):
        """Calculate the resistor value from the colors of the bands."""
        
        print("Initiale bands:",bands)

        if bands and bands[0] in ['gold','silver']:
            bands.reverse()
            print("Reversed bands:" ,bands)

        color_values = {
            "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
            "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
        }
        
        multiplier_values = {
            "black": 1, "brown": 10, "red": 100, "orange": 1000, "yellow": 10000,
            "green": 100000, "blue": 1000000, "violet": 10000000, "gray": 100000000, "white": 1000000000,
            "gold": 0.1, "silver": 0.01
        }
        
        tolerance_values = {
            "brown": "±1%", "red": "±2%", "green": "±0.5%", "blue": "±0.25%", "violet": "±0.1%",
            "gray": "±0.05%", "gold": "±5%", "silver": "±10%"
        }

        # if the number of bands is not sufficiente
        if len(bands) < 3:
            return "Error: non-compliant number of bands"

        try:
            # Calculate for four bands (Value 1, Value 2, Multiplier, Tolerance)
            if len(bands) == 3 or len(bands) == 4:
                val = (color_values[bands[0]] * 10) + color_values[bands[1]]
                res = val * multiplier_values.get(bands[2], 1)
                
                # if there is a fourth band it's the tolerance, otherwise we are taking "±20%"
                tol = tolerance_values.get(bands[3], "") if len(bands) == 4 else "±20%"
                
                return f"{self.format_ohms(res)} {tol}"

            # Calculate for 5 bands (Value 1, 2, 3, Multiplier, Tolerance)
            elif len(bands) >= 5:
                val = (color_values[bands[0]] * 100) + (color_values[bands[1]] * 10) + color_values[bands[2]]
                res = val * multiplier_values.get(bands[3], 1)
                tol = tolerance_values.get(bands[4], "")
                return f"{self.format_ohms(res)} {tol}"
                
        except KeyError as e:
            return f"Error : Unexpectited color detected ({e})"

        return "Error"

        
        
    def format_ohms(self,value):
        """Formatt"""
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f} MΩ"
        elif value >= 1_000:
            return f"{value / 1_000:.2f} kΩ"
        else:
            # Enlever les décimales .00 inutiles
            return f"{value:g} Ω"

if __name__ == "__main__":
    app = OhmegaResistorApp()
    app.mainloop()