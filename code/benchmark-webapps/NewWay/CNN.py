import torch
from torchvision import transforms
import timm
from PIL import Image
import os
import time
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import cv2

class BurnClassifier:
    def __init__(self, model_path):
        """Initialize the burn classifier with Swin Small"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Initialize Swin Small model
        self.model = timm.create_model('swin_small_patch4_window7_224', pretrained=False, num_classes=3)
        
        # Load trained weights
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Standardized image transformations - matching the normalization used in all models
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Fixed resize for consistency
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        
        self.classes = ['First', 'Second', 'Third']

    def preprocess_image(self, image_path):
        """Preprocess a single image with standardized transformations"""
        try:
            image = Image.open(image_path).convert('RGB')
            # Save original image for visualization
            original_img = np.array(image)
            # Transform for model
            transformed_img = self.transform(image).unsqueeze(0)
            return transformed_img, original_img
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {str(e)}")
            return None, None

    @torch.no_grad()
    def predict_single(self, image_path):
        """Make prediction for a single image with confidence score using consistent timing"""
        try:
            # Start timing
            start_time = time.time()
            
            # Preprocess image
            image_tensor, original_img = self.preprocess_image(image_path)
            if image_tensor is None:
                return None, None, 0, None
            
            # Forward pass
            image_tensor = image_tensor.to(self.device)
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            # End timing
            inference_time = time.time() - start_time
            
            return predicted.item(), confidence.item(), inference_time, original_img
            
        except Exception as e:
            print(f"Error in prediction for {image_path}: {str(e)}")
            return None, None, 0, None

    def evaluate_dataset(self, test_dir):
        """Evaluate model on test dataset with detailed metrics"""
        results = {
            'predictions': [],
            'labels': [],
            'processing_times': [],
            'confidence_scores': [],
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
                    # Preprocess and predict
                    pred_class, confidence, inference_time, original_img = self.predict_single(img_path)
                    
                    if pred_class is None:
                        continue
                        
                    successful_processes += 1
                    
                    # Record results
                    results['predictions'].append(pred_class)
                    results['labels'].append(class_idx)
                    results['processing_times'].append(inference_time)
                    results['confidence_scores'].append(confidence)
                    
                    # Store example images (first 2 of each class)
                    if len([img for img in results['example_images'] if img['true_class'] == class_name]) < 2:
                        results['example_images'].append({
                            'image': original_img,
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
                            'confidence': confidence
                        })
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
                    continue
        
        # Calculate success rate (% of images that could be processed)
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
        plt.title('Swin Small CNN - Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix_cnn.png')
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
            plt.savefig('cnn_examples.png')
            plt.close(fig)
        
        # Compile all results
        metrics = {
            'accuracy': accuracy,
            'success_rate': results['success_rate'],
            'average_inference_time': avg_time,
            'average_confidence': avg_confidence,
            'per_class_accuracy': per_class_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'processing_times': results['processing_times'],
            'confidence_scores': results['confidence_scores'],
            'errors': results['errors']
        }
        
        return metrics

def print_results(results):
    """Print evaluation results in a detailed, formatted way"""
    print("\n" + "="*50)
    print("SWIN SMALL CNN EVALUATION RESULTS")
    print("="*50)
    
    print(f"\nOverall Accuracy: {results['accuracy']*100:.2f}%")
    print(f"Success Rate: {results['success_rate']*100:.2f}%")
    print(f"Average Inference Time: {results['average_inference_time']*1000:.2f} ms")
    print(f"Average Confidence Score: {results['average_confidence']*100:.2f}%")
    
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
        print(f"Confidence: {error['confidence']*100:.2f}%\n")

def main():
    # Model and data paths - these will need to be updated with your actual paths
    model_path = '<PROJECT_ROOT>/code/dataset/New-Way/CNN-DatasetNM/best_cnn_full.pth'
    test_dir = '<PROJECT_ROOT>/code/TestingCompare/TestingDataset2'
    
    # Initialize classifier
    classifier = BurnClassifier(model_path)
    
    # Run evaluation
    results = classifier.evaluate_dataset(test_dir)
    
    # Print results
    print_results(results)
    
    print("\nVisualization results:")
    print("- Confusion matrix saved as 'confusion_matrix_cnn.png'")
    print("- Example predictions saved as 'cnn_examples.png'")

if __name__ == "__main__":
    main()