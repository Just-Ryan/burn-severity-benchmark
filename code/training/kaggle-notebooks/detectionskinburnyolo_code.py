!pip install ultralytics

# ===== CELL =====
from ultralytics import YOLO
import os
import yaml
from sklearn.model_selection import train_test_split
import shutil
from pathlib import Path

# Create directories for train/val split
def create_dataset_splits(data_path, train_size=0.8):
    # Create directories
    for split in ['train', 'val']:
        for folder in ['images', 'labels']:
            os.makedirs(f'/kaggle/working/dataset/{split}/{folder}', exist_ok=True)
    
    # Get all image files
    image_files = list(Path(f'{data_path}/images').glob('*.jpg')) + \
                 list(Path(f'{data_path}/images').glob('*.jpeg')) + \
                 list(Path(f'{data_path}/images').glob('*.png'))
    
    # Split into train/val
    train_files, val_files = train_test_split(image_files, train_size=train_size, random_state=42)
    
    # Copy files to respective directories
    for files, split in [(train_files, 'train'), (val_files, 'val')]:
        for img_path in files:
            # Copy image
            shutil.copy2(img_path, f'/kaggle/working/dataset/{split}/images/{img_path.name}')
            # Copy corresponding label
            label_path = Path(f'{data_path}/labels/{img_path.stem}.txt')
            if label_path.exists():
                shutil.copy2(label_path, f'/kaggle/working/dataset/{split}/labels/{label_path.name}')

# Create yaml file
def create_yaml():
    yaml_content = {
        'path': '/kaggle/working/dataset',
        'train': 'train/images',
        'val': 'val/images',
        'names': {0: 'burn'}
    }
    
    with open('/kaggle/working/dataset.yaml', 'w') as f:
        yaml.dump(yaml_content, f)

def train_model():
    # Initialize model
    model = YOLO('yolov8x.pt')  # Load the largest YOLOv8 model for best accuracy
    
    # Training arguments
    args = {
        'data': '/kaggle/working/dataset.yaml',
        'epochs': 100,  # Number of epochs
        'imgsz': 640,   # Input image size
        'batch': 16,    # Batch size
        'patience': 50,  # Early stopping patience
        'optimizer': 'AdamW',  # Optimizer
        'lr0': 0.001,   # Initial learning rate
        'lrf': 0.0001,  # Final learning rate
        'momentum': 0.937,  # SGD momentum/Adam beta1
        'weight_decay': 0.0005,  # Weight decay coefficient
        'warmup_epochs': 3.0,  # Warmup epochs
        'warmup_momentum': 0.8,  # Warmup initial momentum
        'warmup_bias_lr': 0.1,  # Warmup initial bias lr
        'box': 7.5,     # Box loss gain
        'cls': 0.5,     # Classification loss gain
        'dfl': 1.5,     # DFL loss gain
        'save': True,   # Save checkpoints
        'cache': False, # Cache images for faster training
        'device': 0,    # Device to run on (GPU)
        'workers': 8,   # Number of worker threads
        'project': '/kaggle/working/runs/detect',  # Project name
        'name': 'burn_detection',  # Experiment name
        'exist_ok': True,  # Existing project/name ok
        'pretrained': True,  # Use pretrained model
        'optimizer': 'AdamW',  # Optimizer: SGD, Adam, AdamW, or RMSProp
        'verbose': True,  # Print verbose output
        'seed': 42,     # Random seed for reproducibility
        'deterministic': True,  # Enable deterministic mode
    }
    
    # Start training
    model.train(**args)

def main():
    print("Creating dataset splits...")
    create_dataset_splits('/kaggle/input/data4yolo/Dataset')
    
    print("Creating YAML file...")
    create_yaml()
    
    print("Starting model training...")
    train_model()
    
    print("Training complete!")

if __name__ == "__main__":
    main()