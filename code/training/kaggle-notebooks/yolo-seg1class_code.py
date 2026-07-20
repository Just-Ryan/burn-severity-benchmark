################################################################################
# 1. Install Required Packages
################################################################################
!pip install ultralytics
!pip install torch torchvision
!pip install pyyaml matplotlib numpy

# ===== CELL =====
# YOLOv8 Segmentation Model Training for Burn Detection
# This script trains a YOLOv8 segmentation model on a single class (burns)

import os
import yaml
import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Image

# Create data.yaml file
data_yaml = """
train: /kaggle/input/yolo-seg1c-dt/BIAC.v31i.yolov8_1Class/train
val: /kaggle/input/yolo-seg1c-dt/BIAC.v31i.yolov8_1Class/valid
test: /kaggle/input/yolo-seg1c-dt/BIAC.v31i.yolov8_1Class/test
nc: 1
names: ["Burn"]
"""

# Create config directory if it doesn't exist
os.makedirs('config', exist_ok=True)

# Save the YAML configuration
with open('config/burn_data.yaml', 'w') as f:
    f.write(data_yaml)

print("Data YAML configuration file created successfully.")

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

if device == "cuda":
    # Print GPU info
    gpu_info = !nvidia-smi
    print("\nGPU Information:")
    for line in gpu_info:
        print(line)

# Function to train the model
def train_model(model_size="m", epochs=100, imgsz=640, batch=16, patience=20):
    """
    Train a YOLOv8 segmentation model.
    
    Args:
        model_size: Size of the YOLOv8 model (n, s, m, l, x)
        epochs: Number of training epochs
        imgsz: Input image size
        batch: Batch size
        patience: Early stopping patience
    
    Returns:
        trained_model: The trained YOLO model
        results: Training results
    """
    # Load a pre-trained YOLOv8 segmentation model
    model = YOLO(f'yolov8{model_size}-seg.pt')
    
    # Train the model
    results = model.train(
        data='config/burn_data.yaml',
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        patience=patience,
        device=device,
        workers=8,
        cos_lr=True,  # Use cosine learning rate scheduler
        lr0=0.005,     # Initial learning rate
        lrf=0.0005,    # Final learning rate
        momentum=0.937,
        weight_decay=0.00037,
        warmup_epochs=3,
        warmup_momentum=0.8,
        augment=True, # Use data augmentation
        mixup=0.15,    # Apply mixup
        mosaic=0.8,   # Apply mosaic augmentation
        degrees=0.1,  # Rotation augmentation 
        shear=0.2,    # Shear augmentation
        perspective=0.0015, # Perspective augmentation
        flipud=0.1,   # Flip up-down augmentation
        fliplr=0.5,   # Flip left-right augmentation
        hsv_h=0.0,  # HSV hue augmentation
        hsv_s=0.4,    # HSV saturation augmentation
        hsv_v=0.2,    # HSV value augmentation
        translate=0.1,  # Add some translation
        scale=0.2,  # Add scale variation
        copy_paste=0.15, # Copy-paste augmentation
        project='burn_segmentation',
        name=f'yolov8{model_size}_burn_seg',
        exist_ok=True,
        save=True,
        verbose=True,
        pretrained=True,
        optimizer="SGD"  # Try SGD instead of the default
    )
    
    return model, results

# Function to evaluate the model
# Updated function to evaluate the model
def evaluate_model(model, data_yaml_path='config/burn_data.yaml'):
    """
    Evaluate the trained model on the validation set.
    
    Args:
        model: Trained YOLO model
        data_yaml_path: Path to the data YAML file
    """
    # Parse the YAML to get the validation path
    with open(data_yaml_path, 'r') as f:
        data_config = yaml.safe_load(f)
    
    # Evaluate on validation set
    val_results = model.val(data=data_yaml_path, split='val')
    
    print("\nValidation Results:")
    print(f"mAP50-95: {val_results.box.map:.4f}")
    print(f"mAP50: {val_results.box.map50:.4f}")
    
    # Handle precision and recall safely - they might be arrays in newer versions
    if hasattr(val_results.box, 'p') and not isinstance(val_results.box.p, np.ndarray):
        print(f"Precision: {val_results.box.p:.4f}")
    elif hasattr(val_results.box, 'p') and isinstance(val_results.box.p, np.ndarray):
        print(f"Precision: {np.mean(val_results.box.p):.4f}")
    
    if hasattr(val_results.box, 'r') and not isinstance(val_results.box.r, np.ndarray):
        print(f"Recall: {val_results.box.r:.4f}")
    elif hasattr(val_results.box, 'r') and isinstance(val_results.box.r, np.ndarray):
        print(f"Recall: {np.mean(val_results.box.r):.4f}")
    
    # Segmentation metrics
    print("\nSegmentation Results:")
    print(f"Segmentation mAP50-95: {val_results.seg.map:.4f}")
    print(f"Segmentation mAP50: {val_results.seg.map50:.4f}")
    
    # Handle precision and recall for segmentation safely
    if hasattr(val_results.seg, 'p') and not isinstance(val_results.seg.p, np.ndarray):
        print(f"Segmentation Precision: {val_results.seg.p:.4f}")
    elif hasattr(val_results.seg, 'p') and isinstance(val_results.seg.p, np.ndarray):
        print(f"Segmentation Precision: {np.mean(val_results.seg.p):.4f}")
    
    if hasattr(val_results.seg, 'r') and not isinstance(val_results.seg.r, np.ndarray):
        print(f"Segmentation Recall: {val_results.seg.r:.4f}")
    elif hasattr(val_results.seg, 'r') and isinstance(val_results.seg.r, np.ndarray):
        print(f"Segmentation Recall: {np.mean(val_results.seg.r):.4f}")
    
    return val_results

# Function to visualize some predictions
def visualize_predictions(model, data_yaml_path='config/burn_data.yaml', num_samples=3):
    """
    Visualize some prediction examples from the validation set.
    
    Args:
        model: Trained YOLO model
        data_yaml_path: Path to the data YAML file
        num_samples: Number of samples to visualize
    """
    # Parse the YAML to get the validation path
    with open(data_yaml_path, 'r') as f:
        data_config = yaml.safe_load(f)
    
    val_path = data_config['val']
    
    # Get some validation image paths
    import glob
    val_images = glob.glob(os.path.join(val_path, '**/*.jpg'), recursive=True) + \
                 glob.glob(os.path.join(val_path, '**/*.jpeg'), recursive=True) + \
                 glob.glob(os.path.join(val_path, '**/*.png'), recursive=True)
    
    # Select random samples
    if len(val_images) > 0:
        samples = np.random.choice(val_images, min(num_samples, len(val_images)), replace=False)
        
        for i, sample in enumerate(samples):
            # Predict on the sample
            results = model.predict(sample, save=True, conf=0.25)
            
            # Display the prediction
            print(f"\nSample {i+1} Prediction:")
            display(Image(results[0].plot(labels=True, boxes=False)))
    else:
        print("No validation images found. Check the path in your YAML file.")

# Main execution
if __name__ == "__main__":
    # Define model sizes to try
    model_sizes = ['l', 'x']  # Medium and Large models
    
    best_map = 0
    best_model = None
    best_size = None
    
    for size in model_sizes:
        print(f"\n{'='*50}")
        print(f"Training YOLOv8-{size}-seg model")
        print(f"{'='*50}")
        
        # Train model with this size
        model, results = train_model(
            model_size=size,
            epochs=150,      # Increase epochs for better convergence
            imgsz=640,       # Standard YOLOv8 image size
            batch=8,         # Adjust based on GPU memory
            patience=25      # Patience for early stopping
        )
        
        # Evaluate model
        val_results = evaluate_model(model)
        
        # Check if this is the best model so far
        current_map = val_results.seg.map
        if current_map > best_map:
            best_map = current_map
            best_model = model
            best_size = size
            print(f"\nNew best model: YOLOv8-{size}-seg with mAP: {current_map:.4f}")
    
    print(f"\n{'='*50}")
    print(f"Best model: YOLOv8-{best_size}-seg with mAP: {best_map:.4f}")
    print(f"{'='*50}")
    
    # Visualize some predictions with the best model
    if best_model is not None:
        visualize_predictions(best_model, num_samples=5)
        
        # Export the model for deployment
        best_model.export(format='onnx')  # Export to ONNX format
        best_model.export(format='saved_model')  # Export to TensorFlow SavedModel
        
        print(f"\nModel exported to 'burn_segmentation/yolov8{best_size}_burn_seg/weights/' directory")
        
        # Save some examples for inference
        test_results = best_model.predict(
            source='config/burn_data.yaml', 
            split='test',
            save=True, 
            conf=0.25,
            boxes=False,  # Don't show bounding boxes, only segmentation masks
            project='burn_segmentation',
            name=f'yolov8{best_size}_test_results'
        )
        
        print("\nTest results saved.")

# Example of how to use the model for inference on a new image
def predict_burn(model_path, image_path):
    """
    Predict burns on a new image.
    
    Args:
        model_path: Path to the trained model
        image_path: Path to the input image
    """
    # Load the model
    model = YOLO(model_path)
    
    # Predict on the image
    results = model.predict(
        source=image_path,
        conf=0.25,
        boxes=False,  # Only show segmentation masks, no bounding boxes
        save=True
    )
    
    # Display the result
    display(Image(results[0].plot(labels=True, boxes=False)))
    
    return results

# Uncomment the following line to use the model for inference after training:
# predict_burn('burn_segmentation/yolov8m_burn_seg/weights/best.pt', '/path/to/new/image.jpg')