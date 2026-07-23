# Burn AI Flask Server

This Flask server processes burn images using YOLOv8 for segmentation and a CNN model for burn severity classification.

## Setup Instructions

1. **Copy model files from Flutter app assets**:
   - Copy `best.pt` from `<flutter_app_root>/assets/models/` to `flask_server/models/`
   - Copy `cnn_compressed_fp16.pth` from `<flutter_app_root>/assets/models/` to `flask_server/models/`

2. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Running the Server

1. **Start the Flask server**:
   ```
   python app.py
   ```

2. The server will run on `http://0.0.0.0:5000`

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: `{"status": "ok"}`

### Analyze Burn Image
- **URL**: `/analyze`
- **Method**: `POST`
- **Request**: Form data with an image file (key: `image`)
- **Response**:
  ```json
  {
    "success": true,
    "burn_degree": "First/Second/Third Degree Burn",
    "confidence": 0.95,
    "segmentation_confidence": 0.98,
    "segmented_image": "base64_encoded_image"
  }
  ```

## Connecting with Flutter App

The Flutter app is configured to connect to this server at `http://10.0.2.2:5000` when running on an Android emulator. If you're using a physical device or iOS simulator, you'll need to update the server URL in the Flutter app's `BurnAnalyzerService` class.

## Troubleshooting

- If you encounter CUDA-related errors, make sure your PyTorch installation matches your CUDA version or use CPU-only mode.
- If the models fail to load, check that the model files are in the correct location and format.
