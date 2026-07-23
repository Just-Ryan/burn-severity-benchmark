import os
import shutil
from sklearn.model_selection import train_test_split
import random

class DatasetSplitter:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.train_ratio = 0.7
        self.val_ratio = 0.15
        self.test_ratio = 0.15

    def create_directory_structure(self):
        """Create the required directory structure for YOLOv8"""
        # Define directories to create
        directories = [
            'train/images', 'train/labels',
            'val/images', 'val/labels',
            'test/images', 'test/labels'
        ]
        
        # Create base directories
        for dir_path in directories:
            full_path = os.path.join(self.dataset_path, dir_path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(f"Created directory: {full_path}")

    def get_image_label_pairs(self):
        """Get pairs of image and label files"""
        image_extensions = ['.jpg', '.jpeg', '.png']
        label_extension = '.txt'
        
        image_files = []
        label_files = []
        
        # Walk through the dataset directory
        for root, _, files in os.walk(self.dataset_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_ext = os.path.splitext(file)
                
                # Check if file is an image
                if file_ext.lower() in image_extensions:
                    label_path = os.path.join(root, file_name + label_extension)
                    if os.path.exists(label_path):
                        image_files.append(file_path)
                        label_files.append(label_path)
        
        return image_files, label_files

    def split_and_copy_files(self, image_files, label_files):
        """Split the dataset and copy files to appropriate directories"""
        # Create train/val split
        train_images, temp_images, train_labels, temp_labels = train_test_split(
            image_files, label_files, 
            train_size=self.train_ratio, 
            random_state=42
        )

        # Create val/test split from the remaining data
        val_ratio = self.val_ratio / (self.val_ratio + self.test_ratio)
        val_images, test_images, val_labels, test_labels = train_test_split(
            temp_images, temp_labels, 
            train_size=val_ratio, 
            random_state=42
        )

        # Copy files to their respective directories
        splits = {
            'train': (train_images, train_labels),
            'val': (val_images, val_labels),
            'test': (test_images, test_labels)
        }

        for split_name, (split_images, split_labels) in splits.items():
            for img_path, label_path in zip(split_images, split_labels):
                # Copy image
                dest_img = os.path.join(
                    self.dataset_path, 
                    split_name, 
                    'images', 
                    os.path.basename(img_path)
                )
                shutil.copy2(img_path, dest_img)

                # Copy label
                dest_label = os.path.join(
                    self.dataset_path, 
                    split_name, 
                    'labels', 
                    os.path.basename(label_path)
                )
                shutil.copy2(label_path, dest_label)

            print(f"{split_name}: {len(split_images)} images and labels copied")

    def create_yaml_file(self):
        """Create the data.yaml file"""
        yaml_content = f"""path: {self.dataset_path}  # dataset root directory
train: train/images  # train images
val: val/images  # val images
test: test/images  # test images

# Classes
names:
  0: first_degree
  1: second_degree
  2: third_degree

# number of classes
nc: 3"""

        yaml_path = os.path.join(self.dataset_path, 'data.yaml')
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        print(f"\nCreated data.yaml at: {yaml_path}")

    def process(self):
        """Main processing function"""
        print("Starting dataset organization...")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Get image and label pairs
        image_files, label_files = self.get_image_label_pairs()
        if not image_files:
            print("No image-label pairs found!")
            return
        
        print(f"\nFound {len(image_files)} image-label pairs")
        
        # Split and copy files
        self.split_and_copy_files(image_files, label_files)
        
        # Create YAML file
        self.create_yaml_file()
        
        print("\nDataset organization completed!")

if __name__ == "__main__":
    dataset_path = "/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/Yolo_Dataset/Yolo_Only_Dataset"
    
    splitter = DatasetSplitter(dataset_path)
    splitter.process()