import customtkinter as ctk
from PIL import Image
import cv2
import threading
import tkinter as tk # Needed for ToolTip
from tkinter import filedialog
from ultralytics import YOLO

# --- TOOLTIP CLASS ---
class ToolTip:
    """Class to create a hover tooltip for any CustomTkinter widget."""
    def __init__(self, widget, text_dict, language_box_ref):
        self.widget = widget
        self.text_dict = text_dict # Dictionary containing translations
        self.language_box = language_box_ref
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        current_lang = self.language_box.get()
        text = self.text_dict.get(current_lang, self.text_dict["English"])
        
        x = self.widget.winfo_rootx() + (self.widget.winfo_width() // 2)
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Determine colors based on appearance mode
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        fg_color = "#ffffff" if ctk.get_appearance_mode() == "Dark" else "#000000"
        
        label = tk.Label(self.tooltip, text=text, justify='left',
                         background=bg_color, foreground=fg_color, 
                         relief='solid', borderwidth=1,
                         font=("Arial", 11, "normal"))
        label.pack(ipadx=6, ipady=4)

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class ResistorColoredBandsModel():
    def __init__(self):
        # Load the trained YOLO model
        self.model = YOLO("runs/detect/yolo26n_resistor_color_bands_detection/weights/best.pt") 
        
RCBM = ResistorColoredBandsModel()


class OhmegaResistorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ohmega Vision Resistor Reader")
        self.geometry("950x700") # Slightly enlarged for the new UI panels
        self.iconbitmap("Tools/OhmegaVision.ico")

        # Bottom fram for author and version
        self.bottom_frame = ctk.CTkFrame(self, height=30, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 5))
        self.author_label = ctk.CTkLabel(self.bottom_frame, text="Developed by nemelion13 - All rights reserved © 2026", font=("Arial", 10))
        self.author_label.pack(side="left", padx=10)
        self.version_label = ctk.CTkLabel(self.bottom_frame, text="Version 1.2", font=("Arial", 10))
        self.version_label.pack(side="right", padx=10)
        self.contact_label = ctk.CTkLabel(self.bottom_frame, text="Contact: nemelion13@gmail.com")
        self.contact_label.pack(side="right", padx=10)

        # -- MAIN CONTAINER  ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="top", fill="both", expand=True)

        # --- TRANSLATIONS DICTIONARY ---
        self.translations = {
            "English": {
                "Value": "Value: ",
                "Start Camera": "Start Camera",
                "Stop Camera": "Stop Camera",
                "Capture": "Analyze Image", 
                "Open Image": "Load Image",
                "Clean" : "Clear Screen",
                "Controls" : "Controls",
                "Theme:": "Theme:",
                "Language:": "Language:",
                "Select Camera:": "Select Camera:",
                "Settings": "Settings",
                "Help & Support": "Help & Support",
                "Help": "How to use", 
                "Guide": "Visual Guide",
                "Sensitivity": "Sensitivity", 
                "Zoom:": "Zoom:",
                "Detected Colors": "Detected Colors",
                "Not detected": "Not detected",
                "Error: Not enough bands": "Error: Not enough bands",
                "tt_start": "Turn on your webcam stream.",
                "tt_capture": "Freeze the stream and calculate the resistance.",
                "tt_open": "Load an image from your computer.",
                "tt_clean": "Stop the camera and clear the results.",
                "tt_zoom": "Adjust the camera zoom level.",
                "tt_theme": "Change between Light and Dark themes.",
                "tt_language": "Select the UI language.",
                "tt_select_camera": "Choose which camera index to use, change if you're using webcam.",
                "tt_sensitivity": "Adjust detection sensitivity (confidence).",
                "tt_help_btn": "Open the help window with usage instructions.",
                "tt_guide_btn": "Open a visual guide image explaining readings.",
                "tt_detected_colors": "Shows colors detected on the resistor.",
                # Colors
                "black": "Black", "brown": "Brown", "red": "Red", "orange": "Orange",
                "yellow": "Yellow", "green": "Green", "blue": "Blue", "purple": "Purple",
                "gray": "Gray", "white": "White", "gold": "Gold", "silver": "Silver",
                # Error messages
                "Error: Unable to open the camera, change the index or verify your device.": "Error: Unable to open the camera, change the index or verify your device."

            },
            "Français": {
                "Value": "Valeur : ",
                "Start Camera": "Allumer Caméra",
                "Stop Camera": "Éteindre Caméra",
                "Capture": "Analyser l'image",
                "Open Image": "Charger Image",
                "Clean" : "Effacer l'écran",
                "Controls" : "Contrôles",
                "Theme:": "Thème :",
                "Language:": "Langue :",
                "Select Camera:": "Choix Caméra :",
                "Settings": "Paramètres",
                "Help & Support": "Aide et Support",
                "Help": "Mode d'emploi", 
                "Guide": "Guide Visuel",
                "Sensitivity": "Sensibilité",
                "Zoom:": "Zoom :",
                "Detected Colors": "Couleurs Détectées",
                "Not detected": "Non détecté",
                "Error: Not enough bands": "Erreur: Pas assez de bandes",
                "tt_start": "Active le flux vidéo de la webcam.",
                "tt_capture": "Gèle l'image et calcule la valeur de la résistance.",
                "tt_open": "Charge une photo depuis l'ordinateur.",
                "tt_clean": "Coupe la caméra et nettoie l'interface.",
                "tt_zoom": "Ajuste le niveau de zoom de la caméra.",
                "tt_theme": "Basculer entre les thèmes Clair et Sombre.",
                "tt_language": "Sélectionnez la langue de l'interface.",
                "tt_select_camera": "Choisissez l'index de la caméra à utiliser,changer si webcam utilisée.",
                "tt_sensitivity": "Ajuste la sensibilité de détection (confiance).",
                "tt_help_btn": "Ouvre la fenêtre d'aide avec les instructions.",
                "tt_guide_btn": "Ouvre un guide visuel expliquant la lecture.",
                "tt_detected_colors": "Affiche les couleurs détectées sur la résistance.",
                # Colors
                "black": "Noir", "brown": "Marron", "red": "Rouge", "orange": "Orange",
                "yellow": "Jaune", "green": "Vert", "blue": "Bleu", "purple": "Violet",
                "gray": "Gris", "white": "Blanc", "gold": "Or", "silver": "Argent",
                # Error messages
                "Error: Unable to open the camera, change the index or verify your device.": "Erreur : Impossible d'ouvrir la caméra, changez l'index ou vérifiez votre appareil."
            }
        }
        
        # Color mapping for UI dots
        self.color_hex_map = {
            "black": "#2c3e50", "brown": "#8B4513", "red": "#e74c3c", 
            "orange": "#e67e22", "yellow": "#f1c40f", "green": "#2ecc71", 
            "blue": "#3498db", "purple": "#9b59b6", "gray": "#95a5a6", 
            "white": "#ffffff", "gold": "#f39c12", "silver": "#bdc3c7"
        }

        # --- LEFT PANEL: CONTROLS & SETTINGS ---
        self.button_frame = ctk.CTkFrame(self.main_container, width=300)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.button_frame.pack_propagate(False)

        # 1. Camera Controls Frame
        self.camera_frame = ctk.CTkFrame(self.button_frame)
        self.camera_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.camera_label_frame = ctk.CTkFrame(self.camera_frame, fg_color="transparent")
        self.camera_label_frame.pack(side="top", fill="x", padx=10, pady=(10,5))
        try:
            camera_img = ctk.CTkImage(light_image=Image.open("Tools/Camera_image.png"), size=(20, 20))
            camera_icon = ctk.CTkLabel(self.camera_label_frame, image=camera_img, text="")
            camera_icon.pack(side="left", padx=5)
        except: pass
        self.camera_label = ctk.CTkLabel(self.camera_label_frame, text="Controls", font=("Arial", 16, "bold"))
        self.camera_label.pack(side="left", padx=5)

        self.camera_button_frame = ctk.CTkFrame(self.camera_frame, fg_color="transparent")
        self.camera_button_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        self.camera_btn = ctk.CTkButton(self.camera_button_frame, text="Start Camera", command=self.start_camera)
        self.camera_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.capture_btn = ctk.CTkButton(self.camera_button_frame, text="Analyze Image", command=self.capture_image, state="disabled")
        self.capture_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.file_btn = ctk.CTkButton(self.camera_button_frame, text="Load Image", command=self.open_file)
        self.file_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.clean_btn = ctk.CTkButton(self.camera_button_frame, text="Clear Screen", command=self.clean_display, fg_color="gray")
        self.clean_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.camera_button_frame.grid_columnconfigure(0, weight=1)
        self.camera_button_frame.grid_columnconfigure(1, weight=1)
        
        # Zoom Slider
        self.zoom_frame = ctk.CTkFrame(self.camera_frame, fg_color="transparent")
        self.zoom_frame.pack(side="top", fill="x", padx=10, pady=(5, 10))
        self.zoom_label = ctk.CTkLabel(self.zoom_frame, text="Zoom:")
        self.zoom_label.pack(side="left", padx=5)
        self.zoom_btn = ctk.CTkSlider(self.zoom_frame, from_=1.0, to=5.0, number_of_steps=40, command=self.zoom_video, width=120)
        self.zoom_btn.set(1.0)
        self.zoom_btn.pack(side="left", padx=5)
        self.zoom_value_label = ctk.CTkLabel(self.zoom_frame, text="1.0x")
        self.zoom_value_label.pack(side="left", padx=5)

        # 2. Settings Frame
        settings_frame = ctk.CTkFrame(self.button_frame)
        settings_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.settings_frame_label = ctk.CTkFrame(settings_frame, fg_color="transparent")
        self.settings_frame_label.pack(side="top", fill="x", padx=10, pady=(10,5))
        try:
            settings_img = ctk.CTkImage(light_image=Image.open("Tools/Settings_image.png"), size=(20, 20))
            settings_icon = ctk.CTkLabel(self.settings_frame_label, image=settings_img, text="")
            settings_icon.pack(side="left", padx=5)
        except: pass
        self.settings_label = ctk.CTkLabel(self.settings_frame_label, text="Settings", font=("Arial", 16, "bold"))
        self.settings_label.pack(side="left", padx=5)

        # Language Box (Put this early so ToolTips can reference it immediately)
        language_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        language_frame.pack(side="top", fill="x", pady=5, padx=10)
        self.language_frame_label = ctk.CTkLabel(language_frame, text="Language:")
        self.language_frame_label.pack(side="left", padx=5)
        self.language_box = ctk.CTkComboBox(language_frame, values=["English", "Français"], command=self.change_language, width=100)
        self.language_box.set("English")
        self.language_box.pack(side="right", padx=5)

        # Appearance Mode
        appearance_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        appearance_frame.pack(side="top", fill="x", pady=5, padx=10)
        self.appearance_frame_label = ctk.CTkLabel(appearance_frame, text="Theme:")
        self.appearance_frame_label.pack(side="left", padx=5)
        self.appearance_mode = ctk.CTkComboBox(appearance_frame, values=["Light", "Dark"], command=self.change_appearance_mode, width=100)
        self.appearance_mode.set("Light")
        self.appearance_mode.pack(side="right", padx=5)

        # Camera Index
        camera_index_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        camera_index_frame.pack(side="top", fill="x", pady=(5, 15), padx=10)
        self.camera_index_frame_label = ctk.CTkLabel(camera_index_frame, text="Select Camera:")
        self.camera_index_frame_label.pack(side="left", padx=5)
        self.camera_index_box = ctk.CTkComboBox(camera_index_frame, values=[f"{i}" for i in range(5)], width=60) 
        self.camera_index_box.set("0")
        self.camera_index_box.pack(side="right", padx=5)  

        # 3. Help Frame
        help_frame = ctk.CTkFrame(self.button_frame)
        help_frame.pack(side="top", fill="x", padx=10, pady=10)
        help_label_frame = ctk.CTkFrame(help_frame, fg_color="transparent")
        help_label_frame.pack(side="top", fill="x", padx=10, pady=(10,5))
        try:
            help_img = ctk.CTkImage(light_image=Image.open("Tools/Help_Support_image.png"), size=(20, 20))
            help_icon = ctk.CTkLabel(help_label_frame, image=help_img, text="")
            help_icon.pack(side="left", padx=5)
        except: pass
        self.help_label = ctk.CTkLabel(help_label_frame, text="Help & Support", font=("Arial", 16, "bold"))
        self.help_label.pack(side="left", padx=5)

        help_buttons_frame = ctk.CTkFrame(help_frame, fg_color="transparent")
        help_buttons_frame.pack(side="top", fill="x", padx=5, pady=(0, 10))
        self.help_btn = ctk.CTkButton(help_buttons_frame, text="How to use", command=lambda: self.open_top_window("Help"), fg_color="#3498db")
        self.help_btn.pack(side="left", expand=True, padx=5)
        self.guide_btn = ctk.CTkButton(help_buttons_frame, text="Visual Guide", command=lambda: self.open_top_window("Guide"), fg_color="#9b59b6")
        self.guide_btn.pack(side="right", expand=True, padx=5)


        # --- RIGHT PANEL: VIDEO & RESULTS ---
        self.video_frame = ctk.CTkFrame(self.main_container)
        self.video_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sensitivity (Confidence) Slider - Left of video frame
        self.confidence_frame = ctk.CTkFrame(self.video_frame)
        self.confidence_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.confidence_label = ctk.CTkLabel(self.confidence_frame, text="Sensitivity", font=("Arial", 12, "bold"))
        self.confidence_label.pack(side="top", padx=10, pady=(15, 5))
        
        self.confidence_threshold = 0.4
        self.confidence_slider = ctk.CTkSlider(
            self.confidence_frame, from_=0.05, to=0.95, number_of_steps=90, 
            orientation="vertical", command=self.update_confidence_threshold
        )
        self.confidence_slider.set(self.confidence_threshold)
        self.confidence_slider.pack(side="top", fill="y", expand=True, padx=10, pady=10)
        
        self.confidence_value_label = ctk.CTkLabel(self.confidence_frame, text=f"{self.confidence_threshold:.2f}")
        self.confidence_value_label.pack(side="bottom", pady=(5, 15))
# Main Displaying Frame (Center)
        self.displaying_frame = ctk.CTkFrame(self.video_frame)
        self.displaying_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=10)
        
        self.video_label = ctk.CTkLabel(self.displaying_frame, text="")
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.result_frame = ctk.CTkFrame(self.displaying_frame, height=60)
        self.result_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.result_label = ctk.CTkLabel(self.result_frame, text="Value: ", font=("Arial", 22, "bold"))
        self.result_label.pack(pady=10)

        # Colours Detected Frame (Right)
        self.colors_detected_frame = ctk.CTkFrame(self.video_frame, width=160)
        self.colors_detected_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)
        self.colors_detected_frame.pack_propagate(False) # Keep width fixed
        
        self.colors_title = ctk.CTkLabel(self.colors_detected_frame, text="Detected Colors", font=("Arial", 14, "bold"))
        self.colors_title.pack(side="top", pady=(15, 10))
        
        self.bands_display_container = ctk.CTkFrame(self.colors_detected_frame, fg_color="transparent")
        self.bands_display_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Attach Tooltips now that language_box exists
        ToolTip(self.camera_btn, {"English": self.translations["English"]["tt_start"], "Français": self.translations["Français"]["tt_start"]}, self.language_box)
        ToolTip(self.capture_btn, {"English": self.translations["English"]["tt_capture"], "Français": self.translations["Français"]["tt_capture"]}, self.language_box)
        ToolTip(self.file_btn, {"English": self.translations["English"]["tt_open"], "Français": self.translations["Français"]["tt_open"]}, self.language_box)
        ToolTip(self.clean_btn, {"English": self.translations["English"]["tt_clean"], "Français": self.translations["Français"]["tt_clean"]}, self.language_box)
        # Additional ToolTips for other controls
        ToolTip(self.zoom_btn, {"English": self.translations["English"]["tt_zoom"], "Français": self.translations["Français"]["tt_zoom"]}, self.language_box)
        ToolTip(self.appearance_mode, {"English": self.translations["English"]["tt_theme"], "Français": self.translations["Français"]["tt_theme"]}, self.language_box)
        ToolTip(self.language_box, {"English": self.translations["English"]["tt_language"], "Français": self.translations["Français"]["tt_language"]}, self.language_box)
        ToolTip(self.camera_index_box, {"English": self.translations["English"]["tt_select_camera"], "Français": self.translations["Français"]["tt_select_camera"]}, self.language_box)
        ToolTip(self.confidence_slider, {"English": self.translations["English"]["tt_sensitivity"], "Français": self.translations["Français"]["tt_sensitivity"]}, self.language_box)
        ToolTip(self.help_btn, {"English": self.translations["English"]["tt_help_btn"], "Français": self.translations["Français"]["tt_help_btn"]}, self.language_box)
        ToolTip(self.guide_btn, {"English": self.translations["English"]["tt_guide_btn"], "Français": self.translations["Français"]["tt_guide_btn"]}, self.language_box)
        ToolTip(self.colors_title, {"English": self.translations["English"]["tt_detected_colors"], "Français": self.translations["Français"]["tt_detected_colors"]}, self.language_box)

        

        


       

        # Variables
        self.cap = None
        self.running = False
        self.thread = None
        self.current_frame = None
        self.zoom_factor = 1.0


    def update_confidence_threshold(self, value):
        """Update confidence dynamically."""
        self.confidence_threshold = float(value)
        self.confidence_value_label.configure(text=f"{self.confidence_threshold:.2f}")
        if self.current_frame is not None and not self.running:
            self.process_image(self.current_frame)

    def open_top_window(self, window_type):
        """Open a beautiful top-level window for Help or Guide."""
        top_window = ctk.CTkToplevel(self)
        top_window.geometry("600x450")
        current_lang = self.language_box.get()
        top_window.focus_force()
        
        if window_type == "Help":
            top_window.title(self.translations[current_lang]["Help"])
            
            content_en = (
                "Welcome to Ohmega Vision!\n\n"
                "1. Load an Image: Click 'Load Image' to scan an existing photo of a resistor.\n"
                "2. Use Webcam: Click 'Start Camera', hold your resistor in front of the lens, "
                "adjust the zoom, and click 'Analyze Image'.\n"
                "3. Sensitivity: If bands are missing, lower the Sensitivity slider. If there is too much noise, increase it.\n"
                "4. Reading Direction: The app automatically detects the tolerance band (Gold/Silver) to read the resistance in the correct order!"
            )
            content_fr = (
                "Bienvenue dans Ohmega Vision !\n\n"
                "1. Charger une image : Cliquez sur 'Charger Image' pour scanner une photo de résistance.\n"
                "2. Utiliser la Webcam : Cliquez sur 'Allumer Caméra', placez votre composant devant l'objectif, "
                "ajustez le zoom, puis cliquez sur 'Analyser l'image'.\n"
                "3. Sensibilité : S'il manque des anneaux, baissez le curseur de Sensibilité. S'il y a du bruit visuel, montez-le.\n"
                "4. Sens de lecture : L'application détecte automatiquement l'anneau de tolérance (Or/Argent) pour lire le code dans le bon sens !"
            )
            
            textbox = ctk.CTkTextbox(top_window, font=("Arial", 14), wrap="word")
            textbox.pack(fill="both", expand=True, padx=20, pady=20)
            textbox.insert("0.0", content_fr if current_lang == "Français" else content_en)
            textbox.configure(state="disabled") # Read-only
            
        elif window_type == "Guide":
            top_window.title(self.translations[current_lang]["Guide"])
            try:
                img_path = "Tools/French_guide_image.png" if current_lang == "Français" else "Tools/English_guide_image.png"
                guide_img = ctk.CTkImage(light_image=Image.open(img_path), size=(550, 400))
                guide_label = ctk.CTkLabel(top_window, image=guide_img, text="")
                guide_label.pack(padx=10, pady=10)
            except:
                ctk.CTkLabel(top_window, text="Guide image not found in Tools/").pack(pady=50)

    def change_language(self, language):
        """Update all UI text dynamically."""
        if language in self.translations:
            trans = self.translations[language]
            
            # Static Labels
            self.result_label.configure(text=trans["Value"])
            self.camera_label.configure(text=trans["Controls"])
            self.settings_label.configure(text=trans["Settings"])
            self.help_label.configure(text=trans["Help & Support"])
            self.appearance_frame_label.configure(text=trans["Theme:"])
            self.language_frame_label.configure(text=trans["Language:"])
            self.camera_index_frame_label.configure(text=trans["Select Camera:"])
            self.zoom_label.configure(text=trans["Zoom:"])
            self.confidence_label.configure(text=trans["Sensitivity"])
            self.colors_title.configure(text=trans["Detected Colors"])
            
            
            # Buttons
            if not self.running:
                self.camera_btn.configure(text=trans["Start Camera"])
            else:
                self.camera_btn.configure(text=trans["Stop Camera"])
                
            self.capture_btn.configure(text=trans["Capture"])
            self.file_btn.configure(text=trans["Open Image"])
            self.clean_btn.configure(text=trans["Clean"])
            self.help_btn.configure(text=trans["Help"])
            self.guide_btn.configure(text=trans["Guide"])

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an image of a resistor",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            img = cv2.imread(file_path)
            if img is not None:
                self.clean_display()
                self.current_frame = img.copy()
                self.process_image(self.current_frame)

    def zoom_video(self, value):
        self.zoom_factor = max(1.0, float(value))
        if hasattr(self, 'zoom_value_label'):
            self.zoom_value_label.configure(text=f"{self.zoom_factor:.1f}x")

    def display_image(self, img):
        if self.zoom_factor != 1.0:
            h, w = img.shape[:2]
            new_h = int(h / self.zoom_factor)
            new_w = int(w / self.zoom_factor)
            start_y = max(0, (h - new_h) // 2)
            start_x = max(0, (w - new_w) // 2)
            cropped = img[start_y:start_y + new_h, start_x:start_x + new_w]
            img = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Calculate dynamic size based on displaying_frame
        frame_w = self.displaying_frame.winfo_width() - 20
        frame_h = self.displaying_frame.winfo_height() - 90 # leaving room for result label
        
        # Fallback size before window is fully rendered
        if frame_w < 100: frame_w, frame_h = 500, 350 
        
        # Keep aspect ratio
        img_ratio = pil_img.width / pil_img.height
        frame_ratio = frame_w / frame_h
        
        if img_ratio > frame_ratio:
            final_w = frame_w
            final_h = int(frame_w / img_ratio)
        else:
            final_h = frame_h
            final_w = int(frame_h * img_ratio)

        ctk_image = ctk.CTkImage(light_image=pil_img, size=(final_w, final_h))
        self.video_label.configure(image=ctk_image)
        self.video_label.image = ctk_image

    def start_camera(self):
        if self.running: return
        camera_index = int(self.camera_index_box.get())
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("Error: Unable to open the camera.")
            # Error message to user
            current_lang = self.language_box.get()
            error_msg = self.translations[current_lang].get("Error: Unable to open the camera, change the index or verify your device.", "Error: Unable to open the camera, change the index or verify your device.")
            # top level window for error
            error_window = ctk.CTkToplevel(self)
            error_window.title("Error")
            error_window.geometry("400x150")
            error_label = ctk.CTkLabel(error_window, text=error_msg, font=("Arial", 14), wraplength=380)
            error_label.pack(expand=True, fill="both", padx=20, pady=20)
            
            return
            
        self.running = True
        self.capture_btn.configure(state="normal")
        
        current_lang = self.language_box.get()
        self.camera_btn.configure(text=self.translations[current_lang]["Stop Camera"], command=self.stop_camera)
        
        self.thread = threading.Thread(target=self.update_camera)
        self.thread.daemon = True
        self.thread.start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
            
        current_lang = self.language_box.get()
        self.camera_btn.configure(text=self.translations[current_lang]["Start Camera"], command=self.start_camera)
        self.capture_btn.configure(state="disabled")

    def clean_display(self):
        if self.running:
            self.stop_camera()
        self.current_frame = None
        self.video_label.configure(image="", text="")
        self.video_label.image = None
        
        current_lang = self.language_box.get()
        self.result_label.configure(text=self.translations[current_lang]["Value"])
        
        # Clear detected colors panel
        for widget in self.bands_display_container.winfo_children():
            widget.destroy()

    def update_camera(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()
                self.display_image(frame)

    def capture_image(self):
        if self.current_frame is not None:
            if self.running: self.stop_camera() # Freeze frame logic
            self.process_image(self.current_frame)

    def update_colors_ui(self, bands_list):
        """Draw the colors list in the right panel."""
        # Clean previous colors
        for widget in self.bands_display_container.winfo_children():
            widget.destroy()
            
        current_lang = self.language_box.get()
        
        for band in bands_list:
            row_frame = ctk.CTkFrame(self.bands_display_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=8, padx=5)
            
            # Draw the circle using Unicode char
            hex_color = self.color_hex_map.get(band, "#000000")
            # If the background is light and the color is white, add a border trick or use gray
            if hex_color == "#ffffff" and ctk.get_appearance_mode() == "Light":
                hex_color = "#dcdde1" # slightly off-white to be visible
                
            circle = ctk.CTkLabel(row_frame, text="⬤", text_color=hex_color, font=("Arial", 22))
            circle.pack(side="left", padx=(5, 10))
            
            # Translated color name
            translated_name = self.translations[current_lang].get(band, band).capitalize()
            name_label = ctk.CTkLabel(row_frame, text=translated_name, font=("Arial", 14))
            name_label.pack(side="left")

    def process_image(self, img):
        results = RCBM.model(img, conf=self.confidence_threshold, iou=0.2, agnostic_nms=True)
        result = results[0]

        annotated_img = result.plot()
        self.display_image(annotated_img)

        boxes = result.boxes
        detected_bands = []
        for box in boxes:
            cls_id = int(box.cls[0].item())
            class_name = RCBM.model.names[cls_id].lower()

            if class_name!='resistor':
                x_min = box.xyxy[0][0].item()
                conf = box.conf[0].item()
                detected_bands.append((x_min, class_name,conf))

        # Spatial sorting and filtering
        detected_bands.sort(key=lambda x: x[0]); print("Detected bands (sorted):", detected_bands)
        
        filtered_bands = []
        if detected_bands:
            #group initialization
            current_group = [detected_bands[0]]
            pixel_threshold = 15

            # Analyze the lefting bands detected
            for i in range(1,len(detected_bands)):
                x_min, color_name, conf = detected_bands[i]
                last_x = current_group[-1][0]

                if abs(x_min-last_x) <= pixel_threshold:
                    current_group.append((x_min,color_name,conf))
                    print(f"Current groupe{i}:{current_group}")
                else:
                    #gap is too large : it's a new band of colour
                    best_band = max(current_group,key=lambda item: item[2])
                    filtered_bands.append(best_band[1])

                    #start a new group
                    current_group = [(x_min,color_name,conf)]
                    print(f"Current groupe{i}:{current_group}")
                
            best_band = max(current_group, key= lambda item: item[2])
            filtered_bands.append(best_band[1])

        sorted_bands = filtered_bands 
        print("Filtered bands (after thresholding):", sorted_bands)
        
        # --- LOGIC REVERSAL BEFORE UI UPDATE ---
        # If the user held the resistor backwards, we reverse the list 
        # so the UI displays the logical reading order top-to-bottom
        if sorted_bands and sorted_bands[0] in ['gold', 'silver']:
            sorted_bands.reverse()
        print("Final sorted bands (after potential reversal):", sorted_bands)
        # Update the UI Panel with detected colors
        self.update_colors_ui(sorted_bands)

        # Calculate Final Resistance
        current_lang = self.language_box.get()
        
        if sorted_bands:
            resistance_value = self.calculate_resistance(sorted_bands)
            if "Error" in resistance_value:
                err_msg = self.translations[current_lang]["Error: Not enough bands"]
                self.result_label.configure(text=f"{err_msg}")
            else:
                self.result_label.configure(text=f"{self.translations[current_lang]['Value']}{resistance_value}")
        else:
            self.result_label.configure(text=f"{self.translations[current_lang]['Value']}{self.translations[current_lang]['Not detected']}") 


    def calculate_resistance(self, bands):
        # Dictionary mappings
        color_values = {
            "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
            "green": 5, "blue": 6, "purple": 7, "gray": 8, "white": 9
        }
        multiplier_values = {
            "black": 1, "brown": 10, "red": 100, "orange": 1000, "yellow": 10000,
            "green": 100000, "blue": 1000000, "purple": 10000000, "gray": 100000000, "white": 1000000000,
            "gold": 0.1, "silver": 0.01
        }
        tolerance_values = {
            "brown": "±1%", "red": "±2%", "green": "±0.5%", "blue": "±0.25%", "purple": "±0.1%",
            "gray": "±0.05%", "gold": "±5%", "silver": "±10%"
        }

        if len(bands) < 3 or len(bands) > 5:
            return "Error"

        try:
            if len(bands) == 3 or len(bands) == 4:
                val = (color_values[bands[0]] * 10) + color_values[bands[1]]
                res = val * multiplier_values.get(bands[2], 1)
                tol = tolerance_values.get(bands[3], "") if len(bands) == 4 else "±20%"
                return f"{self.format_ohms(res)} {tol}"

            elif len(bands) >= 5:
                val = (color_values[bands[0]] * 100) + (color_values[bands[1]] * 10) + color_values[bands[2]]
                res = val * multiplier_values.get(bands[3], 1)
                tol = tolerance_values.get(bands[4], "")
                return f"{self.format_ohms(res)} {tol}"
                
        except KeyError:
            return "Error"
        return "Error"

        
    def format_ohms(self, value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f} MΩ"
        elif value >= 1_000:
            return f"{value / 1_000:.2f} kΩ"
        else:
            return f"{value:g} Ω"


if __name__ == "__main__":
    app = OhmegaResistorApp()
    app.mainloop()
    