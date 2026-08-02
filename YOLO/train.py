from ultralytics import YOLO
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)
results = model.train(data="data.yaml",
                       epochs=100, 
                       imgsz=640, 
                      batch=16, 
                      device=0, 
                      name="yolo26n_resistor_color_bands_detection"
                      )  # train the model