import os
from ultralytics import YOLO
import time
import numpy as np
from pathlib import Path
import cv2

class YOLOBurnEvaluator:
    def __init__(self, model_path, dataset_path, conf_threshold=0.25, iou_threshold=0.5):
        """
        Initialize the YOLO evaluator
        Args:
            model_path: Path to the .pt model file
            dataset_path: Path to the dataset root
            conf_threshold: Confidence threshold for detection
            iou_threshold: IoU threshold for considering a detection as correct
        """
        self.model = YOLO(model_path)
        self.dataset_path = dataset_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # Setup correct paths
        self.images_path = os.path.join(dataset_path, "images", "test")
        self.labels_path = os.path.join(dataset_path, "labels", "test")
        
        # Verify paths exist
        if not os.path.exists(self.images_path):
            raise FileNotFoundError(f"Images path does not exist: {self.images_path}")
        if not os.path.exists(self.labels_path):
            raise FileNotFoundError(f"Labels path does not exist: {self.labels_path}")
        
        # Get image files
        self.image_files = [f for f in os.listdir(self.images_path) 
                          if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"Found {len(self.image_files)} images in {self.images_path}")
    
    def calculate_iou(self, box1, box2):
        """Calculate IoU between two bounding boxes"""
        # Convert YOLO format to x1,y1,x2,y2
        x1 = box1[0] - box1[2]/2
        y1 = box1[1] - box1[3]/2
        x2 = box1[0] + box1[2]/2
        y2 = box1[1] + box1[3]/2
        
        x3 = box2[0] - box2[2]/2
        y3 = box2[1] - box2[3]/2
        x4 = box2[0] + box2[2]/2
        y4 = box2[1] + box2[3]/2
        
        # Calculate intersection
        x_left = max(x1, x3)
        y_top = max(y1, y3)
        x_right = min(x2, x4)
        y_bottom = min(y2, y4)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
            
        intersection = (x_right - x_left) * (y_bottom - y_top)
        
        # Calculate union
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x4 - x3) * (y4 - y3)
        union = box1_area + box2_area - intersection
        
        return intersection / union if union > 0 else 0
    
    def read_yolo_label(self, label_path):
        """Read YOLO format label file"""
        boxes = []
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    # YOLO format: class x_center y_center width height
                    data = line.strip().split()
                    if len(data) == 5 and int(data[0]) == 0:  # Only class 0 (burns)
                        boxes.append([float(x) for x in data[1:]])
        return boxes
    
    def evaluate(self):
        """Evaluate the model on the test dataset"""
        total_gt = 0  # Total ground truth boxes
        total_pred = 0  # Total predicted boxes
        total_correct = 0  # Total correct predictions
        total_time = 0  # Total inference time
        
        results = {
            'precision': 0,
            'recall': 0,
            'f1_score': 0,
            'average_time': 0,
            'processed_images': 0
        }
        
        print(f"Starting evaluation on {len(self.image_files)} images...")
        
        for img_file in self.image_files:
            # Prepare paths
            img_path = os.path.join(self.images_path, img_file)
            label_path = os.path.join(self.labels_path, 
                                    os.path.splitext(img_file)[0] + '.txt')
            
            # Read ground truth boxes
            gt_boxes = self.read_yolo_label(label_path)
            total_gt += len(gt_boxes)
            
            try:
                # Run inference and time it
                start_time = time.time()
                predictions = self.model.predict(img_path, 
                                              conf=self.conf_threshold,
                                              verbose=False)
                end_time = time.time()
                total_time += (end_time - start_time)
                
                # Process predictions
                pred_boxes = []
                for pred in predictions:
                    for box in pred.boxes:
                        if box.conf.item() > self.conf_threshold:
                            # Convert box to YOLO format (x_center, y_center, width, height)
                            x_center = box.xywh[0][0].item() / pred.boxes.orig_shape[1]
                            y_center = box.xywh[0][1].item() / pred.boxes.orig_shape[0]
                            width = box.xywh[0][2].item() / pred.boxes.orig_shape[1]
                            height = box.xywh[0][3].item() / pred.boxes.orig_shape[0]
                            pred_boxes.append([x_center, y_center, width, height])
                
                total_pred += len(pred_boxes)
                
                # Match predictions with ground truth
                for gt_box in gt_boxes:
                    for pred_box in pred_boxes:
                        if self.calculate_iou(gt_box, pred_box) > self.iou_threshold:
                            total_correct += 1
                            break
                
                # Print progress every 10 images
                if (self.image_files.index(img_file) + 1) % 10 == 0:
                    print(f"Processed {self.image_files.index(img_file) + 1}/{len(self.image_files)} images")
                
            except Exception as e:
                print(f"Error processing {img_file}: {str(e)}")
                continue
        
        # Calculate metrics
        processed_images = len(self.image_files)
        precision = total_correct / total_pred if total_pred > 0 else 0
        recall = total_correct / total_gt if total_gt > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        avg_time = (total_time / processed_images * 1000) if processed_images > 0 else 0
        
        results = {
            'precision': precision * 100,
            'recall': recall * 100,
            'f1_score': f1_score * 100,
            'average_time': avg_time,
            'processed_images': processed_images,
            'total_gt_boxes': total_gt,
            'total_pred_boxes': total_pred,
            'total_correct': total_correct
        }
        
        return results

def main():
    # Paths
    model_path = "<PROJECT_ROOT>/code/TestingCompare/YoloAndCNN/best.pt"
    dataset_path = "<PROJECT_ROOT>/code/dataset/Yolo_Dataset/processed_dataset"
    
    # Create evaluator
    try:
        evaluator = YOLOBurnEvaluator(
            model_path=model_path,
            dataset_path=dataset_path,
            conf_threshold=0.25,
            iou_threshold=0.5
        )
        
        # Run evaluation
        print("Starting YOLOv8 Burn Detection Evaluation...")
        results = evaluator.evaluate()
        
        # Print results
        print("\nEvaluation Results:")
        print("-" * 50)
        print(f"Precision: {results['precision']:.2f}%")
        print(f"Recall: {results['recall']:.2f}%")
        print(f"F1-Score: {results['f1_score']:.2f}%")
        print(f"Average inference time: {results['average_time']:.2f}ms per image")
        print(f"Total images processed: {results['processed_images']}")
        print(f"Total ground truth boxes: {results['total_gt_boxes']}")
        print(f"Total predicted boxes: {results['total_pred_boxes']}")
        print(f"Total correct detections: {results['total_correct']}")
        print("-" * 50)
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please verify that the following paths exist:")
        print(f"- Dataset path: {dataset_path}")
        print(f"- Model path: {model_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()