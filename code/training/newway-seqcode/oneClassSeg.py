import os
from pathlib import Path
import shutil
from tqdm import tqdm

class LabelRemapper:
    def __init__(self, input_dir, output_dir):
        """
        Initialize the label remapper
        
        Args:
            input_dir (str): Path to the original YOLOv8 dataset directory
            output_dir (str): Path to save the remapped dataset
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory structure
        for split in ['train', 'valid', 'test']:
            (self.output_dir / split / 'images').mkdir(parents=True, exist_ok=True)
            (self.output_dir / split / 'labels').mkdir(parents=True, exist_ok=True)

    def remap_label_file(self, label_path, output_path):
        """
        Remap class labels in a label file to 0
        
        Args:
            label_path (Path): Path to the original label file
            output_path (Path): Path to save the remapped label file
        """
        try:
            with open(label_path, 'r') as f_in, open(output_path, 'w') as f_out:
                for line in f_in:
                    # Split the line into values
                    values = line.strip().split()
                    if len(values) < 7:  # Need at least class + 3 points (7 values)
                        continue
                    
                    # Replace class id with 0, keep coordinates unchanged
                    values[0] = '0'
                    
                    # Write remapped line
                    f_out.write(' '.join(values) + '\n')
                    
        except Exception as e:
            print(f"Error processing {label_path}: {str(e)}")

    def process_split(self, split):
        """
        Process a dataset split (train/valid/test)
        
        Args:
            split (str): Dataset split to process
        """
        # Setup paths
        input_images = self.input_dir / split / 'images'
        input_labels = self.input_dir / split / 'labels'
        output_images = self.output_dir / split / 'images'
        output_labels = self.output_dir / split / 'labels'
        
        if not input_images.exists() or not input_labels.exists():
            print(f"Directory not found: {split}")
            return
        
        # Process all images and labels
        image_files = list(input_images.glob('*'))
        for img_path in tqdm(image_files, desc=f'Processing {split}'):
            # Copy image
            shutil.copy2(img_path, output_images / img_path.name)
            
            # Remap and copy label if it exists
            label_path = input_labels / f"{img_path.stem}.txt"
            if label_path.exists():
                output_label_path = output_labels / f"{img_path.stem}.txt"
                self.remap_label_file(label_path, output_label_path)

    def verify_conversion(self):
        """
        Verify the conversion by checking file counts and sampling labels
        
        Returns:
            dict: Statistics about the conversion
        """
        stats = {'total_processed': 0, 'errors': 0}
        
        for split in ['train', 'valid', 'test']:
            input_count = len(list((self.input_dir / split / 'images').glob('*'))) if (self.input_dir / split / 'images').exists() else 0
            output_count = len(list((self.output_dir / split / 'images').glob('*'))) if (self.output_dir / split / 'images').exists() else 0
            
            stats[f'{split}_input_files'] = input_count
            stats[f'{split}_output_files'] = output_count
            stats['total_processed'] += output_count
            
            if input_count != output_count:
                stats['errors'] += 1
                print(f"Warning: File count mismatch in {split}")
                print(f"Input: {input_count}, Output: {output_count}")
        
        return stats

def main():
    # Set paths
    input_dir = Path('<PROJECT_ROOT>/code/dataset/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_3Class')
    output_dir = Path('<PROJECT_ROOT>/code/dataset/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_1Class')
    
    # Initialize remapper
    remapper = LabelRemapper(input_dir, output_dir)
    
    # Process each split
    for split in ['train', 'valid', 'test']:
        remapper.process_split(split)
    
    # Verify conversion
    stats = remapper.verify_conversion()
    
    print("\nProcessing completed!")
    print(f"Total files processed: {stats['total_processed']}")
    print(f"Output directory: {output_dir}")
    
    # Create data.yaml for the new dataset
    yaml_content = f"""path: {output_dir}
train: train/images
val: valid/images
test: test/images

nc: 1  # number of classes
names: ['burn']  # class names
"""
    
    with open(output_dir / 'data.yaml', 'w') as f:
        f.write(yaml_content)
    
    print("\ndata.yaml created with single class configuration")

if __name__ == "__main__":
    main()