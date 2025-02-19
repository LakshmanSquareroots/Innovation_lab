import torch
import os
import cv2
from PIL import Image
import numpy as np
from flask import Response
from ultralytics import YOLO
import numpy as np

class YOLOModel:
 
    def __init__(self):
        """
        Initialize YOLOv5 model by loading weights from a local file.
        """

        self.model = YOLO("yolov8n.pt")  # Use "yolov8s.pt" for a better model
        

    def process_image(self, image):
        

        # Read image
        # image = cv2.imread(image_path)

        image  = np.asarray(image)
        image = np.copy(image)
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Run YOLO Object Detection
        results = self.model(image)[0]
        detections = []
        try:
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = results.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                
                detections.append({"label": label, "confidence": confidence, "bbox": [x1, y1, x2, y2]})
                print((x1, y1), (x2, y2))
                # Draw bounding boxes
                print(type(image))
                cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(image_rgb, f"{label} {confidence:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        except Exception as e:
            print(f"Error during bounding box drawing: {e}")
        
        return image_rgb

class FaceDetectionModel:
    def __init__(self):
        # Placeholder for a face detection model
        pass

    def process_image(self, image_path):
        """
        Dummy face detection function for demonstration.
        """
        return "Face detection processing not implemented yet."

class LabelReadingModel:
    def __init__(self):
        # Placeholder for a label reading model
        pass

    def process_image(self, image_path):
        """
        Dummy label reading function for demonstration.
        """
        return "Label reading processing not implemented yet."
