"""
Prediction Module
Handles predictions for single images and batch predictions.
"""

import numpy as np
import tensorflow as tf
from PIL import Image
import os
import json
from datetime import datetime


class ImagePredictor:
    """Class for handling predictions."""
    
    def __init__(self, model, class_names, preprocessor=None, persistence_file=None):
        """
        Initialize predictor.
        
        Args:
            model: Trained Keras model
            class_names: List of class names
            preprocessor: DataPreprocessor instance (optional)
            persistence_file: Path to file for saving/loading predictions (optional)
        """
        self.model = model
        self.class_names = class_names
        self.preprocessor = preprocessor
        self.prediction_history = []
        self.persistence_file = persistence_file
    
    def predict_single_image(self, image, return_probabilities=True):
        """
        Predict class for a single image.
        
        Args:
            image: Input image (32x32x3) - numpy array or preprocessed
            return_probabilities: Whether to return all class probabilities
        
        Returns:
            dict containing prediction results
        """
        # Ensure image has batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Ensure image is normalized (values between 0 and 1)
        if image.max() > 1.0:
            image = image.astype('float32') / 255.0
        
        # Make prediction
        start_time = datetime.now()
        predictions = self.model.predict(image, verbose=0)
        end_time = datetime.now()
        
        # Get predicted class
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        # Prepare result
        result = {
            'predicted_class': predicted_class,
            'predicted_class_index': int(predicted_class_idx),
            'confidence': confidence,
            'prediction_time_ms': (end_time - start_time).total_seconds() * 1000,
            'timestamp': end_time.isoformat()
        }
        
        if return_probabilities:
            result['all_probabilities'] = {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            }
        
        # Store in history
        self.prediction_history.append(result)
        
        return result
    
    def predict_batch(self, images):
        """
        Predict classes for multiple images.
        
        Args:
            images: Batch of images (N, 32, 32, 3)
        
        Returns:
            list of prediction results
        """
        start_time = datetime.now()
        predictions = self.model.predict(images, verbose=0)
        end_time = datetime.now()
        
        total_time = (end_time - start_time).total_seconds() * 1000
        avg_time_per_image = total_time / len(images)
        
        results = []
        for i, pred in enumerate(predictions):
            predicted_class_idx = np.argmax(pred)
            confidence = float(pred[predicted_class_idx])
            predicted_class = self.class_names[predicted_class_idx]
            
            result = {
                'image_index': i,
                'predicted_class': predicted_class,
                'predicted_class_index': int(predicted_class_idx),
                'confidence': confidence,
                'all_probabilities': {
                    self.class_names[j]: float(pred[j])
                    for j in range(len(self.class_names))
                }
            }
            results.append(result)
        
        batch_info = {
            'total_images': len(images),
            'total_time_ms': total_time,
            'avg_time_per_image_ms': avg_time_per_image,
            'timestamp': end_time.isoformat(),
            'predictions': results
        }
        
        return batch_info
    
    def predict_from_file(self, file_path):
        """
        Predict class for an image file.
        
        Args:
            file_path: Path to image file
        
        Returns:
            dict containing prediction results
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor is required for file predictions")
        
        # Load and preprocess image
        image = self.preprocessor.load_and_preprocess_uploaded_image(file_path)
        
        # Make prediction
        result = self.predict_single_image(image)
        result['file_path'] = file_path
        result['file_name'] = os.path.basename(file_path)
        
        return result
    
    def predict_from_folder(self, folder_path, extensions=('.png', '.jpg', '.jpeg')):
        """
        Predict classes for all images in a folder.
        
        Args:
            folder_path: Path to folder containing images
            extensions: Tuple of allowed file extensions
        
        Returns:
            dict with predictions for all images
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor is required for folder predictions")
        
        results = []
        errors = []
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(extensions):
                file_path = os.path.join(folder_path, filename)
                try:
                    result = self.predict_from_file(file_path)
                    results.append(result)
                except Exception as e:
                    errors.append({
                        'file_name': filename,
                        'error': str(e)
                    })
        
        return {
            'total_processed': len(results),
            'total_errors': len(errors),
            'predictions': results,
            'errors': errors
        }
    
    def get_top_k_predictions(self, image, k=3):
        """
        Get top k predictions for an image.
        
        Args:
            image: Input image
            k: Number of top predictions to return
        
        Returns:
            list of top k predictions with probabilities
        """
        # Ensure image has batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Make prediction
        predictions = self.model.predict(image, verbose=0)[0]
        
        # Get top k indices
        top_k_indices = np.argsort(predictions)[-k:][::-1]
        
        top_k_results = []
        for idx in top_k_indices:
            top_k_results.append({
                'class': self.class_names[idx],
                'class_index': int(idx),
                'probability': float(predictions[idx])
            })
        
        return top_k_results
    
    def evaluate_predictions(self, images, true_labels):
        """
        Evaluate predictions against true labels.
        
        Args:
            images: Batch of images
            true_labels: True class indices
        
        Returns:
            dict with evaluation metrics
        """
        predictions = self.model.predict(images, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        # Calculate accuracy
        correct = np.sum(predicted_classes == true_labels)
        total = len(true_labels)
        accuracy = correct / total
        
        # Per-class accuracy
        per_class_accuracy = {}
        for i, class_name in enumerate(self.class_names):
            class_mask = true_labels == i
            if np.sum(class_mask) > 0:
                class_correct = np.sum(
                    (predicted_classes == i) & class_mask
                )
                class_total = np.sum(class_mask)
                per_class_accuracy[class_name] = class_correct / class_total
            else:
                per_class_accuracy[class_name] = 0.0
        
        return {
            'accuracy': float(accuracy),
            'correct_predictions': int(correct),
            'total_predictions': int(total),
            'per_class_accuracy': per_class_accuracy
        }
    
    def get_prediction_statistics(self):
        """
        Get statistics from prediction history.
        
        Returns:
            dict with statistics
        """
        if not self.prediction_history:
            return {'message': 'No predictions made yet'}
        
        confidences = [p['confidence'] for p in self.prediction_history]
        pred_times = [p['prediction_time_ms'] for p in self.prediction_history]
        
        # Count predictions per class
        class_counts = {name: 0 for name in self.class_names}
        for pred in self.prediction_history:
            class_counts[pred['predicted_class']] += 1
        
        return {
            'total_predictions': len(self.prediction_history),
            'average_confidence': float(np.mean(confidences)),
            'min_confidence': float(np.min(confidences)),
            'max_confidence': float(np.max(confidences)),
            'average_prediction_time_ms': float(np.mean(pred_times)),
            'predictions_per_class': class_counts
        }
    
    def clear_history(self):
        """Clear prediction history."""
        self.prediction_history = []
    
    def save_predictions(self, filepath):
        """
        Save prediction history to file.
        
        Args:
            filepath: Path to save predictions
        """
        with open(filepath, 'w') as f:
            json.dump(self.prediction_history, f, indent=2)
        print(f"Predictions saved to: {filepath}")
    
    def load_predictions(self, filepath):
        """
        Load prediction history from file.
        
        Args:
            filepath: Path to load predictions from
        """
        with open(filepath, 'r') as f:
            self.prediction_history = json.load(f)
        print(f"Predictions loaded from: {filepath}")
    
    def save_to_persistence(self):
        """Save predictions to persistence file if configured."""
        if self.persistence_file and self.prediction_history:
            try:
                os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
                
                # Convert any non-serializable objects to strings
                serializable_history = []
                for pred in self.prediction_history:
                    try:
                        # Create a copy and ensure all values are JSON serializable
                        safe_pred = {}
                        for key, value in pred.items():
                            if isinstance(value, (int, float, str, bool, type(None))):
                                safe_pred[key] = value
                            elif isinstance(value, dict):
                                safe_pred[key] = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                                                 for k, v in value.items()}
                            else:
                                safe_pred[key] = str(value)
                        serializable_history.append(safe_pred)
                    except Exception as e:
                        print(f"Warning: Skipping non-serializable prediction: {str(e)}")
                        continue
                
                with open(self.persistence_file, 'w') as f:
                    json.dump(serializable_history, f, indent=2)
                    
            except Exception as e:
                print(f"Warning: Could not save predictions to persistence: {str(e)}")
    
    def load_from_persistence(self):
        """Load predictions from persistence file if it exists."""
        if self.persistence_file and os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, 'r') as f:
                    content = f.read()
                    if content.strip():  # Check if file is not empty
                        self.prediction_history = json.loads(content)
                        print(f"Loaded {len(self.prediction_history)} predictions from persistence")
                    else:
                        print("Persistence file is empty, starting fresh")
                        self.prediction_history = []
            except json.JSONDecodeError as e:
                print(f"Warning: Corrupted persistence file, starting fresh: {str(e)}")
                self.prediction_history = []
                # Backup corrupted file
                backup_path = f"{self.persistence_file}.backup"
                try:
                    os.rename(self.persistence_file, backup_path)
                    print(f"Backed up corrupted file to: {backup_path}")
                except:
                    pass
            except Exception as e:
                print(f"Warning: Could not load predictions from persistence: {str(e)}")
                self.prediction_history = []


def visualize_prediction(image, prediction_result, save_path=None):
    """
    Visualize a prediction result.
    
    Args:
        image: Original image (32x32x3)
        prediction_result: Prediction result dict
        save_path: Optional path to save visualization
    """
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Show image
    ax1.imshow(image)
    ax1.set_title(f"Predicted: {prediction_result['predicted_class']}\n"
                  f"Confidence: {prediction_result['confidence']:.2%}",
                  fontsize=12, fontweight='bold')
    ax1.axis('off')
    
    # Show probability distribution
    if 'all_probabilities' in prediction_result:
        classes = list(prediction_result['all_probabilities'].keys())
        probs = list(prediction_result['all_probabilities'].values())
        
        colors = ['green' if c == prediction_result['predicted_class'] 
                 else 'skyblue' for c in classes]
        
        ax2.barh(classes, probs, color=colors, edgecolor='black')
        ax2.set_xlabel('Probability', fontsize=11)
        ax2.set_title('Class Probabilities', fontsize=12, fontweight='bold')
        ax2.set_xlim([0, 1])
        ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


if __name__ == "__main__":
    print("Prediction module loaded successfully!")
    print("This module requires a trained model to be loaded.")
