"""
Model Module
Handles model creation, training, evaluation, and retraining.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import os
import json
from datetime import datetime


class ImageClassificationModel:
    """Class for handling model operations."""
    
    def __init__(self, input_shape=(32, 32, 3), num_classes=10):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None
        self.training_metadata = {}
    
    def create_cnn_model(self):
        """
        Create a CNN model for image classification.
        
        Returns:
            Compiled Keras model
        """
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', 
                         input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and Dense Layers
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train_model(self, X_train, y_train, X_val, y_val, 
                   epochs=15, batch_size=64, callbacks=None):
        """
        Train the model.
        
        Args:
            X_train: Training images
            y_train: Training labels
            X_val: Validation images
            y_val: Validation labels
            epochs: Number of epochs
            batch_size: Batch size
            callbacks: List of Keras callbacks
        
        Returns:
            Training history
        """
        if self.model is None:
            self.create_cnn_model()
        
        # Default callbacks
        if callbacks is None:
            callbacks = [
                EarlyStopping(
                    monitor='val_loss',
                    patience=10,
                    restore_best_weights=True,
                    verbose=1
                ),
                ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=5,
                    min_lr=1e-7,
                    verbose=1
                )
            ]
        
        # Train the model
        self.history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        # Store metadata
        self.training_metadata = {
            'timestamp': datetime.now().isoformat(),
            'epochs_trained': len(self.history.history['loss']),
            'final_train_accuracy': float(self.history.history['accuracy'][-1]),
            'final_val_accuracy': float(self.history.history['val_accuracy'][-1]),
            'final_train_loss': float(self.history.history['loss'][-1]),
            'final_val_loss': float(self.history.history['val_loss'][-1]),
            'batch_size': batch_size,
            'total_epochs_requested': epochs
        }
        
        return self.history
    
    def retrain_model(self, X_train, y_train, X_val, y_val, 
                     epochs=20, batch_size=64):
        """
        Retrain the existing model with new data.
        
        Args:
            X_train: Training images
            y_train: Training labels
            X_val: Validation images
            y_val: Validation labels
            epochs: Number of epochs
            batch_size: Batch size
        
        Returns:
            Training history
        """
        if self.model is None:
            raise ValueError("No model to retrain. Create a model first.")
        
        print(f"Retraining model starting at {datetime.now()}")
        
        # Callbacks for retraining
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Continue training
        history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        # Update metadata
        retrain_metadata = {
            'retrain_timestamp': datetime.now().isoformat(),
            'retrain_epochs': len(history.history['loss']),
            'retrain_final_accuracy': float(history.history['accuracy'][-1]),
            'retrain_final_val_accuracy': float(history.history['val_accuracy'][-1])
        }
        
        self.training_metadata['retraining_history'] = self.training_metadata.get('retraining_history', [])
        self.training_metadata['retraining_history'].append(retrain_metadata)
        
        return history
    
    def evaluate_model(self, X_test, y_test, class_names=None):
        """
        Evaluate the model and generate comprehensive metrics.
        
        Args:
            X_test: Test images
            y_test: Test labels (categorical)
            class_names: List of class names
        
        Returns:
            dict of evaluation metrics
        """
        if self.model is None:
            raise ValueError("No model to evaluate. Train a model first.")
        
        # Make predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        # Calculate metrics
        from sklearn.metrics import precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision_macro': float(precision_score(y_true, y_pred, average='macro')),
            'precision_weighted': float(precision_score(y_true, y_pred, average='weighted')),
            'recall_macro': float(recall_score(y_true, y_pred, average='macro')),
            'recall_weighted': float(recall_score(y_true, y_pred, average='weighted')),
            'f1_macro': float(f1_score(y_true, y_pred, average='macro')),
            'f1_weighted': float(f1_score(y_true, y_pred, average='weighted')),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'evaluation_timestamp': datetime.now().isoformat()
        }
        
        # Classification report
        if class_names is not None:
            report = classification_report(y_true, y_pred, 
                                          target_names=class_names, 
                                          output_dict=True)
            metrics['classification_report'] = report
        
        return metrics
    
    def save_model(self, model_dir='../models', model_name='cifar10_cnn_model'):
        """
        Save the model and metadata.
        
        Args:
            model_dir: Directory to save model
            model_name: Base name for model files
        """
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save as HDF5
        h5_path = os.path.join(model_dir, f'{model_name}.h5')
        self.model.save(h5_path)
        print(f"Model saved as HDF5: {h5_path}")
        
        # Save as TensorFlow SavedModel
        tf_path = os.path.join(model_dir, model_name)
        self.model.save(tf_path)
        print(f"Model saved as TensorFlow SavedModel: {tf_path}")
        
        # Save metadata
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        metadata = {
            'input_shape': self.input_shape,
            'num_classes': self.num_classes,
            'training_metadata': self.training_metadata
        }
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        print(f"Metadata saved: {metadata_path}")
        
        # Save training history if available
        if self.history is not None:
            history_path = os.path.join(model_dir, 'training_history.pkl')
            with open(history_path, 'wb') as f:
                pickle.dump(self.history.history, f)
            print(f"Training history saved: {history_path}")
    
    def load_model(self, model_path):
        """
        Load a saved model.
        
        Args:
            model_path: Path to model file (.h5 or SavedModel directory)
        """
        self.model = keras.models.load_model(model_path)
        print(f"Model loaded from: {model_path}")
        
        # Try to load metadata
        model_dir = os.path.dirname(model_path) if os.path.isfile(model_path) else model_path
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                self.training_metadata = metadata.get('training_metadata', {})
            print("Metadata loaded successfully")
    
    def get_model_summary(self):
        """
        Get a summary of the model architecture.
        
        Returns:
            str: Model summary
        """
        if self.model is None:
            return "No model created yet."
        
        from io import StringIO
        stream = StringIO()
        self.model.summary(print_fn=lambda x: stream.write(x + '\n'))
        return stream.getvalue()
    
    def check_retraining_needed(self, current_accuracy, threshold=0.75):
        """
        Check if model retraining is needed based on accuracy threshold.
        
        Args:
            current_accuracy: Current model accuracy
            threshold: Minimum acceptable accuracy
        
        Returns:
            bool: True if retraining is needed
        """
        return current_accuracy < threshold


def load_latest_model(model_dir='../models'):
    """
    Load the latest trained model.
    
    Args:
        model_dir: Directory containing model files
    
    Returns:
        ImageClassificationModel instance
    """
    model_classifier = ImageClassificationModel()
    
    # Try to load HDF5 model first
    h5_path = os.path.join(model_dir, 'cifar10_cnn_model.h5')
    if os.path.exists(h5_path):
        model_classifier.load_model(h5_path)
        return model_classifier
    
    # Try SavedModel format
    tf_path = os.path.join(model_dir, 'cifar10_cnn_model')
    if os.path.exists(tf_path):
        model_classifier.load_model(tf_path)
        return model_classifier
    
    raise FileNotFoundError(f"No model found in {model_dir}")


if __name__ == "__main__":
    # Test model creation
    model_classifier = ImageClassificationModel()
    model = model_classifier.create_cnn_model()
    
    print("Model created successfully!")
    print("\nModel Summary:")
    print(model_classifier.get_model_summary())
    
    # Count parameters
    trainable_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    print(f"\nTotal trainable parameters: {trainable_params:,}")
