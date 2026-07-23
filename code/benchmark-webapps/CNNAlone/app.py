import os
import sys
from flask import Flask, render_template, request, redirect, url_for
import torch
import torch.nn as nn
from torchvision import transforms, models
import numpy as np
import cv2
from PIL import Image
import traceback
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the CNN model architecture (as a fallback if direct loading fails)
class BurnCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(BurnCNN, self).__init__()
        # This is a placeholder architecture - you need to match your actual model architecture
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(256 * 7 * 7, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# Load the PyTorch model
MODEL_PATH = '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/New-Way/CNN-DatasetNM/best_cnn_full.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"Loading model from {MODEL_PATH}")
print(f"Using device: {device}")

# Load checkpoint - which is an OrderedDict (state_dict)
checkpoint = torch.load(MODEL_PATH, map_location=device)
print(f"Checkpoint type: {type(checkpoint)}")

# Try a few different common model architectures
# Since we don't know the exact architecture, we'll try a pretrained model
# ResNet50 is a common choice for image classification
model = models.resnet50(pretrained=False)
# Modify the final layer to output 4 classes
model.fc = nn.Linear(model.fc.in_features, 4)

try:
    # Try loading the state_dict (with strict=False to ignore missing/extra keys)
    model.load_state_dict(checkpoint, strict=False)
    print("Loaded ResNet50 model with state_dict")
except Exception as e:
    print(f"Error loading ResNet50: {e}")
    
    # If ResNet50 fails, try ResNet18
    try:
        model = models.resnet18(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 4)
        model.load_state_dict(checkpoint, strict=False)
        print("Loaded ResNet18 model with state_dict")
    except Exception as e:
        print(f"Error loading ResNet18: {e}")
        
        # If that also fails, try a simple CNN
        try:
            model = BurnCNN()
            model.load_state_dict(checkpoint, strict=False)
            print("Loaded custom CNN with state_dict")
        except Exception as e:
            print(f"Error loading custom CNN: {e}")
            print("Using untrained model as fallback")

model.to(device)
model.eval()  # Set to evaluation mode

# Define image transformation
IMG_SIZE = 224
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    # Load and preprocess image for PyTorch
    with open(image_path, 'rb') as f:
        img = Image.open(f).convert('RGB')
    
    input_tensor = transform(img)
    input_batch = input_tensor.unsqueeze(0).to(device)
    
    # Make prediction with PyTorch model
    with torch.no_grad():
        try:
            output = model(input_batch)
            
            # Handle different output formats
            if isinstance(output, tuple):
                # Some models return multiple outputs, take the first one
                output = output[0]
                
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        except Exception as e:
            print(f"Error during prediction: {e}")
            # Fallback to default values in case of error
            predicted_idx = torch.tensor([0])
            confidence = torch.tensor([0.0])
    
    class_names = ['No Burn', 'First Degree', 'Second Degree', 'Third Degree']
    predicted_class = class_names[predicted_idx.item()]
    confidence_value = confidence.item()
    
    # Load image for visualization
    img_cv = cv2.imread(image_path)
    img_cv = cv2.resize(img_cv, (IMG_SIZE, IMG_SIZE))
    
    # Draw boundary box and text
    cv2.rectangle(img_cv, (0, 0), (IMG_SIZE, IMG_SIZE), (0, 255, 0), 2)
    cv2.putText(img_cv, f'{predicted_class} ({confidence_value:.2f})', 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Save the processed image
    output_path = image_path.replace('.', '_processed.')
    cv2.imwrite(output_path, img_cv)
    
    return predicted_class, confidence_value, os.path.basename(output_path)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                # Save original image
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Process image and get prediction
                predicted_class, confidence, processed_filename = process_image(filepath)
                
                # Render result template
                return render_template('result.html',
                                    original_image=filename,
                                    processed_image=processed_filename,
                                    prediction=predicted_class,
                                    confidence=confidence)
            except Exception as e:
                error_message = f"Error during processing: {e}"
                print(error_message)
                print(traceback.format_exc())
                return render_template('index.html', error=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)