from ultralytics import YOLO
import os
import time
import cv2

class StandaloneYOLO:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.classes = ['First Degree Burn', 'Second Degree Burn', 'Third Degree Burn']
        
    def process_image(self, image_path):
        results = self.model(image_path)
        
        # If no detection is made, we'll consider it as "not classified"
        if len(results[0].boxes) == 0:
            return "Not Classified"
            
        # Get the box with highest confidence
        box = results[0].boxes[0]
        class_id = int(box.cls[0])
        return self.classes[class_id]

def evaluate_system(system, test_folders):
    total_images = 0
    correct_predictions = 0
    total_time = 0
    
    for class_idx, folder in enumerate(test_folders):
        folder_name = os.path.basename(folder)
        
        for image_name in os.listdir(folder):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder, image_name)
                
                start_time = time.time()
                predicted_class = system.process_image(image_path)
                end_time = time.time()
                
                total_time += (end_time - start_time)
                total_images += 1
                
                # Handle predictions based on whether it's a burn or no-burn case
                if folder_name == "NoBurn":
                    # For No Burn cases, "Not Classified" is considered correct
                    if predicted_class == "Not Classified":
                        correct_predictions += 1
                else:
                    # For burn cases, check if prediction matches the folder class
                    if predicted_class == system.classes[class_idx]:
                        correct_predictions += 1
    
    accuracy = correct_predictions / total_images
    avg_time_per_image = total_time / total_images
    
    print("\nTesting Results on Unseen Data:")
    print(f"Total images processed: {total_images}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Average time per image: {avg_time_per_image:.4f} seconds")

def main():
    # Initialize the standalone YOLO system
    yolo_path = '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/Yolo_Dataset/resultsYoloV8x/best.pt'
    standalone_system = StandaloneYOLO(yolo_path)
    
    # Define test folders
    test_folders = [
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/First',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/Second',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/Third',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/NoBurn'
    ]
    
    # Evaluate the system
    evaluate_system(standalone_system, test_folders)

if __name__ == "__main__":
    main()
