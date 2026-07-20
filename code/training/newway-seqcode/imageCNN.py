import os
import shutil
from pathlib import Path
from tqdm import tqdm

class BurnImageOrganizer:
    def __init__(self, input_dir, output_dir):
        """
        Initialize the burn image organizer
        
        Args:
            input_dir (str): Path to the YOLOv8 dataset directory
            output_dir (str): Path to save the organized images
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Define class mapping
        self.class_names = {
            0: 'Degree1',
            1: 'Degree2',
            2: 'Degree3'
        }
        
        # Create output directories
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories for each split and degree"""
        for split in ['train', 'valid', 'test']:
            for degree in self.class_names.values():
                dir_path = self.output_dir / split / degree
                dir_path.mkdir(parents=True, exist_ok=True)
                
    def get_highest_severity(self, label_path):
        """
        Read label file and return the highest severity class
        
        Args:
            label_path (Path): Path to the label file
            
        Returns:
            int: Highest severity class found (-1 if no valid labels)
        """
        if not label_path.exists():
            return -1
            
        highest_class = -1
        try:
            with open(label_path, 'r') as f:
                for line in f:
                    values = line.strip().split()
                    if len(values) < 7:  # Need at least class + 3 points
                        continue
                    class_id = int(values[0])
                    highest_class = max(highest_class, class_id)
        except Exception as e:
            print(f"Error reading {label_path}: {e}")
            return -1
            
        return highest_class
        
    def organize_split(self, split):
        """
        Organize images for a specific split based on their highest severity
        
        Args:
            split (str): Dataset split to process ('train', 'valid', or 'test')
        """
        images_dir = self.input_dir / split / 'images'
        labels_dir = self.input_dir / split / 'labels'
        
        if not images_dir.exists() or not labels_dir.exists():
            print(f"Directory not found: {split}")
            return
            
        # Process all images
        image_files = list(images_dir.glob('*'))
        for img_path in tqdm(image_files, desc=f'Organizing {split}'):
            # Get corresponding label file
            label_path = labels_dir / f"{img_path.stem}.txt"
            
            # Get highest severity class
            highest_class = self.get_highest_severity(label_path)
            
            if highest_class >= 0 and highest_class in self.class_names:
                # Determine destination directory
                dest_dir = self.output_dir / split / self.class_names[highest_class]
                
                # Copy image to appropriate directory
                shutil.copy2(
                    img_path,
                    dest_dir / img_path.name
                )
            else:
                print(f"Warning: No valid labels found for {img_path}")
                
    def organize_dataset(self):
        """Organize the complete dataset"""
        print("Starting dataset organization...")
        
        # Process each split
        for split in ['train', 'valid', 'test']:
            self.organize_split(split)
            
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print summary of organized dataset"""
        print("\nDataset Organization Summary:")
        print("-" * 40)
        
        for split in ['train', 'valid', 'test']:
            print(f"\n{split.upper()} Split:")
            for degree in self.class_names.values():
                dir_path = self.output_dir / split / degree
                if dir_path.exists():
                    num_images = len(list(dir_path.glob('*')))
                    print(f"  {degree}: {num_images} images")

def main():
    # Set paths
    input_dir = Path('/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_3Class')
    output_dir = Path('/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/New-Way/CNN-DatasetNM')
    
    # Initialize and run organizer
    organizer = BurnImageOrganizer(input_dir, output_dir)
    organizer.organize_dataset()
    
    print("\nOrganization completed. Images organized in:", output_dir)

if __name__ == "__main__":
    main()