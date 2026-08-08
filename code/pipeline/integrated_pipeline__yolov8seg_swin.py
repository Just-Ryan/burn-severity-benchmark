import torch
import cv2
import numpy as np
from ultralytics import YOLO
import timm
from PIL import Image
import time
import os
from torchvision import transforms
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

class IntegratedBurnAnalyzer:
    def __init__(self, yolo_path, cnn_path):
        """Initialize both models with standardized settings"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Initialize YOLOv8-Seg (1-class) - for burn region segmentation only
        self.yolo_model = YOLO(yolo_path)
        self.yolo_img_size = 640  # Default YOLO image size
        
        # Initialize Swin Small model - for burn severity classification
        self.cnn_model = timm.create_model('swin_small_patch4_window7_224', pretrained=False, num_classes=3)
        self.cnn_model.load_state_dict(torch.load(cnn_path, map_location=self.device))
        self.cnn_model = self.cnn_model.to(self.device)
        self.cnn_model.eval()
        
        # Updated transformations based on the second implementation
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self.classes = ['First', 'Second', 'Third']

    def segment_burn(self, image_path):
        """Detect and segment burn region using YOLOv8-Seg with consistent preprocessing"""
        try:
            # Start timing for segmentation
            seg_start_time = time.time()
            
            # Load original image
            original_img = cv2.imread(image_path)
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            # Run YOLO inference with fixed size
            results = self.yolo_model(image_path, imgsz=self.yolo_img_size, verbose=False)
            result = results[0]
            
            # Calculate segmentation time
            seg_time = time.time() - seg_start_time
            
            if len(result.boxes) == 0:
                return None, None, seg_time, original_img, None
            
            # Get highest confidence detection
            confidences = result.boxes.conf.cpu().numpy()
            max_conf_idx = np.argmax(confidences)
            confidence = confidences[max_conf_idx]
            
            # Get mask
            if result.masks is not None:
                mask = result.masks.data[max_conf_idx].cpu().numpy()
                
                # Resize mask to match image
                mask = cv2.resize(mask, (original_img.shape[1], original_img.shape[0]))
                
                # Create masked image with improved threshold from second implementation
                masked_image = original_img.copy()
                mask_binary = (mask > 0.1).astype(np.uint8)  # Threshold 0.1 (matches deployed Flask + paper)
                masked_image = masked_image * mask_binary[:, :, np.newaxis]
                
                # Create visualization for reporting
                mask_overlay = np.zeros_like(original_img)
                mask_overlay[mask_binary > 0] = [0, 255, 0]  # Green mask overlay
                visualization = cv2.addWeighted(original_img, 1.0, mask_overlay, 0.5, 0)
                
                return masked_image, confidence, seg_time, original_img, visualization
            
            return None, None, seg_time, original_img, None
            
        except Exception as e:
            print(f"Error in segmentation for {image_path}: {str(e)}")
            return None, None, 0, None, None

    @torch.no_grad()
    def classify_burn(self, masked_image):
        """Classify burn severity using CNN with improved preprocessing and temperature scaling"""
        try:
            # Start timing for classification
            class_start_time = time.time()
            
            # Convert numpy array to PIL Image
            image = Image.fromarray(masked_image)
            
            # Apply CNN-specific transformations (updated from second implementation)
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Get prediction with temperature scaling from second implementation
            outputs = self.cnn_model(image_tensor)
            temperature = 1.5  # Added temperature scaling from second implementation
            scaled_outputs = outputs / temperature
            probabilities = torch.nn.functional.softmax(scaled_outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            # Calculate classification time
            class_time = time.time() - class_start_time
            
            return predicted.item(), confidence.item(), class_time
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return None, 0, 0

    def analyze_image(self, image_path):
        """Complete analysis pipeline for a single image"""
        try:
            total_start_time = time.time()
            
            # Step 1: Segmentation
            masked_image, seg_confidence, seg_time, original_img, visualization = self.segment_burn(image_path)
            
            if masked_image is None:
                return None, None, None, 0, None, None, None
            
            # Step 2: Classification
            class_pred, class_confidence, class_time = self.classify_burn(masked_image)
            
            if class_pred is None:
                return None, None, None, 0, None, None, None
                
            # Calculate total time
            total_time = time.time() - total_start_time
            
            return class_pred, class_confidence, seg_confidence, total_time, masked_image, original_img, visualization
            
        except Exception as e:
            print(f"Error in pipeline for {image_path}: {str(e)}")
            return None, None, None, 0, None, None, None

    def evaluate_dataset(self, test_dir):
        """Evaluate complete pipeline on test dataset with standardized metrics"""
        results = {
            'predictions': [],
            'labels': [],
            'total_processing_times': [],
            'seg_times': [],
            'class_times': [],
            'seg_confidences': [],
            'class_confidences': [],
            'per_class_counts': {cls: 0 for cls in self.classes},
            'per_class_correct': {cls: 0 for cls in self.classes},
            'errors': [],
            'example_images': []
        }
        
        total_images = 0
        successful_processes = 0
        
        print("\nStarting evaluation...")
        
        for class_idx, class_name in enumerate(self.classes):
            class_path = os.path.join(test_dir, class_name)
            if not os.path.exists(class_path):
                print(f"Warning: Directory not found - {class_path}")
                continue
                
            print(f"\nProcessing {class_name} images...")
            
            for img_name in os.listdir(class_path):
                if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                    
                total_images += 1
                img_path = os.path.join(class_path, img_name)
                results['per_class_counts'][class_name] += 1
                
                try:
                    # Run full analysis pipeline
                    pred_class, class_conf, seg_conf, total_time, masked_img, original_img, visualization = self.analyze_image(img_path)
                    
                    if pred_class is not None:
                        successful_processes += 1
                        
                        # Record all results
                        results['predictions'].append(pred_class)
                        results['labels'].append(class_idx)
                        results['total_processing_times'].append(total_time)
                        results['seg_confidences'].append(seg_conf)
                        results['class_confidences'].append(class_conf)
                        
                        # Store example images (first 2 of each class)
                        if len([img for img in results['example_images'] if img['true_class'] == class_name]) < 2:
                            results['example_images'].append({
                                'original': original_img,
                                'masked': masked_img,
                                'visualization': visualization,
                                'true_class': class_name,
                                'pred_class': self.classes[pred_class],
                                'seg_confidence': seg_conf,
                                'class_confidence': class_conf,
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
                                'seg_confidence': seg_conf,
                                'class_confidence': class_conf
                            })
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
                    continue
        
        results['success_rate'] = successful_processes / total_images if total_images > 0 else 0
        
        return self.compute_metrics(results)

    def compute_metrics(self, results):
        """Compute comprehensive evaluation metrics"""
        if not results['predictions']:
            print("No valid predictions to evaluate.")
            return {
                'accuracy': 0,
                'success_rate': 0,
                'average_processing_time': 0,
                'average_seg_confidence': 0,
                'average_class_confidence': 0
            }
            
        predictions = np.array(results['predictions'])
        labels = np.array(results['labels'])
        
        # Basic metrics
        accuracy = np.mean(predictions == labels)
        avg_time = np.mean(results['total_processing_times'])
        avg_seg_conf = np.mean(results['seg_confidences'])
        avg_class_conf = np.mean(results['class_confidences'])
        
        # Per-class accuracy
        per_class_accuracy = {
            cls: results['per_class_correct'][cls] / max(results['per_class_counts'][cls], 1)
            for cls in self.classes
        }
        
        # Detailed classification report
        report = classification_report(
            labels, 
            predictions, 
            target_names=self.classes, 
            output_dict=True
        )
        
        # Confusion matrix
        cm = confusion_matrix(labels, predictions)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, 
                   annot=True, 
                   fmt='d', 
                   cmap='Blues',
                   xticklabels=self.classes,
                   yticklabels=self.classes)
        plt.title('Integrated Pipeline - Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix_integrated.png')
        plt.close()
        
        # Save example images
        if results['example_images']:
            # Create figure with 3 columns (original, masked, visualization) for each example
            num_examples = len(results['example_images'])
            fig, axs = plt.subplots(num_examples, 3, figsize=(15, 5*num_examples))
            
            for i, img_data in enumerate(results['example_images']):
                # Original image
                axs[i, 0].imshow(img_data['original'])
                axs[i, 0].set_title("Original Image")
                axs[i, 0].axis('off')
                
                # Masked image (used for classification)
                axs[i, 1].imshow(img_data['masked'])
                axs[i, 1].set_title("Masked Burn Region")
                axs[i, 1].axis('off')
                
                # Visualization with mask overlay
                axs[i, 2].imshow(img_data['visualization'])
                correct_mark = "â" if img_data['correct'] else "â"
                axs[i, 2].set_title(f"{correct_mark} True: {img_data['true_class']}, Pred: {img_data['pred_class']}\n" 
                                   f"Seg Conf: {img_data['seg_confidence']*100:.2f}%, Class Conf: {img_data['class_confidence']*100:.2f}%")
                axs[i, 2].axis('off')
                
            plt.tight_layout()
            plt.savefig('integrated_examples.png')
            plt.close(fig)
        
        # Compile all results
        metrics = {
            'accuracy': accuracy,
            'success_rate': results['success_rate'],
            'average_processing_time': avg_time,
            'average_seg_confidence': avg_seg_conf,
            'average_class_confidence': avg_class_conf,
            'per_class_accuracy': per_class_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'processing_times': results['total_processing_times'],
            'seg_confidences': results['seg_confidences'],
            'class_confidences': results['class_confidences'],
            'errors': results['errors']
        }
        
        return metrics

def print_results(results):
    """Print evaluation results in a detailed, formatted way"""
    print("\n" + "="*50)
    print("INTEGRATED PIPELINE (YOLO-SEG + CNN) EVALUATION RESULTS")
    print("="*50)
    
    print(f"\nOverall Accuracy: {results['accuracy']*100:.2f}%")
    print(f"Success Rate: {results['success_rate']*100:.2f}%")
    print(f"Average Processing Time: {results['average_processing_time']*1000:.2f} ms")
    print(f"Average Segmentation Confidence: {results['average_seg_confidence']*100:.2f}%")
    print(f"Average Classification Confidence: {results['average_class_confidence']*100:.2f}%")
    
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
    
    if results['errors']:
        print("\nMost Challenging Cases:")
        print("-"*50)
        errors = sorted(results['errors'], 
                       key=lambda x: (x['seg_confidence'] + x['class_confidence'])/2, 
                       reverse=True)[:5]
        for error in errors:
            print(f"Image: {os.path.basename(error['image'])}")
            print(f"True: {error['true']}, Predicted: {error['predicted']}")
            print(f"Segmentation Confidence: {error['seg_confidence']*100:.2f}%")
            print(f"Classification Confidence: {error['class_confidence']*100:.2f}%\n")

def main():
    # Model paths
    yolo_path = '<PROJECT_ROOT>/code/dataset/New-Way/Seqmentation-Dataset/results1Class/best.pt'
    cnn_path = '<PROJECT_ROOT>/code/dataset/New-Way/CNN-DatasetM/cnn_compressed_fp16.pth'
    test_dir = '<PROJECT_ROOT>/code/TestingCompare/TestingDataset2'
    
    # Initialize analyzer
    analyzer = IntegratedBurnAnalyzer(yolo_path, cnn_path)
    
    # Run evaluation
    results = analyzer.evaluate_dataset(test_dir)
    
    # Print results
    print_results(results)
    
    print("\nVisualization results:")
    print("- Confusion matrix saved as 'confusion_matrix_integrated.png'")
    print("- Example predictions saved as 'integrated_examples.png'")

if __name__ == "__main__":
    main()