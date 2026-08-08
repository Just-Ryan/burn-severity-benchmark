import sys
import os
# Add yolov5 to path
yolo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yolov5')
if yolo_path not in sys.path:
    sys.path.append(yolo_path)

import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def visualize_detection(model, image_path):
    """
    Visualize object detection results for a single image and save it.
    """
    # Class names and colors
    class_names = ['first_degree', 'second_degree', 'third_degree']
    colors = {
        'first_degree': (50, 200, 50),    # Green
        'second_degree': (50, 150, 250),  # Orange
        'third_degree': (250, 50, 50)     # Red
    }
    
    # Load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Make prediction
    results = model(img)
    
    # Get detection results
    pred_boxes = results.xyxy[0].cpu().numpy()
    
    # Create a copy of the image for drawing
    img_draw = img.copy()
    
    # Draw each detection
    for box in pred_boxes:
        x1, y1, x2, y2, conf, cls = box
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        class_id = int(cls)
        score = conf
        
        class_name = class_names[class_id]
        color = colors[class_name]
        
        # Draw bounding box
        cv2.rectangle(img_draw, (x1, y1), (x2, y2), color, 2)
        
        # Create label
        label = f'{class_name} {score:.2f}'
        
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        
        # Draw label background
        cv2.rectangle(img_draw, (x1, y1 - text_height - 10), 
                     (x1 + text_width, y1), color, -1)
        
        # Draw label text
        cv2.putText(img_draw, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        print(f"Detected {class_name} with confidence: {score:.2f}")
    
    # Convert back to BGR for saving
    img_draw = cv2.cvtColor(img_draw, cv2.COLOR_RGB2BGR)
    
    # Create output directory if it doesn't exist
    output_dir = 'output_detections'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the image with detections
    output_path = os.path.join(output_dir, f'detection_{os.path.basename(image_path)}')
    cv2.imwrite(output_path, img_draw)
    print(f"\nSaved detection result to: {output_path}")
    
    return output_path

def process_test_images(model, test_dir):
    """
    Process all images in the test directory
    """
    # Get all image files
    image_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(image_files)} images in test directory")
    
    # Process each image
    for image_file in image_files:
        print(f"\nProcessing {image_file}...")
        image_path = os.path.join(test_dir, image_file)
        output_path = visualize_detection(model, image_path)
        
        # Display using cv2.imshow (press any key to continue to next image)
        img = cv2.imread(output_path)
        cv2.imshow('Detection Result', img)
        cv2.waitKey(0)
    
    cv2.destroyAllWindows()

try:
    # Load YOLOv5 model using local path
    print("Loading model...")
    model = torch.hub.load('./yolov5', 'custom', 
                         path='<PROJECT_ROOT>/code/TestingCompare/YoloAlone/best.pt',
                         source='local')
    
    # Set up model parameters
    model.conf = 0.25  # Confidence threshold
    model.iou = 0.45   # NMS IoU threshold
    
    # Set the path to test images
    test_dir = "<PROJECT_ROOT>/code/dataset/Yolo_Dataset/Yolo_Only_Dataset/test/images"
    
    # Verify paths exist
    if not os.path.exists(test_dir):
        raise FileNotFoundError(f"Test directory not found: {test_dir}")
    
    # Process all test images
    process_test_images(model, test_dir)
    
except Exception as e:
    print(f"An error occurred: {str(e)}")