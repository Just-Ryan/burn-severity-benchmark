import os
import traceback
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import torch
import cv2
from ultralytics import YOLO
import timm
from PIL import Image
import time
from torchvision import transforms
from werkzeug.utils import secure_filename
import uuid

# Important for macOS
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
# Force PyTorch to use a single thread for inference
torch.set_num_threads(1)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULTS_FOLDER'] = 'static/results'

# Make sure upload and results directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

class IntegratedBurnAnalyzer:
    def __init__(self, yolo_path, cnn_path):
        """Initialize both models with standardized settings"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Initialize YOLOv8-Seg (1-class) - for burn region segmentation only
        print(f"Loading YOLO model from: {yolo_path}")
        self.yolo_model = YOLO(yolo_path)
        self.yolo_img_size = 640  # Default YOLO image size
        
        # Initialize Swin Small model - for burn severity classification
        print(f"Loading CNN model from: {cnn_path}")
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
        
        # Treatment advice for each burn degree
        self.treatment_advice = {
            'First': [
                "Cool the burn with cool (not cold) running water for 10 minutes",
                "Take over-the-counter pain relievers if needed",
                "Apply aloe vera gel or moisturizer",
                "Protect the area with a loose bandage if necessary",
                "Do not break blisters"
            ],
            'Second': [
                "Seek medical attention for moderate to severe second-degree burns",
                "Cool the burn under cool running water for 15 minutes",
                "Do not apply ice directly to the burn",
                "Cover with a sterile, non-stick bandage",
                "Do not apply home remedies or ointments without medical guidance",
                "Take over-the-counter pain medication if recommended by a doctor"
            ],
            'Third': [
                "THIS IS A MEDICAL EMERGENCY - Seek immediate medical attention",
                "Call emergency services or go to an emergency room immediately",
                "Do not remove clothing stuck to the burn",
                "Cover the area with a clean, dry cloth or sterile bandage",
                "Do not immerse large severe burns in water",
                "Elevate the burned area above heart level if possible",
                "Monitor for signs of shock until medical help arrives"
            ]
        }
        
        # Severity descriptions
        self.severity_descriptions = {
            'First': "First-degree burns affect only the outer layer of skin. The burn site is red, painful, and may have mild swelling. The skin is dry without blisters.",
            'Second': "Second-degree burns affect both the outer and underlying layer of skin. The burn site appears red, blistered, and may be swollen and painful.",
            'Third': "Third-degree burns extend into deeper tissues. The burn area may appear white, charred, or leathery. There might be little or no pain due to nerve damage."
        }

    def segment_burn(self, image_path):
        """Detect and segment burn region using YOLOv8-Seg with consistent preprocessing"""
        try:
            # Start timing for segmentation
            seg_start_time = time.time()
            
            # Load original image
            original_img = cv2.imread(image_path)
            if original_img is None:
                return None, None, 0, None, None, None
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            # Run YOLO inference with fixed size and safe settings for macOS
            results = self.yolo_model(image_path, imgsz=self.yolo_img_size, verbose=False, 
                                      device=self.device, workers=0)
            result = results[0]
            
            # Calculate segmentation time
            seg_time = time.time() - seg_start_time
            
            if len(result.boxes) == 0:
                return None, None, seg_time, original_img, None, None
            
            # Get highest confidence detection
            confidences = result.boxes.conf.cpu().numpy()
            max_conf_idx = np.argmax(confidences)
            confidence = confidences[max_conf_idx]
            
            # Get mask
            if result.masks is not None:
                mask = result.masks.data[max_conf_idx].cpu().numpy()
                
                # Resize mask to match image
                mask = cv2.resize(mask, (original_img.shape[1], original_img.shape[0]))
                
                # Create masked image with improved threshold
                masked_image = original_img.copy()
                mask_binary = (mask > 0.1).astype(np.uint8)  # Using 0.1 threshold
                masked_image = masked_image * mask_binary[:, :, np.newaxis]
                
                # Create visualization for reporting
                mask_overlay = np.zeros_like(original_img)
                mask_overlay[mask_binary > 0] = [0, 255, 0]  # Green mask overlay
                visualization = cv2.addWeighted(original_img, 1.0, mask_overlay, 0.5, 0)
                
                return masked_image, confidence, seg_time, original_img, visualization, mask_binary
            
            return None, None, seg_time, original_img, None, None
            
        except Exception as e:
            print(f"Error in segmentation for {image_path}: {str(e)}")
            traceback.print_exc()
            return None, None, 0, None, None, None

    @torch.no_grad()
    def classify_burn(self, masked_image):
        """Classify burn severity using CNN with improved preprocessing and temperature scaling"""
        try:
            # Start timing for classification
            class_start_time = time.time()
            
            # Convert numpy array to PIL Image
            image = Image.fromarray(masked_image)
            
            # Apply CNN-specific transformations
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Get prediction with temperature scaling
            outputs = self.cnn_model(image_tensor)
            temperature = 1.5  # Temperature scaling
            scaled_outputs = outputs / temperature
            probabilities = torch.nn.functional.softmax(scaled_outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            # Get all probabilities for visualization
            all_probs = probabilities.cpu().numpy()[0]
            
            # Calculate classification time
            class_time = time.time() - class_start_time
            
            return predicted.item(), confidence.item(), class_time, all_probs
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            traceback.print_exc()
            return None, 0, 0, None

    def analyze_image(self, image_path):
        """Complete analysis pipeline for a single image"""
        try:
            total_start_time = time.time()
            
            # Step 1: Segmentation
            masked_image, seg_confidence, seg_time, original_img, visualization, mask_binary = self.segment_burn(image_path)

            if original_img is None:
                return {
                    'success': False,
                    'error': 'Could not decode the uploaded image'
                }

            # Pipeline fallback: if no burn region is localised, classify the full frame
            used_fallback = False
            if masked_image is None:
                masked_image = original_img
                visualization = original_img
                seg_confidence = 0.0
                used_fallback = True
            
            # Step 2: Classification
            class_pred, class_confidence, class_time, all_probs = self.classify_burn(masked_image)
            
            if class_pred is None:
                return {
                    'success': False,
                    'error': 'Failed to classify the burn'
                }
                
            # Calculate total time
            total_time = time.time() - total_start_time
            
            # Get class name and advice
            predicted_class = self.classes[class_pred]
            treatment_advice = self.treatment_advice[predicted_class]
            description = self.severity_descriptions[predicted_class]
            
            # Save visualization images with absolute path references
            timestamp = int(time.time())
            original_filename = f'original_{timestamp}.jpg'
            masked_filename = f'masked_{timestamp}.jpg'
            visualization_filename = f'visualization_{timestamp}.jpg'
            
            original_path = os.path.join(app.config['RESULTS_FOLDER'], original_filename)
            masked_path = os.path.join(app.config['RESULTS_FOLDER'], masked_filename)
            visualization_path = os.path.join(app.config['RESULTS_FOLDER'], visualization_filename)
            
            # Convert images to PIL format for saving
            Image.fromarray(original_img).save(original_path)
            Image.fromarray(masked_image).save(masked_path)
            Image.fromarray(visualization).save(visualization_path)
            
            
            # Get the base URL for the application
            # Use URLs with /static/ for serving via Flask
            original_url = f"/static/results/{original_filename}"
            masked_url = f"/static/results/{masked_filename}"
            visualization_url = f"/static/results/{visualization_filename}"
            
            print(f"Image saved paths:")
            print(f"  Original: {original_path}")
            print(f"  Masked: {masked_path}")
            print(f"  Visualization: {visualization_path}")
            
            # Convert NumPy values to native Python types for JSON serialization
            class_confidence_float = float(class_confidence)
            seg_confidence_float = float(seg_confidence)
            total_time_float = float(total_time)
            
            # Convert NumPy array to Python list for probabilities
            all_probabilities_dict = {
                self.classes[i]: float(all_probs[i] * 100) for i in range(len(self.classes))
            }
            
            return {
                'success': True,
                'predicted_class': predicted_class,
                'class_confidence': class_confidence_float * 100,  # Convert to percentage
                'seg_confidence': seg_confidence_float * 100,      # Convert to percentage
                'used_fallback': used_fallback,
                'processing_time': total_time_float * 1000,        # Convert to milliseconds
                'original_image': original_url,
                'masked_image': masked_url,
                'visualization': visualization_url,
                'treatment_advice': treatment_advice,
                'description': description,
                'all_probabilities': all_probabilities_dict
            }
            
        except Exception as e:
            print(f"Error in pipeline for {image_path}: {str(e)}")
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }


# Initialize the analyzer with model paths
burn_analyzer = None

def initialize_models():
    global burn_analyzer
    base = os.path.dirname(os.path.abspath(__file__))
    yolo_path = os.path.join(base, 'models', 'best.pt')
    cnn_path = os.path.join(base, 'models', 'cnn_compressed_fp16.pth')
    burn_analyzer = IntegratedBurnAnalyzer(yolo_path, cnn_path)
    print("Models initialized successfully")


# Initialize at import time so the app also works under gunicorn (not only __main__)
initialize_models()

@app.route('/')
def index():
    """Health check endpoint for the API"""
    return jsonify({
        "status": "ok",
        "message": "Burn Analysis API is running"
    })

@app.route('/static/<path:filename>')
def custom_static(filename):
    """Serve static files with proper caching disabled"""
    response = send_from_directory('static', filename)
    # Add cache control headers to prevent caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/analyze', methods=['POST'])
def analyze():
    filepath = None
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'success': False, 'error': 'No image file provided'}), 400

        file = request.files['file']
        filename = secure_filename(f"upload_{uuid.uuid4().hex}.jpg")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = burn_analyzer.analyze_image(filepath)
        status = 200 if result.get('success') else 400
        return jsonify(result), status
    except Exception:
        traceback.print_exc()
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    finally:
        # clean up the uploaded file; results are kept for serving
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=False)