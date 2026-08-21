# Ohmega Resistor

**Author:** BEKALE Hans Hearlly, Mechatronic Engineer  
**Date:** July-August 2026  

---

## 📖 About the Project

This document explains that the project relies on a CustomTkinter interface combined with computer vision. This application allows users to obtain a resistor's value in ohms by holding it in front of their webcam. It is also possible to load an image of the component directly from the computer.

Powered by a custom YOLO model (YOLO26) and OpenCV, the software automatically isolates the resistor, identifies its color bands, filters out double-detections, and calculates the precise resistance value and tolerance in real-time.


---

## ✨ Key Features

* **Real-Time Analysis:** Instantly read resistor values using your computer's webcam.
* **Image Processing:** Load an existing picture of a resistor for static analysis.
* **Smart Orientation Detection:** Automatically detects the Gold/Silver tolerance band to read the resistor from the correct direction, even if held upside down.
* **Spatial Anti-Duplication:** Built-in algorithm to prevent the AI from counting the same color band twice.
* **Modern UI:** Built with CustomTkinter featuring Dark/Light mode, dynamic zoom, and a sensitivity (confidence) slider.
* **Bilingual Support:** Interface available in both English and French.


---

## ⚙️ Installation & Requirements

To run this application, you will need Python installed on your system. 

1. Clone this repository to your local machine.
2. Install the required dependencies by reading the `requirements.txt` file:

```bash
pip install -r requirements.txt

 ## Crédits
    Ohmega Vision icon: Gemini pro

    settings icon : Icône de Parametres by dtafalonso (Dtaf Alonso) on <a href="https://icon-icons.com/fr/authors/125-dtafalonso-dtaf-alonso">Icon-Icons.com</a>

    camera icon : Icône de Camera photo by Vexels on <a href="https://icon-icons.com/fr/authors/525-vexels">Icon-Icons.com</a>

    help icon : Icône de Aider et soutien by Sean Poon on <a href="https://icon-icons.com/fr/authors/81-sean-poon">Icon-Icons.com</a> 
---
--- 
 
## HELP
---
   