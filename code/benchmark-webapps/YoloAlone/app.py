from flask import Flask, render_template, request, redirect, url_for
import torch
import cv2
import numpy as np
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLOv5 model
YOLO_PATH = "<PROJECT_ROOT>/code/TestingCompare/YoloAlone/best.pt"
YOLOV5_DIR = "<PROJECT_ROOT>/code/TestingCompare/YoloAlone/yolov5"
model = torch.hub.load(YOLOV5_DIR, 'custom', path=YOLO_PATH, source='local')
model.conf = 0.25  # confidence threshold
model.iou = 0.45   # NMS IoU threshold

# Class names
class_names = ['first_degree', 'second_degree', 'third_degree']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    """Process image and return detection results"""
    # Read image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Get predictions
    results = model(image)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    
    detections = []
    
    # Draw boxes and collect detection info
    for det in results.pred[0]:
        x1, y1, x2, y2, conf, cls = det.cpu().numpy()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        cls = int(cls)
        
        # Draw bounding box
        plt.gca().add_patch(plt.Rectangle((x1, y1), 
                                        x2-x1, y2-y1,
                                        fill=False, 
                                        color='red', 
                                        linewidth=2))
        
        # Add label
        plt.text(x1, y1-10, 
                f'{class_names[cls]} {conf:.2f}',
                color='red',
                fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7))
        
        detections.append({
            'class': class_names[cls],
            'confidence': float(conf),
            'bbox': [x1, y1, x2, y2]
        })
    
    plt.axis('off')
    
    # Save plot
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.png')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return detections, output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save uploaded file
            file.save(filepath)
            
            # Process image
            detections, result_path = process_image(filepath)
            
            # Render result page
            return render_template('result.html',
                                original_image=filename,
                                result_image='result.png',
                                detections=detections)
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)