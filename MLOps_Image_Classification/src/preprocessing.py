"""
Data Preprocessing Module
Handles data loading, preprocessing, and augmentation for image classification.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
import pickle
import os
from PIL import Image


class DataPreprocessor:
    """Class for handling data preprocessing operations."""
    
    def __init__(self):
        self.class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 
                           'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
        self.input_shape = (32, 32, 3)
        self.num_classes = 10
    
    def load_cifar10_data(self):
        """
        Load CIFAR-10 dataset from Keras datasets.
        
        Returns:
            tuple: (X_train, y_train), (X_test, y_test)
        """
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        return (X_train, y_train), (X_test, y_test)
    
    def normalize_images(self, images):
        """
        Normalize image pixel values to [0, 1] range.
        
        Args:
            images: numpy array of images
        
        Returns:
            numpy array of normalized images
        """
        return images.astype('float32') / 255.0
    
    def preprocess_labels(self, labels, categorical=True):
        """
        Preprocess labels (convert to categorical if needed).
        
        Args:
            labels: numpy array of labels
            categorical: whether to convert to categorical (one-hot encoding)
        
        Returns:
            processed labels
        """
        if categorical:
            return to_categorical(labels, self.num_classes)
        return labels.flatten()
    
    def preprocess_single_image(self, image):
        """
        Preprocess a single image for prediction.
        
        Args:
            image: numpy array or PIL Image (32x32x3)
        
        Returns:
            preprocessed image ready for model input
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Ensure correct shape
        if image.shape != self.input_shape:
            raise ValueError(f"Image must have shape {self.input_shape}, got {image.shape}")
        
        # Normalize
        image_normalized = self.normalize_images(image)
        
        # Add batch dimension
        image_batch = np.expand_dims(image_normalized, axis=0)
        
        return image_batch
    
    def create_data_augmentation_generator(self):
        """
        Create an ImageDataGenerator for data augmentation.
        
        Returns:
            ImageDataGenerator object
        """
        datagen = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1,
            fill_mode='nearest'
        )
        return datagen
    
    def load_and_preprocess_uploaded_image(self, file_path):
        """
        Load and preprocess an uploaded image file.
        
        Args:
            file_path: path to image file
        
        Returns:
            preprocessed image
        """
        # Load image
        img = Image.open(file_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 32x32
        img = img.resize((32, 32), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Preprocess
        return self.preprocess_single_image(img_array)
    
    def save_preprocessed_data(self, data, filepath):
        """
        Save preprocessed data to disk.
        
        Args:
            data: data to save
            filepath: path to save file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load_preprocessed_data(self, filepath):
        """
        Load preprocessed data from disk.
        
        Args:
            filepath: path to load file
        
        Returns:
            loaded data
        """
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    
    def prepare_training_data(self, with_augmentation=False):
        """
        Prepare complete training dataset.
        
        Args:
            with_augmentation: whether to include data augmentation
        
        Returns:
            dict containing prepared data
        """
        # Load data
        (X_train, y_train), (X_test, y_test) = self.load_cifar10_data()
        
        # Normalize
        X_train_normalized = self.normalize_images(X_train)
        X_test_normalized = self.normalize_images(X_test)
        
        # Convert labels
        y_train_categorical = self.preprocess_labels(y_train, categorical=True)
        y_test_categorical = self.preprocess_labels(y_test, categorical=True)
        
        data = {
            'X_train': X_train_normalized,
            'y_train': y_train_categorical,
            'X_test': X_test_normalized,
            'y_test': y_test_categorical,
            'class_names': self.class_names,
            'input_shape': self.input_shape,
            'num_classes': self.num_classes
        }
        
        if with_augmentation:
            data['data_generator'] = self.create_data_augmentation_generator()
        
        return data
    
    def batch_preprocess_images(self, image_folder):
        """
        Preprocess all images in a folder.
        
        Args:
            image_folder: path to folder containing images
        
        Returns:
            list of preprocessed images, list of filenames
        """
        images = []
        filenames = []
        
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(image_folder, filename)
                try:
                    img = self.load_and_preprocess_uploaded_image(filepath)
                    images.append(img[0])  # Remove batch dimension
                    filenames.append(filename)
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
        
        if images:
            return np.array(images), filenames
        return None, None


def get_data_statistics(X, y, class_names):
    """
    Get statistics about the dataset.
    
    Args:
        X: images
        y: labels
        class_names: list of class names
    
    Returns:
        dict of statistics
    """
    stats = {
        'total_samples': len(X),
        'image_shape': X.shape[1:],
        'num_classes': len(class_names),
        'class_names': class_names,
        'pixel_mean': float(X.mean()),
        'pixel_std': float(X.std()),
        'pixel_min': float(X.min()),
        'pixel_max': float(X.max())
    }
    
    # Class distribution
    unique, counts = np.unique(y, return_counts=True)
    stats['class_distribution'] = {class_names[i]: int(count) 
                                   for i, count in zip(unique, counts)}
    
    return stats


if __name__ == "__main__":
    # Test preprocessing
    preprocessor = DataPreprocessor()
    data = preprocessor.prepare_training_data()
    
    print("Data preprocessing test:")
    print(f"Training data shape: {data['X_train'].shape}")
    print(f"Test data shape: {data['X_test'].shape}")
    print(f"Number of classes: {data['num_classes']}")
    print(f"Class names: {data['class_names']}")
    
    # Get statistics
    stats = get_data_statistics(
        data['X_train'], 
        np.argmax(data['y_train'], axis=1),
        data['class_names']
    )
    print("\nDataset Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
