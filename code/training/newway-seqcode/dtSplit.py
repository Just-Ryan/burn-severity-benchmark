import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm

class DatasetSplitter:
    def __init__(self, input_dir, output_dir, train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15, seed=42):
        """
        Initialize the dataset splitter.
        
        Args:
            input_dir (str): Path to the input directory that contains class subfolders (Degree1, Degree2, Degree3)
            output_dir (str): Path where the split dataset will be saved
            train_ratio (float): Fraction of images to use for training
            valid_ratio (float): Fraction for validation
            test_ratio (float): Fraction for testing
            seed (int): Random seed for reproducibility
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.train_ratio = train_ratio
        self.valid_ratio = valid_ratio
        self.test_ratio = test_ratio
        self.seed = seed
        
        # List of class names determined by subdirectories in input_dir
        self.class_names = [d.name for d in self.input_dir.iterdir() if d.is_dir()]
        
        # Create output directories for each split and class
        self.setup_directories()
    
    def setup_directories(self):
        """Create output directories for train, valid, and test splits for each class."""
        for split in ['train', 'valid', 'test']:
            for class_name in self.class_names:
                dir_path = self.output_dir / split / class_name
                dir_path.mkdir(parents=True, exist_ok=True)
    
    def split_and_copy(self):
        """
        For each class folder in the input directory, shuffle the images and copy them
        into train, valid, and test folders based on the defined ratios.
        """
        random.seed(self.seed)
        for class_name in self.class_names:
            class_dir = self.input_dir / class_name
            images = list(class_dir.glob('*.*'))  # Adjust pattern if needed (e.g., '*.jpeg' or '*.jpg')
            random.shuffle(images)
            n = len(images)
            n_train = int(n * self.train_ratio)
            n_valid = int(n * self.valid_ratio)
            # Remaining images go to test
            train_images = images[:n_train]
            valid_images = images[n_train:n_train+n_valid]
            test_images = images[n_train+n_valid:]
            
            print(f"Splitting {class_name}: total={n}, train={len(train_images)}, valid={len(valid_images)}, test={len(test_images)}")
            
            for img in tqdm(train_images, desc=f'Copying {class_name} to train'):
                shutil.copy2(img, self.output_dir / "train" / class_name / img.name)
            for img in tqdm(valid_images, desc=f'Copying {class_name} to valid'):
                shutil.copy2(img, self.output_dir / "valid" / class_name / img.name)
            for img in tqdm(test_images, desc=f'Copying {class_name} to test'):
                shutil.copy2(img, self.output_dir / "test" / class_name / img.name)
    
    def organize_dataset(self):
        """Organize the dataset by splitting each class folder into train, valid, and test."""
        print("Starting dataset organization...")
        self.split_and_copy()
        self.print_summary()
    
    def print_summary(self):
        """Print a summary of the number of images in each split and class."""
        print("\nDataset Organization Summary:")
        for split in ['train', 'valid', 'test']:
            print(f"\n{split.upper()} Split:")
            for class_name in self.class_names:
                dir_path = self.output_dir / split / class_name
                count = len(list(dir_path.glob('*')))
                print(f"  {class_name}: {count} images")

def main():
    # Input directory containing the three class folders: Degree1, Degree2, Degree3
    input_dir = '<PROJECT_ROOT>/code/dataset/New-Way/CNN-DatasetM'
    # Output directory for the organized dataset with train, valid, and test splits
    output_dir = '<PROJECT_ROOT>/code/dataset/New-Way/CNN-DatasetM'
    
    splitter = DatasetSplitter(input_dir, output_dir)
    splitter.organize_dataset()
    
    print(f"\nOrganization completed. The organized dataset is available at: {output_dir}")

if __name__ == "__main__":
    main()
