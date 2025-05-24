import os
from ultralytics import YOLO
import cv2
import numpy as np
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.results_dir = 'app/static/results'
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
        # Initialize BLIP-2 model for VQA (switched to flan-t5-xl)
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
        self.vqa_model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-flan-t5-xl", 
            torch_dtype=torch.float16
        )
        if torch.cuda.is_available():
            self.vqa_model = self.vqa_model.to("cuda")

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

    def count_objects(self, image_path, object_name):
        """Count specific objects in the image"""
        results = self.model(image_path)
        count = 0
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                if class_name == object_name:
                    count += 1
        
        return count

    def answer_question(self, image_path, question):
        """Answer a question about the image using BLIP-2"""
        try:
            # Load and process the image using PIL
            image = Image.open(image_path).convert("RGB")
            
            # Process the image and question
            inputs = self.processor(image, question, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            # Generate answer
            generated_ids = self.vqa_model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                min_length=1,
                repetition_penalty=1.5,
                length_penalty=1.0,
                temperature=1.0,
            )
            
            answer = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            print(f"[BLIP2] Q: {question} | A: {answer}")
            if answer.lower() == question.lower():
                return "Sorry, I could not answer this question."
            return answer
            
        except Exception as e:
            print(f"Error in answer_question: {str(e)}")
            return f"Error processing question: {str(e)}"

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