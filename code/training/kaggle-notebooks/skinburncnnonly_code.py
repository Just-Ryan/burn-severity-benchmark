# Install required packages (if not already installed)
!pip install -q tensorflow matplotlib seaborn scikit-learn

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import NASNetMobile
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import os

# Check TensorFlow and Keras versions
print("TensorFlow version:", tf.__version__)
print("Keras version:", tf.keras.__version__)

# Define the dataset directory.
# Your dataset has four folders, but we want to exclude "No Sunburn".
dataset_dir = "/kaggle/input/cnndataset2/Dataset"

# Specify the classes to use (exclude "No Sunburn")
classes_to_use = ["First Degree Burn", "Second Degree Burn", "Third Degree Burn"]

# Image and training parameters
img_size = (224, 224)
batch_size = 64

# Create ImageDataGenerator with a 20% validation split.
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Training generator: load only the specified classes.
train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=classes_to_use,
    class_mode='sparse',  # integer-encoded labels
    subset='training',
    shuffle=True
)

# Validation generator: same classes, no shuffling.
validation_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=classes_to_use,
    class_mode='sparse',
    subset='validation',
    shuffle=False
)

# Build the model using NASNetMobile as the base.
# Freeze the base model for initial training.
base_model = NASNetMobile(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Create the classifier model.
# Note: The output layer now has 3 units (one for each burn class).
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='selu'),
    Dropout(0.5),
    Dense(3, activation='softmax')
])

# Compile the model.
model.compile(optimizer=Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Train the model for 15 epochs.
epochs = 20
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator
)

# Plot Training and Validation Accuracy & Loss
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], 'bo-', label='Train Accuracy')
plt.plot(history.history['val_accuracy'], 'ro-', label='Validation Accuracy')
plt.title('Training & Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], 'bo-', label='Train Loss')
plt.plot(history.history['val_loss'], 'ro-', label='Validation Loss')
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

# Evaluate the model on the validation set.
val_loss, val_accuracy = model.evaluate(validation_generator)
print("Evaluation loss:", val_loss)
print("Evaluation accuracy:", val_accuracy)

# Generate predictions on the validation set.
predictions = model.predict(validation_generator)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = validation_generator.classes

# Get the class names (order corresponds to classes_to_use).
class_names = list(train_generator.class_indices.keys())

# Print the classification report.
print("Classification Report:")
print(classification_report(true_labels, predicted_labels, target_names=class_names))

# Plot the confusion matrix.
conf_mat = confusion_matrix(true_labels, predicted_labels)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_mat, annot=True, fmt="d", cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# Save the trained model in the .keras format.
model.save("nasnet_skin_burn_classification_no_nosunburn.keras")
print("Model saved as nasnet_skin_burn_classification_no_nosunburn.keras")

# Convert the model to TensorFlow Lite format.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("nasnet_skin_burn_classification_no_nosunburn.tflite", "wb") as f:
    f.write(tflite_model)
print("TFLite model saved as nasnet_skin_burn_classification_no_nosunburn.tflite")
