# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from sklearn.metrics import classification_report
import numpy as np

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

# Enable GPU acceleration
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Define paths to the dataset
base_dir = "/kaggle/input/cnndataset/Dataset"
classes = ["First Degree Burn", "Second Degree Burn", "Third Degree Burn", "No Sunburn"]

# Load and preprocess data with advanced augmentation
def load_data(base_dir, classes, img_size=(224, 224), batch_size=32):
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,  # Normalize pixel values to [0, 1]
        rotation_range=20,     # Randomly rotate images
        width_shift_range=0.2, # Randomly shift images horizontally
        height_shift_range=0.2, # Randomly shift images vertically
        shear_range=0.2,       # Apply shear transformations
        zoom_range=0.2,        # Randomly zoom images
        horizontal_flip=True,  # Randomly flip images horizontally
        vertical_flip=True,    # Randomly flip images vertically
        validation_split=0.2   # 20% of data for validation
    )

    train_generator = train_datagen.flow_from_directory(
        base_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,  # Normalize pixel values to [0, 1]
        validation_split=0.2   # 20% of data for validation
    )

    val_generator = val_datagen.flow_from_directory(
        base_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    return train_generator, val_generator

# Load uncropped data
train_generator, val_generator = load_data(base_dir, classes)

# Build the model using DenseNet121
def build_model(input_shape=(224, 224, 3), num_classes=4):
    base_model = DenseNet121(
        include_top=False,
        weights='imagenet',
        input_shape=input_shape
    )
    base_model.trainable = True  # Fine-tune the entire model

    # Add custom layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)  # Add batch normalization
    x = Dropout(0.5)(x)          # Add dropout to prevent overfitting
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

# Compile the model
model = build_model()
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Add learning rate scheduler and early stopping
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=3,
    min_lr=1e-6,
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# Train the model
epochs = 50  # Increase epochs for better training
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=val_generator,
    validation_steps=val_generator.samples // val_generator.batch_size,
    epochs=epochs,
    callbacks=[reduce_lr, early_stopping],
    verbose=1
)

# Evaluate the model
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

# Generate predictions
y_pred = model.predict(val_generator)
y_pred = np.argmax(y_pred, axis=1)
y_true = val_generator.classes

# Classification Report
class_names = list(val_generator.class_indices.keys())
print("Classification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))

# Save the model
model.save("uncropped_burn_model_densenet121_optimized.h5")