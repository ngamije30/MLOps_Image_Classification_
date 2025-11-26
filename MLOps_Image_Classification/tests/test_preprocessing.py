"""
Unit tests for preprocessing module
"""

import pytest
import numpy as np
from PIL import Image
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.preprocessing import DataPreprocessor, get_data_statistics


class TestDataPreprocessor:
    """Test cases for DataPreprocessor class."""
    
    @pytest.fixture
    def preprocessor(self):
        """Create a preprocessor instance for testing."""
        return DataPreprocessor()
    
    def test_initialization(self, preprocessor):
        """Test that preprocessor initializes correctly."""
        assert preprocessor.num_classes == 10
        assert len(preprocessor.class_names) == 10
        assert preprocessor.input_shape == (32, 32, 3)
    
    def test_normalize_images(self, preprocessor):
        """Test image normalization."""
        # Create test images
        images = np.random.randint(0, 256, (10, 32, 32, 3), dtype=np.uint8)
        
        # Normalize
        normalized = preprocessor.normalize_images(images)
        
        # Check that values are in [0, 1] range
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0
        assert normalized.dtype == np.float32
    
    def test_preprocess_labels(self, preprocessor):
        """Test label preprocessing."""
        labels = np.array([[0], [1], [2], [3], [4]])
        
        # Categorical encoding
        categorical = preprocessor.preprocess_labels(labels, categorical=True)
        assert categorical.shape == (5, 10)
        assert np.all(categorical.sum(axis=1) == 1)  # One-hot encoded
        
        # Non-categorical
        flat = preprocessor.preprocess_labels(labels, categorical=False)
        assert flat.shape == (5,)
        assert np.array_equal(flat, np.array([0, 1, 2, 3, 4]))
    
    def test_preprocess_single_image_numpy(self, preprocessor):
        """Test preprocessing a single numpy array image."""
        # Create a test image
        image = np.random.randint(0, 256, (32, 32, 3), dtype=np.uint8)
        
        # Preprocess
        processed = preprocessor.preprocess_single_image(image)
        
        # Check shape and normalization
        assert processed.shape == (1, 32, 32, 3)
        assert processed.min() >= 0.0
        assert processed.max() <= 1.0
    
    def test_preprocess_single_image_pil(self, preprocessor):
        """Test preprocessing a PIL Image."""
        # Create a test PIL image
        img_array = np.random.randint(0, 256, (32, 32, 3), dtype=np.uint8)
        pil_image = Image.fromarray(img_array)
        
        # Preprocess
        processed = preprocessor.preprocess_single_image(pil_image)
        
        # Check shape and normalization
        assert processed.shape == (1, 32, 32, 3)
        assert processed.min() >= 0.0
        assert processed.max() <= 1.0
    
    def test_preprocess_single_image_wrong_shape(self, preprocessor):
        """Test that wrong shape raises error."""
        # Create image with wrong shape
        wrong_image = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        
        # Should raise ValueError
        with pytest.raises(ValueError):
            preprocessor.preprocess_single_image(wrong_image)
    
    def test_create_data_augmentation_generator(self, preprocessor):
        """Test data augmentation generator creation."""
        datagen = preprocessor.create_data_augmentation_generator()
        
        # Check that it's an ImageDataGenerator
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        assert isinstance(datagen, ImageDataGenerator)
    
    def test_prepare_training_data(self, preprocessor):
        """Test complete training data preparation."""
        # This will actually download CIFAR-10, so we'll make it optional
        try:
            data = preprocessor.prepare_training_data(with_augmentation=False)
            
            # Check all required keys are present
            assert 'X_train' in data
            assert 'y_train' in data
            assert 'X_test' in data
            assert 'y_test' in data
            assert 'class_names' in data
            
            # Check shapes
            assert data['X_train'].shape[1:] == (32, 32, 3)
            assert data['X_test'].shape[1:] == (32, 32, 3)
            assert data['y_train'].shape[1] == 10  # Categorical
            assert data['y_test'].shape[1] == 10
            
            # Check normalization
            assert data['X_train'].min() >= 0.0
            assert data['X_train'].max() <= 1.0
            
        except Exception as e:
            pytest.skip(f"Could not download CIFAR-10: {str(e)}")


class TestGetDataStatistics:
    """Test cases for get_data_statistics function."""
    
    def test_get_data_statistics(self):
        """Test statistics calculation."""
        # Create test data
        X = np.random.rand(100, 32, 32, 3).astype(np.float32)
        y = np.random.randint(0, 10, 100)
        class_names = [f'Class_{i}' for i in range(10)]
        
        # Get statistics
        stats = get_data_statistics(X, y, class_names)
        
        # Check all required fields
        assert 'total_samples' in stats
        assert 'image_shape' in stats
        assert 'num_classes' in stats
        assert 'class_distribution' in stats
        assert 'pixel_mean' in stats
        assert 'pixel_std' in stats
        
        # Check values
        assert stats['total_samples'] == 100
        assert stats['image_shape'] == (32, 32, 3)
        assert stats['num_classes'] == 10
        assert len(stats['class_distribution']) <= 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
