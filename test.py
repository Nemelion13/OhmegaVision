import cv2
import customtkinter as ctk
from PIL import Image
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Flux Vidéo dans CustomTkinter")
        self.geometry("640x480")

        # 1. Créer un label pour afficher la vidéo
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(padx=10, pady=10)

        # 2. Initialiser la capture vidéo (0 pour la webcam par défaut)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erreur : Impossible d'ouvrir la caméra.")
            self.destroy()
            return

        # 3. Démarrer la mise à jour du flux dans un thread séparé
        self.running = True
        self.thread = threading.Thread(target=self.update_video)
        self.thread.daemon = True  # Le thread s'arrêtera avec la fenêtre
        self.thread.start()

        # 4. Gérer la fermeture propre de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video(self):
        """Boucle principale pour lire et afficher les frames."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convertir l'image de BGR (OpenCV) en RGB (PIL/CustomTkinter)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convertir le tableau numpy en image PIL
                img = Image.fromarray(frame_rgb)
                # Créer une image CustomTkinter
                ctk_image = ctk.CTkImage(light_image=img, size=(640, 480))
                # Mettre à jour le label avec la nouvelle image
                self.video_label.configure(image=ctk_image)
                self.video_label.image = ctk_image  # Garder une référence

    def on_close(self):
        """Arrêter le thread et libérer la caméra."""
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()