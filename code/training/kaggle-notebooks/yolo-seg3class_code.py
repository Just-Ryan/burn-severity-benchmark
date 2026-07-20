################################################################################
# 1. Install Required Packages
################################################################################
!pip install --quiet ultralytics==8.0.43
!pip install --upgrade ultralytics
!pip install --quiet --upgrade ray==2.6.3
!pip install --quiet matplotlib seaborn
################################################################################
# 2. Import Libraries
################################################################################
import os
from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
################################################################################
# 3. Create Data YAML for 3-Class YOLOv8 Segmentation
################################################################################
data_yaml = """
train: /kaggle/input/yolo-seg3c-dt/BIAC.v31i.yolov8_3Class/train
val: /kaggle/input/yolo-seg3c-dt/BIAC.v31i.yolov8_3Class/valid
test: /kaggle/input/yolo-seg3c-dt/BIAC.v31i.yolov8_3Class/test
nc: 3
names: ["Degree1", "Degree2", "Degree3"]
"""
yaml_path = "/kaggle/working/data_3class.yaml"
with open(yaml_path, "w") as f:
    f.write(data_yaml)
print("Created data YAML at:", yaml_path)
################################################################################
# 4. Initialize and Train YOLOv8x-Seg Model
################################################################################
model = YOLO("yolov8x-seg.pt")  # Use YOLOv8x for segmentation
results = model.train(
    data=yaml_path,               # Path to the 3-class dataset YAML
    epochs=300,                   # Increase epochs for better convergence
    imgsz=640,                    # Image size (higher improves accuracy but uses more GPU memory)
    batch=8,                      # Reduce batch size if GPU memory is limited
    device=0,                     # Use the Tesla accelerator (GPU)
    augment=True,                 # Enable advanced data augmentation
    optimizer="AdamW",            # Use AdamW for better generalization
    lr0=0.0001,                   # Initial learning rate
    lrf=0.01,                     # Final learning rate (1% of initial LR)
    momentum=0.937,               # Momentum for SGD or AdamW
    weight_decay=0.0005,          # Regularization to prevent overfitting
    box=10.0,                     # Higher weight for bounding box accuracy
    cls=0.3,                      # Lower weight for classification loss
    hsv_h=0.015,                  # HSV-Hue augmentation (adjust for burn color variations)
    hsv_s=0.7,                    # HSV-Saturation augmentation
    hsv_v=0.4,                    # HSV-Value augmentation
    degrees=0,                    # Disable rotation (burns are sensitive to orientation)
    translate=0.1,                # Small translation augmentation
    scale=0.5,                    # Scale augmentation (zoom in/out slightly)
    shear=0,                      # Disable shear (burns are sensitive to distortion)
    perspective=0,                # Disable perspective transformation
    flipud=0,                     # Disable vertical flipping (burns are not symmetric vertically)
    fliplr=0.5,                   # Horizontal flipping (common for images)
    mosaic=0.5,                   # Reduce mosaic augmentation to avoid confusion
    mixup=0.0,                    # Disable mixup (can confuse segmentation boundaries)
    copy_paste=0.0,               # Disable copy-paste (avoids overlapping burns)
    project="/kaggle/working",    # Save logs and weights here
    name="yolov8_3class_seg_v5",  # Folder name for the training run
    verbose=True,                 # Show detailed logs
    cache=True,                   # Cache images for faster training
    workers=4,                    # Number of workers for data loading
    patience=100,                 # Early stopping patience (stop if no improvement for 100 epochs)
    amp=True                      # Enable mixed precision training for faster convergence
)
################################################################################
# 5. Post-Training
################################################################################
print("Training completed! Check '/kaggle/working/yolov8_3class_seg_v5' for logs and weights.")
################################################################################
# 6. Evaluate the Model on the Validation Set
################################################################################
metrics = model.val()  # Evaluate the model on the validation set
print("Validation Metrics:", metrics)
################################################################################
# 7. Test the Model on the Test Set
################################################################################
test_images_dir = '/kaggle/input/yolo-seg3c-dt/BIAC.v31i.yolov8_3Class/test/images'
test_results = model(test_images_dir)

# Visualize test results
for r in test_results:
    im_array = r.plot()  # Plot predictions (bounding boxes and masks) on the image
    im = Image.fromarray(im_array[..., ::-1])  # Convert to PIL image
    im.show()  # Display the image
################################################################################
# 8. Export the Trained Model
################################################################################
model.export(format="onnx")  # Export the trained model to ONNX format
print("Model exported to ONNX format.")
################################################################################
# 9. Plot Training Metrics
################################################################################
# Load training results from the log file
log_file = "/kaggle/working/yolov8_3class_seg_v5/results.csv"
if os.path.exists(log_file):
    results_df = pd.read_csv(log_file)

    # Plot Losses
    plt.figure(figsize=(12, 6))
    plt.plot(results_df["epoch"], results_df["train/box_loss"], label="Box Loss")
    plt.plot(results_df["epoch"], results_df["train/seg_loss"], label="Segmentation Loss")
    plt.plot(results_df["epoch"], results_df["train/cls_loss"], label="Classification Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Losses")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot mAP50 and Segmentation mAP50
    plt.figure(figsize=(12, 6))
    plt.plot(results_df["epoch"], results_df["metrics/mAP50(B)"], label="mAP50")
    plt.plot(results_df["epoch"], results_df["metrics/mAP50-95(B)"], label="mAP50-95")
    plt.plot(results_df["epoch"], results_df["metrics/mAP50(S)"], label="Segmentation mAP50")
    plt.xlabel("Epoch")
    plt.ylabel("mAP")
    plt.title("mAP Metrics")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Log file not found. Skipping plotting.")