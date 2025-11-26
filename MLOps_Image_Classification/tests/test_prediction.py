"""
Unit tests for prediction module
"""

import pytest
import numpy as np
from PIL import Image
import os
import sys
import tempfile
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.prediction import ImagePredictor
from src.model import ImageClassificationModel
from src.preprocessing import DataPreprocessor


class TestImagePredictor:
    """Test cases for ImagePredictor class."""
    
    @pytest.fixture
    def predictor(self):
        """Create a predictor instance for testing."""
        # Create a simple model
        model_classifier = ImageClassificationModel()
        model_classifier.create_cnn_model()
        
        # Create preprocessor
        preprocessor = DataPreprocessor()
        
        # Class names
        class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 
                       'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
        
        return ImagePredictor(model_classifier.model, class_names, preprocessor)
    
    def test_initialization(self, predictor):
        """Test predictor initialization."""
        assert predictor.model is not None
        assert len(predictor.class_names) == 10
        assert predictor.preprocessor is not None
        assert len(predictor.prediction_history) == 0
    
    def test_predict_single_image(self, predictor):
        """Test single image prediction."""
        # Create a test image
        image = np.random.rand(32, 32, 3).astype(np.float32)
        
        # Make prediction
        result = predictor.predict_single_image(image, return_probabilities=True)
        
        # Check result structure
        assert 'predicted_class' in result
        assert 'predicted_class_index' in result
        assert 'confidence' in result
        assert 'prediction_time_ms' in result
        assert 'all_probabilities' in result
        
        # Check values
        assert result['predicted_class'] in predictor.class_names
        assert 0 <= result['predicted_class_index'] < 10
        assert 0 <= result['confidence'] <= 1
        assert result['prediction_time_ms'] >= 0
        assert len(result['all_probabilities']) == 10
        
        # Check history is updated
        assert len(predictor.prediction_history) == 1
    
    def test_predict_batch(self, predictor):
        """Test batch prediction."""
        # Create batch of test images
        images = np.random.rand(5, 32, 32, 3).astype(np.float32)
        
        # Make batch prediction
        result = predictor.predict_batch(images)
        
        # Check result structure
        assert 'total_images' in result
        assert 'total_time_ms' in result
        assert 'avg_time_per_image_ms' in result
        assert 'predictions' in result
        
        # Check values
        assert result['total_images'] == 5
        assert len(result['predictions']) == 5
        
        # Check each prediction
        for pred in result['predictions']:
            assert 'predicted_class' in pred
            assert 'confidence' in pred
            assert 'all_probabilities' in pred
    
    def test_get_top_k_predictions(self, predictor):
        """Test getting top k predictions."""
        # Create a test image
        image = np.random.rand(32, 32, 3).astype(np.float32)
        
        # Get top 3 predictions
        top_k = predictor.get_top_k_predictions(image, k=3)
        
        # Check result
        assert len(top_k) == 3
        
        # Check each prediction
        for pred in top_k:
            assert 'class' in pred
            assert 'class_index' in pred
            assert 'probability' in pred
            assert pred['class'] in predictor.class_names
            assert 0 <= pred['probability'] <= 1
        
        # Check they're sorted by probability
        probs = [p['probability'] for p in top_k]
        assert probs == sorted(probs, reverse=True)
    
    def test_evaluate_predictions(self, predictor):
        """Test prediction evaluation."""
        # Create test data
        images = np.random.rand(20, 32, 32, 3).astype(np.float32)
        true_labels = np.random.randint(0, 10, 20)
        
        # Evaluate
        result = predictor.evaluate_predictions(images, true_labels)
        
        # Check result structure
        assert 'accuracy' in result
        assert 'correct_predictions' in result
        assert 'total_predictions' in result
        assert 'per_class_accuracy' in result
        
        # Check values
        assert 0 <= result['accuracy'] <= 1
        assert result['correct_predictions'] <= result['total_predictions']
        assert result['total_predictions'] == 20
        assert len(result['per_class_accuracy']) == 10
    
    def test_get_prediction_statistics(self, predictor):
        """Test getting prediction statistics."""
        # Make some predictions
        for _ in range(5):
            image = np.random.rand(32, 32, 3).astype(np.float32)
            predictor.predict_single_image(image)
        
        # Get statistics
        stats = predictor.get_prediction_statistics()
        
        # Check statistics
        assert 'total_predictions' in stats
        assert 'average_confidence' in stats
        assert 'average_prediction_time_ms' in stats
        assert 'predictions_per_class' in stats
        
        # Check values
        assert stats['total_predictions'] == 5
        assert 0 <= stats['average_confidence'] <= 1
        assert len(stats['predictions_per_class']) == 10
    
    def test_clear_history(self, predictor):
        """Test clearing prediction history."""
        # Make some predictions
        image = np.random.rand(32, 32, 3).astype(np.float32)
        predictor.predict_single_image(image)
        
        # Check history has items
        assert len(predictor.prediction_history) > 0
        
        # Clear history
        predictor.clear_history()
        
        # Check history is empty
        assert len(predictor.prediction_history) == 0
    
    def test_save_and_load_predictions(self, predictor):
        """Test saving and loading predictions."""
        # Make some predictions
        for _ in range(3):
            image = np.random.rand(32, 32, 3).astype(np.float32)
            predictor.predict_single_image(image)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            # Save predictions
            predictor.save_predictions(filepath)
            
            # Check file exists
            assert os.path.exists(filepath)
            
            # Clear history
            predictor.clear_history()
            assert len(predictor.prediction_history) == 0
            
            # Load predictions
            predictor.load_predictions(filepath)
            
            # Check history is restored
            assert len(predictor.prediction_history) == 3
        
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_persistence_integration(self):
        """Test persistence save/load integration."""
        # Create predictor with persistence file
        model_classifier = ImageClassificationModel()
        model_classifier.create_cnn_model()
        preprocessor = DataPreprocessor()
        class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 
                       'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            persistence_file = f.name
        
        try:
            predictor = ImagePredictor(
                model_classifier.model,
                class_names,
                preprocessor,
                persistence_file=persistence_file
            )
            
            # Make predictions
            for _ in range(3):
                image = np.random.rand(32, 32, 3).astype(np.float32)
                predictor.predict_single_image(image)
            
            # Save to persistence
            predictor.save_to_persistence()
            
            # Create new predictor and load from persistence
            new_predictor = ImagePredictor(
                model_classifier.model,
                class_names,
                preprocessor,
                persistence_file=persistence_file
            )
            new_predictor.load_from_persistence()
            
            # Check history is loaded
            assert len(new_predictor.prediction_history) == 3
        
        finally:
            if os.path.exists(persistence_file):
                os.remove(persistence_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
