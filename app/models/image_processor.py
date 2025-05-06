import os
from ultralytics import YOLO
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.results_dir = 'app/static/results'
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def detect_objects(self, image_path):
        """Detect objects in the image and return their names"""
        results = self.model(image_path)
        objects = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                objects.append(class_name)
        
        return list(set(objects))  # Return unique objects

    def highlight_object(self, image_path, object_name):
        print(f"[highlight_object] Called for {image_path} and object '{object_name}'")
        results = self.model(image_path)
        image = cv2.imread(image_path)
        if image is None:
            print(f"[highlight_object] ERROR: Could not read image {image_path}")
            return None
        found = False
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                if class_name == object_name:
                    found = True
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Draw rectangle
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Add label
                    label = f"{class_name} {box.conf[0]:.2f}"
                    cv2.putText(image, label, (x1, y1 - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if not found:
            print(f"[highlight_object] Object '{object_name}' not found in {image_path}")
            return None
        # Save the result as JPEG
        base = os.path.splitext(os.path.basename(image_path))[0]
        result_path = os.path.join(self.results_dir, f"highlighted_{base}.jpg")
        try:
            success = cv2.imwrite(result_path, image)
            if success:
                print(f"[highlight_object] Saved highlighted image to {result_path}")
            else:
                print(f"[highlight_object] ERROR: Failed to save image to {result_path}")
                return None
        except Exception as e:
            print(f"[highlight_object] Exception while saving image: {e}")
            return None
        return result_path 