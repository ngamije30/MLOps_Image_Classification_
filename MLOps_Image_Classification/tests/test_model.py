"""
Unit tests for model module
"""

import pytest
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import sys
import tempfile

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model import ImageClassificationModel, load_latest_model


class TestImageClassificationModel:
    """Test cases for ImageClassificationModel class."""
    
    @pytest.fixture
    def model_classifier(self):
        """Create a model classifier instance for testing."""
        return ImageClassificationModel(input_shape=(32, 32, 3), num_classes=10)
    
    def test_initialization(self, model_classifier):
        """Test that model initializes correctly."""
        assert model_classifier.input_shape == (32, 32, 3)
        assert model_classifier.num_classes == 10
        assert model_classifier.model is None
        assert model_classifier.history is None
    
    def test_create_cnn_model(self, model_classifier):
        """Test CNN model creation."""
        model = model_classifier.create_cnn_model()
        
        # Check model is created
        assert model is not None
        assert isinstance(model, keras.Model)
        
        # Check input/output shapes
        assert model.input_shape == (None, 32, 32, 3)
        assert model.output_shape == (None, 10)
        
        # Check model is compiled
        assert model.optimizer is not None
        assert model.loss is not None
    
    def test_model_summary(self, model_classifier):
        """Test getting model summary."""
        model_classifier.create_cnn_model()
        summary = model_classifier.get_model_summary()
        
        # Check that summary is a string and not empty
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'conv2d' in summary.lower()
    
    def test_train_model_small(self, model_classifier):
        """Test model training with small dataset."""
        # Create small synthetic dataset
        X_train = np.random.rand(50, 32, 32, 3).astype(np.float32)
        y_train = keras.utils.to_categorical(np.random.randint(0, 10, 50), 10)
        X_val = np.random.rand(10, 32, 32, 3).astype(np.float32)
        y_val = keras.utils.to_categorical(np.random.randint(0, 10, 10), 10)
        
        # Train for just 2 epochs
        history = model_classifier.train_model(
            X_train, y_train, X_val, y_val,
            epochs=2, batch_size=16
        )
        
        # Check history exists
        assert history is not None
        assert 'loss' in history.history
        assert 'accuracy' in history.history
        assert 'val_loss' in history.history
        assert 'val_accuracy' in history.history
        
        # Check metadata is stored
        assert 'timestamp' in model_classifier.training_metadata
        assert 'epochs_trained' in model_classifier.training_metadata
    
    def test_evaluate_model(self, model_classifier):
        """Test model evaluation."""
        # Create and train a simple model
        model_classifier.create_cnn_model()
        
        # Create small synthetic dataset
        X_test = np.random.rand(20, 32, 32, 3).astype(np.float32)
        y_test = keras.utils.to_categorical(np.random.randint(0, 10, 20), 10)
        class_names = [f'Class_{i}' for i in range(10)]
        
        # Evaluate
        metrics = model_classifier.evaluate_model(X_test, y_test, class_names)
        
        # Check all required metrics
        assert 'accuracy' in metrics
        assert 'precision_macro' in metrics
        assert 'recall_macro' in metrics
        assert 'f1_macro' in metrics
        assert 'confusion_matrix' in metrics
        assert 'classification_report' in metrics
        
        # Check values are in valid range
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['precision_macro'] <= 1
    
    def test_save_and_load_model(self, model_classifier):
        """Test saving and loading model."""
        # Create model
        model_classifier.create_cnn_model()
        
        # Use temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save model
            model_classifier.save_model(model_dir=tmpdir, model_name='test_model')
            
            # Check files exist
            assert os.path.exists(os.path.join(tmpdir, 'test_model.h5'))
            assert os.path.exists(os.path.join(tmpdir, 'model_metadata.pkl'))
            
            # Create new classifier and load
            new_classifier = ImageClassificationModel()
            new_classifier.load_model(os.path.join(tmpdir, 'test_model.h5'))
            
            # Check model is loaded
            assert new_classifier.model is not None
            assert new_classifier.model.input_shape == (None, 32, 32, 3)
    
    def test_retrain_model(self, model_classifier):
        """Test model retraining."""
        # Create and train initial model
        X_train = np.random.rand(50, 32, 32, 3).astype(np.float32)
        y_train = keras.utils.to_categorical(np.random.randint(0, 10, 50), 10)
        X_val = np.random.rand(10, 32, 32, 3).astype(np.float32)
        y_val = keras.utils.to_categorical(np.random.randint(0, 10, 10), 10)
        
        # Initial training
        model_classifier.train_model(X_train, y_train, X_val, y_val, epochs=1, batch_size=16)
        
        # Retrain
        history = model_classifier.retrain_model(X_train, y_train, X_val, y_val, epochs=1, batch_size=16)
        
        # Check history exists
        assert history is not None
        assert 'retraining_history' in model_classifier.training_metadata
    
    def test_check_retraining_needed(self, model_classifier):
        """Test retraining trigger logic."""
        # Low accuracy should trigger retraining
        assert model_classifier.check_retraining_needed(0.70, threshold=0.75) is True
        
        # High accuracy should not trigger retraining
        assert model_classifier.check_retraining_needed(0.85, threshold=0.75) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
