from ultralytics import YOLO
import torch
import numpy as np
import time
import os
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import cv2

class YOLOSegmentationBenchmark:
    def __init__(self, model_path):
        """Initialize YOLOv8 segmentation model with consistent settings"""
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        
        # Load YOLOv8 model
        self.model = YOLO(model_path)
        self.classes = ['First', 'Second', 'Third']
        
        # Image size - ensuring consistency across all models
        self.img_size = 640  # Default YOLO image size
        
    def predict_single(self, image_path):
        """Make prediction for a single image with consistent preprocessing"""
        try:
            # Start timing
            start_time = time.time()
            
            # Run inference
            results = self.model(image_path, imgsz=self.img_size, verbose=False)
            result = results[0]  # Get first result
            
            # Get prediction data
            if len(result.boxes) == 0:
                return None, None, None, 0
            
            # Get the highest confidence prediction
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            masks = result.masks.data.cpu().numpy() if result.masks is not None else None
            
            # Get the index of highest confidence prediction
            max_conf_idx = np.argmax(confidences)
            
            # Calculate inference time
            inference_time = time.time() - start_time
            
            # For visualization (save top 5 examples)
            original_img = cv2.imread(image_path)
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            return (class_ids[max_conf_idx], 
                    confidences[max_conf_idx],
                    masks[max_conf_idx] if masks is not None else None,
                    inference_time,
                    original_img)
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return None, None, None, 0, None

    def evaluate_dataset(self, test_dir):
        """Evaluate model on test dataset with standardized metrics"""
        results = {
            'predictions': [],
            'labels': [],
            'processing_times': [],
            'confidence_scores': [],
            'mask_areas': [],
            'per_class_counts': {cls: 0 for cls in self.classes},
            'per_class_correct': {cls: 0 for cls in self.classes},
            'errors': [],
            'example_images': []  # Store some example predictions for visualization
        }
        
        total_images = 0
        successful_processes = 0
        
        print("\nStarting evaluation...")
        
        # Process each class directory
        for class_idx, class_name in enumerate(self.classes):
            class_path = os.path.join(test_dir, class_name)
            if not os.path.exists(class_path):
                print(f"Warning: Directory not found - {class_path}")
                continue
                
            print(f"\nProcessing {class_name} images...")
            
            # Process each image in the class directory
            for img_name in os.listdir(class_path):
                if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                
                total_images += 1
                img_path = os.path.join(class_path, img_name)
                results['per_class_counts'][class_name] += 1
                
                try:
                    # Get prediction
                    pred_class, confidence, mask, inference_time, original_img = self.predict_single(img_path)
                    
                    if pred_class is None:
                        continue
                    
                    successful_processes += 1
                    
                    # Calculate mask area if mask exists
                    mask_area = np.sum(mask) if mask is not None else 0
                    
                    # Record results
                    results['predictions'].append(pred_class)
                    results['labels'].append(class_idx)
                    results['processing_times'].append(inference_time)
                    results['confidence_scores'].append(confidence)
                    results['mask_areas'].append(mask_area)
                    
                    # Store example images (first 5 of each class)
                    if len([img for img in results['example_images'] if img['true_class'] == class_name]) < 2:
                        # Create visualization with mask if available
                        vis_img = original_img.copy()
                        if mask is not None:
                            # Resize mask to match image
                            resized_mask = cv2.resize(mask, (vis_img.shape[1], vis_img.shape[0]))
                            # Apply a colored overlay for the mask
                            mask_overlay = np.zeros_like(vis_img)
                            mask_overlay[resized_mask > 0.5] = [0, 255, 0]  # Green overlay
                            vis_img = cv2.addWeighted(vis_img, 1.0, mask_overlay, 0.5, 0)
                            
                        results['example_images'].append({
                            'image': vis_img,
                            'true_class': class_name,
                            'pred_class': self.classes[pred_class],
                            'confidence': confidence,
                            'correct': pred_class == class_idx
                        })
                    
                    # Track correct predictions per class
                    if pred_class == class_idx:
                        results['per_class_correct'][class_name] += 1
                    else:
                        # Record error details
                        results['errors'].append({
                            'image': img_path,
                            'true': class_name,
                            'predicted': self.classes[pred_class],
                            'confidence': confidence,
                            'mask_area': mask_area
                        })
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
                    continue
        
        results['success_rate'] = successful_processes / total_images if total_images > 0 else 0
        
        return self.compute_metrics(results)

    def compute_metrics(self, results):
        """Compute comprehensive evaluation metrics"""
        predictions = np.array(results['predictions'])
        labels = np.array(results['labels'])
        
        # Basic metrics
        accuracy = np.mean(predictions == labels)
        avg_time = np.mean(results['processing_times'])
        avg_confidence = np.mean(results['confidence_scores'])
        avg_mask_area = np.mean(results['mask_areas'])
        
        # Per-class accuracy
        per_class_accuracy = {
            cls: results['per_class_correct'][cls] / max(results['per_class_counts'][cls], 1)
            for cls in self.classes
        }
        
        # Detailed classification report
        report = classification_report(labels, predictions, 
                                    target_names=self.classes, 
                                    output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(labels, predictions)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.classes,
                   yticklabels=self.classes)
        plt.title('YOLOv8-Seg (3-Class) - Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix_yolo_seg.png')
        plt.close()
        
        # Save example images
        if results['example_images']:
            fig, axs = plt.subplots(len(results['example_images']), 1, figsize=(8, 4*len(results['example_images'])))
            for i, img_data in enumerate(results['example_images']):
                axs[i].imshow(img_data['image'])
                correct_mark = "✓" if img_data['correct'] else "✗"
                axs[i].set_title(f"{correct_mark} True: {img_data['true_class']}, Pred: {img_data['pred_class']}\n" 
                                f"Confidence: {img_data['confidence']*100:.2f}%")
                axs[i].axis('off')
            plt.tight_layout()
            plt.savefig('yolo_seg_examples.png')
            plt.close(fig)
        
        # Compile all results
        metrics = {
            'accuracy': accuracy,
            'success_rate': results['success_rate'],
            'average_inference_time': avg_time,
            'average_confidence': avg_confidence,
            'average_mask_area': avg_mask_area,
            'per_class_accuracy': per_class_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'processing_times': results['processing_times'],
            'confidence_scores': results['confidence_scores'],
            'mask_areas': results['mask_areas'],
            'errors': results['errors']
        }
        
        return metrics

def print_results(results):
    """Print evaluation results in a detailed, formatted way"""
    print("\n" + "="*50)
    print("YOLOV8 SEGMENTATION (3-CLASS) EVALUATION RESULTS")
    print("="*50)
    
    print(f"\nOverall Accuracy: {results['accuracy']*100:.2f}%")
    print(f"Success Rate: {results['success_rate']*100:.2f}%")
    print(f"Average Inference Time: {results['average_inference_time']*1000:.2f} ms")
    print(f"Average Confidence Score: {results['average_confidence']*100:.2f}%")
    print(f"Average Mask Area: {results['average_mask_area']:.2f} pixels")
    
    print("\nPer-Class Performance:")
    print("-"*50)
    report = results['classification_report']
    
    for class_name in ['First', 'Second', 'Third']:
        metrics = report[class_name]
        print(f"\n{class_name} Degree Burns:")
        print(f"  Precision: {metrics['precision']*100:.2f}%")
        print(f"  Recall: {metrics['recall']*100:.2f}%")
        print(f"  F1-Score: {metrics['f1-score']*100:.2f}%")
        print(f"  Support: {metrics['support']}")
    
    print("\nMost Challenging Cases:")
    print("-"*50)
    errors = sorted(results['errors'], key=lambda x: x['confidence'], reverse=True)[:5]
    for error in errors:
        print(f"Image: {os.path.basename(error['image'])}")
        print(f"True: {error['true']}, Predicted: {error['predicted']}")
        print(f"Confidence: {error['confidence']*100:.2f}%")
        print(f"Mask Area: {error['mask_area']:.2f} pixels\n")

def main():
    # Model and data paths - these will need to be updated with your actual paths
    model_path = '<PROJECT_ROOT>/code/dataset/New-Way/Seqmentation-Dataset/results3Class/runs/segment/train/weights/best.pt'
    test_dir = '<PROJECT_ROOT>/code/TestingCompare/TestingDataset'
    
    # Initialize benchmark
    benchmark = YOLOSegmentationBenchmark(model_path)
    
    # Run evaluation
    results = benchmark.evaluate_dataset(test_dir)
    
    # Print results
    print_results(results)
    
    print("\nVisualization results:")
    print("- Confusion matrix saved as 'confusion_matrix_yolo_seg.png'")
    print("- Example predictions saved as 'yolo_seg_examples.png'")

if __name__ == "__main__":
    main()