import os
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
import shutil

class MaskGenerator:
    def __init__(self, base_dir, output_dir):
        """
        Initialize the mask generator for YOLOv8 polygon annotations
        
        Args:
            base_dir (str): Path to the YOLOv8 dataset directory
            output_dir (str): Path to save the masked images
        """
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directories for each degree
        self.degree_dirs = {
            0: self.output_dir / 'Degree1',
            1: self.output_dir / 'Degree2',
            2: self.output_dir / 'Degree3'
        }
        
        for dir_path in self.degree_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def read_yolo_polygon(self, label_path, img_width, img_height):
        """
        Read YOLOv8 polygon annotation and convert to pixel coordinates
        
        Args:
            label_path (Path): Path to the label file
            img_width (int): Width of the image
            img_height (int): Height of the image
            
        Returns:
            list: List of tuples (class_id, polygon_points)
        """
        polygons = []
        
        if not label_path.exists():
            return polygons
            
        with open(label_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if len(values) < 7:  # Need at least class + 3 points (7 values)
                    continue
                    
                class_id = int(values[0])
                points = values[1:]
                
                # Convert normalized coordinates to pixel coordinates
                polygon_points = []
                for i in range(0, len(points), 2):
                    x = float(points[i]) * img_width
                    y = float(points[i + 1]) * img_height
                    polygon_points.append([int(x), int(y)])
                    
                polygons.append((class_id, np.array(polygon_points, np.int32)))
                
        return polygons
        
    def create_mask(self, image_shape, polygon_points):
        """
        Create a binary mask from polygon points
        
        Args:
            image_shape (tuple): Shape of the image (height, width)
            polygon_points (np.array): Array of polygon points
            
        Returns:
            np.array: Binary mask
        """
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [polygon_points], 255)
        return mask
        
    def apply_mask(self, image, mask):
        """
        Apply mask to image
        
        Args:
            image (np.array): Original image
            mask (np.array): Binary mask
            
        Returns:
            np.array: Masked image
        """
        # Create a 3-channel mask
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # Apply mask
        masked_image = cv2.bitwise_and(image, mask_3ch)
        return masked_image
        
    def process_dataset(self, split):
        """
        Process images and labels for a specific split (train/valid/test)
        
        Args:
            split (str): Dataset split to process ('train', 'valid', or 'test')
        """
        images_dir = self.base_dir / split / 'images'
        labels_dir = self.base_dir / split / 'labels'
        
        if not images_dir.exists() or not labels_dir.exists():
            print(f"Directory not found: {split}")
            return
            
        # Process all images in the split
        for img_path in tqdm(list(images_dir.glob('*')), desc=f'Processing {split}'):
            # Read image
            image = cv2.imread(str(img_path))
            if image is None:
                print(f"Failed to read image: {img_path}")
                continue
                
            # Get corresponding label file
            label_path = labels_dir / f"{img_path.stem}.txt"
            
            # Read polygon annotations
            polygons = self.read_yolo_polygon(label_path, image.shape[1], image.shape[0])
            
            # Process each polygon in the image
            for class_id, polygon_points in polygons:
                # Create mask
                mask = self.create_mask(image.shape, polygon_points)
                
                # Apply mask to get burn region
                masked_image = self.apply_mask(image, mask)
                
                # Save masked image in appropriate degree folder
                output_path = self.degree_dirs[class_id] / f"{img_path.stem}_{class_id}{img_path.suffix}"
                cv2.imwrite(str(output_path), masked_image)

def main():
    # Set paths
    base_dir = Path('<PROJECT_ROOT>/code/dataset/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8')
    output_dir = Path('<PROJECT_ROOT>/code/dataset/New-Way/CNN-DatasetM')
    
    # Initialize mask generator
    generator = MaskGenerator(base_dir, output_dir)
    
    # Process each split
    for split in ['train', 'valid', 'test']:
        generator.process_dataset(split)
        
    print("Processing completed. Masked images saved to:", output_dir)

if __name__ == "__main__":
    main()