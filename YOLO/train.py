from ultralytics import YOLO
import os
path = os.path.join(os.getcwd(), "../runs/detect/yolo26n_resistor_color_bands_detection/weights/last.pt")
model = YOLO(path)  # load a pretrained model (recommended for training)
#results = model.train(data="data.yaml",epochs=100, imgsz=640, batch=16,  name="yolo26n_resistor_color_bands_detection")  # train the model
results = model.train(resume=True)