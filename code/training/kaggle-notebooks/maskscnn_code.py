################################################################################
# 1. Install Required Packages
################################################################################
!pip install --quiet torch torchvision torchaudio
!pip install --quiet timm albumentations tensorboard
################################################################################
# 2. Import Libraries
################################################################################
import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torch.cuda.amp import GradScaler, autocast
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms, models
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import timm
import numpy as np
################################################################################
# 3. Define Custom Dataset Class
################################################################################
class BurnDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))
        self.image_paths = []
        self.labels = []
        for label, class_name in enumerate(self.classes):
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                self.image_paths.append(os.path.join(class_dir, img_name))
                self.labels.append(label)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image=np.array(image))["image"]
        return image, label
################################################################################
# 4. Data Preprocessing and Augmentation
################################################################################
transform = A.Compose([
    A.Resize(224, 224),  # Resize to 224x224
    A.HorizontalFlip(p=0.5),  # Random horizontal flip
    A.RandomBrightnessContrast(p=0.2),  # Adjust brightness/contrast
    A.Rotate(limit=10, p=0.5),  # Random rotation
    A.CoarseDropout(max_holes=8, max_height=32, max_width=32, fill_value=0, p=0.3),  # Simulate occlusions
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize
    ToTensorV2()  # Convert to tensor
])
################################################################################
# 5. Load Datasets
################################################################################
train_dataset = BurnDataset("/kaggle/input/cnn-mask-dt/CNN-DatasetM/train", transform=transform)
val_dataset = BurnDataset("/kaggle/input/cnn-mask-dt/CNN-DatasetM/valid", transform=transform)
test_dataset = BurnDataset("/kaggle/input/cnn-mask-dt/CNN-DatasetM/test", transform=transform)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, pin_memory=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, pin_memory=True, num_workers=4)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False, pin_memory=True, num_workers=4)
################################################################################
# 6. Initialize State-of-the-Art Model
################################################################################
# DenseNet-121
model = timm.create_model("densenet201", pretrained=True)
num_ftrs = model.classifier.in_features
model.classifier = nn.Linear(num_ftrs, 3)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
################################################################################
# 7. Define Loss Function and Optimizer
################################################################################
class_counts = [100, 50, 30]  # Example counts for Degree1, Degree2, Degree3
class_weights = 1.0 / torch.tensor(class_counts, dtype=torch.float)
class_weights = class_weights.to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)

optimizer = optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.01)  # AdamW optimizer
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30)  # Cosine annealing scheduler

scaler = GradScaler()  # For mixed precision training
writer = SummaryWriter("/kaggle/working/logs")  # For TensorBoard logging
################################################################################
# 8. Train the Model with Early Stopping
################################################################################
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=30, patience=5):
    best_val_acc = 0.0
    trigger_times = 0

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            with autocast():  # Mixed precision training
                outputs = model(inputs)
                loss = criterion(outputs, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()

        train_acc = correct / total
        writer.add_scalar("Loss/train", running_loss, epoch)
        writer.add_scalar("Accuracy/train", train_acc, epoch)

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (preds == labels).sum().item()

        val_acc = val_correct / val_total
        writer.add_scalar("Accuracy/val", val_acc, epoch)
        scheduler.step()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss:.4f}, Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")

        # Save the best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            trigger_times = 0
            torch.save(model.state_dict(), "/kaggle/working/best_cnn_mask.pth")
        else:
            trigger_times += 1
            if trigger_times >= patience:
                print("Early stopping triggered.")
                break

    print("Training completed!")

train_model(model, train_loader, val_loader, criterion, optimizer)
################################################################################
# 9. Evaluate the Model on Test Set
################################################################################
model.load_state_dict(torch.load("/kaggle/working/best_cnn_mask.pth"))
model.eval()
test_correct = 0
test_total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        test_total += labels.size(0)
        test_correct += (preds == labels).sum().item()

test_acc = test_correct / test_total
print(f"Test Accuracy: {test_acc:.4f}")
################################################################################
# 10. Save Metadata
################################################################################
metadata = {
    "model": "densenet201",
    "optimizer": "AdamW",
    "lr": 0.0001,
    "batch_size": 16,
    "epochs": 30
}

with open("/kaggle/working/metadata.json", "w") as f:
    json.dump(metadata, f)