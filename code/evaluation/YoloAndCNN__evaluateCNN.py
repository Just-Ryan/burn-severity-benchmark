import matplotlib.pyplot as plt

# Data from your log
epochs = list(range(1, 31))
loss_values = [73.1921, 45.4682, 31.5786, 25.4476, 18.6644, 17.9561, 11.8947, 12.4925, 8.2595, 7.6440,
               6.2298, 6.0448, 9.4595, 5.3583, 4.7426, 3.9128, 3.6099, 2.1496, 4.5985, 1.6493,
               1.2743, 2.1553, 0.9734, 1.6942, 1.5012, 0.9270, 0.9663, 1.3457, None, None]  # last two epochs missing loss

train_acc = [0.7625, 0.8592, 0.8971, 0.9200, 0.9371, 0.9542, 0.9633, 0.9587, 0.9746, 0.9792,
             0.9812, 0.9842, 0.9796, 0.9838, 0.9854, 0.9900, 0.9917, 0.9950, 0.9879, 0.9950,
             0.9958, 0.9950, 0.9975, 0.9962, 0.9954, 0.9967, 0.9962, 0.9962, None, None]

val_acc = [0.8304, 0.8655, 0.8499, 0.8928, 0.8441, 0.8441, 0.8928, 0.9006, 0.8967, 0.8713,
           0.9162, 0.9142, 0.9103, 0.9162, 0.9220, 0.9181, 0.8986, 0.8986, 0.9142, 0.9298,
           0.9318, 0.9181, 0.9376, 0.9318, 0.9376, 0.9298, 0.9279, 0.9181, None, None]

# Remove None entries if present (early stopping)
epochs = epochs[:len([v for v in loss_values if v is not None])]
loss_values = [v for v in loss_values if v is not None]
train_acc = [v for v in train_acc if v is not None]
val_acc = [v for v in val_acc if v is not None]

# Plotting
plt.figure(figsize=(12, 6))

# Loss Curve
plt.subplot(1, 2, 1)
plt.plot(epochs, loss_values, label='Training Loss', color='red', marker='o')
plt.title("Training Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.legend()

# Accuracy Curves
plt.subplot(1, 2, 2)
plt.plot(epochs, train_acc, label='Training Accuracy', color='blue', marker='o')
plt.plot(epochs, val_acc, label='Validation Accuracy', color='green', marker='o')
plt.title("Accuracy over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()