!pip install ultralytics matplotlib seaborn

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
    train_files, val_files = train_test_split(image_files, train_size=train_size, random_state=42, shuffle=True, stratify=None)
    
    # Copy files to respective directories
    for files, split in [(train_files, 'train'), (val_files, 'val')]:
        for img_path in files:
            # Copy image
            shutil.copy2(img_path, f'/kaggle/working/dataset/{split}/images/{img_path.name}')
            # Copy corresponding label
            label_path = Path(f'{data_path}/labels/{img_path.stem}.txt')
            if label_path.exists():
                shutil.copy2(label_path, f'/kaggle/working/dataset/{split}/labels/{label_path.name}')

# Create yaml file for 3 classes
def create_yaml():
    yaml_content = {
        'path': '/kaggle/working/dataset',
        'train': 'train/images',
        'val': 'val/images',
        'names': {
            0: 'first_degree',
            1: 'second_degree',
            2: 'third_degree'
        }
    }
    
    with open('/kaggle/working/dataset.yaml', 'w') as f:
        yaml.dump(yaml_content, f)

def train_model():
    # Initialize model
    model = YOLO('yolov8x.pt')  # Using YOLOv8x for best accuracy
    
    # Training arguments optimized for multi-class detection
    args = {
        'data': '/kaggle/working/dataset.yaml',
        'epochs': 150,  # Increased epochs for better class separation
        'imgsz': 640,   # Input image size
        'batch': 16,    # Batch size
        'patience': 50,  # Early stopping patience
        'optimizer': 'AdamW',  # AdamW optimizer for better convergence
        'lr0': 0.001,   # Initial learning rate
        'lrf': 0.0001,  # Final learning rate
        'momentum': 0.937,  # SGD momentum/Adam beta1
        'weight_decay': 0.0005,  # Weight decay coefficient
        'warmup_epochs': 5.0,  # Increased warmup epochs for stability
        'warmup_momentum': 0.8,
        'warmup_bias_lr': 0.1,
        'box': 7.5,     # Box loss gain
        'cls': 0.75,    # Increased classification loss gain for better class separation
        'dfl': 1.5,     # DFL loss gain
        'save': True,   # Save checkpoints
        'cache': False,
        'device': 0,    # GPU device
        'workers': 8,   # Number of worker threads
        'project': '/kaggle/working/runs/detect',
        'name': 'burn_classification',
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'AdamW',
        'verbose': True,
        'seed': 42,
        'deterministic': True,  # For reproducibility
        'dropout': 0.2,  # Added dropout for better generalization
        'label_smoothing': 0.1,  # Label smoothing for better generalization
    }
    
    # Start training
    results = model.train(**args)
    
    # After training, validate the model
    metrics = model.val()
    print("\nValidation Metrics:")
    print(f"mAP50: {metrics.box.map50:.3f}")
    print(f"mAP50-95: {metrics.box.map:.3f}")
    for i, class_ap in enumerate(metrics.box.ap_class):
        print(f"AP for class {i}: {class_ap:.3f}")

def main():
    print("Setting up dataset...")
    create_dataset_splits('/kaggle/input/yoloonlyds/Dataset')
    
    print("Creating YAML configuration...")
    create_yaml()
    
    print("Starting model training...")
    train_model()
    
    print("Training complete!")

if __name__ == "__main__":
    main()

# Optional: Add confusion matrix visualization after training
def plot_confusion_matrix():
    import matplotlib.pyplot as plt
    from ultralytics.utils.plotting import plot_confusion_matrix
    
    # Load the best model
    model = YOLO('/kaggle/working/runs/detect/burn_classification/weights/best.pt')
    
    # Get confusion matrix
    confusion_matrix = model.val()[0].confusion_matrix
    
    # Plot confusion matrix
    class_names = ['First Degree', 'Second Degree', 'Third Degree']
    plot_confusion_matrix(confusion_matrix.matrix, class_names)
    plt.title('Burn Classification Confusion Matrix')
    plt.savefig('/kaggle/working/confusion_matrix.png')
    plt.close()

# Run confusion matrix plotting after training
plot_confusion_matrix()