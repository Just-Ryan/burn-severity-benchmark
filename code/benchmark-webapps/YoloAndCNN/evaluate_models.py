

import torch
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('/Users/ryanmacbook/Downloads/مشروع تخرج ١/code/dataset/New-Way/Seqmentation-Dataset/results1Class/best.pt')


# Create example input
example_input = torch.randn(1, 3, 224, 224)

# Export the model to ONNX
# Export the model to CoreML format
model.export(format='coreml')
