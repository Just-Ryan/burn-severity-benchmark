import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from PIL import Image
import numpy as np
import os
import time

class StandaloneCNN:
    def __init__(self, model_path):
        print(f"Initializing model from: {model_path}")
        
        try:
            # Try direct model loading first
            custom_objects = {
                'relu': tf.keras.activations.relu,
                'softmax': tf.keras.activations.softmax,
                'selu': tf.keras.activations.selu
            }
            self.model = load_model(model_path, custom_objects=custom_objects, compile=False)
            print("Model loaded successfully via direct loading")
        except Exception as e:
            print(f"Direct loading failed: {str(e)}")
            print("Attempting alternative loading method...")
            
            try:
                # Create model with imagenet weights first
                base_model = MobileNet(
                    weights='imagenet',
                    include_top=False,
                    input_shape=(224, 224, 3)
                )
                
                # Create custom top layers
                x = base_model.output
                x = GlobalAveragePooling2D()(x)
                x = Dense(64, activation='relu')(x)
                x = Dense(128, activation='selu')(x)
                predictions = Dense(4, activation='softmax')(x)
                
                self.model = Model(inputs=base_model.input, outputs=predictions)
                
                # Load the weights from saved model
                try:
                    self.model.load_weights(model_path)
                    print("Model weights loaded successfully")
                except Exception as weight_error:
                    print(f"Weight loading failed: {str(weight_error)}")
                    print("Using ImageNet weights as fallback")
            except Exception as model_error:
                print(f"Model creation failed: {str(model_error)}")
                raise
        
        self.classes = ['First Degree Burn', 'Second Degree Burn', 'Third Degree Burn', 'No Burn']
    
    def process_image(self, image_path):
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image)
            image_array = image_array / 255.0  # Simple normalization
            image_array = np.expand_dims(image_array, axis=0)
            
            # Make prediction
            predictions = self.model.predict(image_array, verbose=0)
            predicted_class = np.argmax(predictions[0])
            
            return self.classes[predicted_class]
            
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            raise

def evaluate_system(system, test_folders):
    total_images = 0
    correct_predictions = 0
    total_time = 0
    class_stats = {cls: {'correct': 0, 'total': 0} for cls in system.classes}
    
    print("\nStarting evaluation...")
    
    for class_idx, folder in enumerate(test_folders):
        print(f"\nProcessing folder: {folder}")
        current_class = system.classes[class_idx]
        
        for image_name in os.listdir(folder):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder, image_name)
                
                try:
                    start_time = time.time()
                    predicted_class = system.process_image(image_path)
                    end_time = time.time()
                    
                    total_time += (end_time - start_time)
                    total_images += 1
                    class_stats[current_class]['total'] += 1
                    
                    if system.classes.index(predicted_class) == class_idx:
                        correct_predictions += 1
                        class_stats[current_class]['correct'] += 1
                    
                    if total_images % 10 == 0:
                        print(f"Processed {total_images} images...")
                
                except Exception as e:
                    print(f"Skipping image {image_name} due to error: {str(e)}")
                    continue
    
    if total_images > 0:
        accuracy = correct_predictions / total_images
        avg_time_per_image = total_time / total_images
        
        print("\nEvaluation Results:")
        print("==================")
        print(f"Total images processed: {total_images}")
        print(f"Correct predictions: {correct_predictions}")
        print(f"Overall Accuracy: {accuracy:.4f}")
        print(f"Average processing time: {avg_time_per_image:.4f} seconds")
        
        print("\nPer-Class Performance:")
        print("=====================")
        for cls in system.classes:
            if class_stats[cls]['total'] > 0:
                class_acc = class_stats[cls]['correct'] / class_stats[cls]['total']
                print(f"{cls}: {class_acc:.4f} ({class_stats[cls]['correct']}/{class_stats[cls]['total']})")
    else:
        print("No images were processed successfully.")

def main():
    print("\nChecking environment...")
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Eager execution: {tf.executing_eagerly()}")
    
    cnn_path = '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/CNN_Dataset/MobileNetresults/burn_classification_model.keras'
    test_folders = [
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/First',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/Second',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/Third',
        '/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/TestingCompare/TestingDataset/NoBurn'
    ]
    
    print("\nVerifying paths...")
    print(f"Model file exists: {os.path.exists(cnn_path)}")
    for folder in test_folders:
        print(f"Test folder exists: {folder} - {os.path.exists(folder)}")
    
    try:
        standalone_system = StandaloneCNN(cnn_path)
        evaluate_system(standalone_system, test_folders)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()