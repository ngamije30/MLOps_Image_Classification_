"""
Train CIFAR-10 model locally and save it for deployment.
This script trains the model on your local machine and saves it to the models/ directory.
"""

import os
import sys
import tensorflow as tf
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.preprocessing import DataPreprocessor
from src.model import ImageClassificationModel
from config import get_config

print("=" * 70)
print("🚀 CIFAR-10 Model Training Script")
print("=" * 70)
print(f"TensorFlow version: {tf.__version__}")
print(f"Training started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Initialize configuration
config = get_config()
config.init_app()

# Initialize preprocessor
print("\n📦 Initializing data preprocessor...")
preprocessor = DataPreprocessor()

# Load and prepare data
print("📥 Loading CIFAR-10 dataset...")
data = preprocessor.prepare_training_data()

print(f"✓ Training samples: {data['X_train'].shape[0]}")
print(f"✓ Test samples: {data['X_test'].shape[0]}")
print(f"✓ Image shape: {data['X_train'].shape[1:]}")

# Create model
print("\n🏗️ Creating CNN model architecture...")
model_classifier = ImageClassificationModel()
model_classifier.create_cnn_model()

print("✓ Model created successfully!")
print(model_classifier.get_model_summary())

# Train model
epochs = 15  # Reduced from 50 for faster training
batch_size = config.DEFAULT_BATCH_SIZE

print(f"\n🏋️ Training model for {epochs} epochs with batch size {batch_size}...")
print("This will take approximately 3-5 minutes...\n")

history = model_classifier.train_model(
    data['X_train'], 
    data['y_train'],
    data['X_test'], 
    data['y_test'],
    epochs=epochs,
    batch_size=batch_size
)

# Save model
model_dir = config.MODEL_DIR
os.makedirs(model_dir, exist_ok=True)

# Save in both formats for compatibility
h5_path = os.path.join(model_dir, 'cifar10_cnn_model.h5')
keras_path = os.path.join(model_dir, 'cifar10_cnn_model.keras')

print(f"\n💾 Saving model...")
model_classifier.save_model(h5_path)
model_classifier.save_model(keras_path)

print(f"✓ Model saved to: {h5_path}")
print(f"✓ Model saved to: {keras_path}")

# Display training results
print("\n" + "=" * 70)
print("📊 Training Results")
print("=" * 70)

final_train_loss = history.history['loss'][-1]
final_train_acc = history.history['accuracy'][-1]
final_val_loss = history.history['val_loss'][-1]
final_val_acc = history.history['val_accuracy'][-1]

print(f"Final Training Loss: {final_train_loss:.4f}")
print(f"Final Training Accuracy: {final_train_acc:.4f} ({final_train_acc*100:.2f}%)")
print(f"Final Validation Loss: {final_val_loss:.4f}")
print(f"Final Validation Accuracy: {final_val_acc:.4f} ({final_val_acc*100:.2f}%)")

print("\n" + "=" * 70)
print("✅ Training complete!")
print("=" * 70)
print("\n📤 Next steps:")
print("1. Check the models/ directory for the trained model files")
print("2. Commit and push to GitHub:")
print("   git add models/")
print("   git commit -m 'Add pre-trained CIFAR-10 model'")
print("   git push origin main")
print("\n3. Update .gitignore to allow model files (removing models/*.h5 exclusion)")
print("\n4. Remove auto-training from app.py startup code")
print("\n" + "=" * 70)
