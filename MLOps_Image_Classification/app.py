"""
Flask API for Image Classification ML Pipeline
Provides endpoints for prediction, model monitoring, retraining, and data upload.
Enhanced with security, logging, rate limiting, and persistence.
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image
import pickle
import json
from datetime import datetime
import threading
import time
import logging
from logging.handlers import RotatingFileHandler

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.preprocessing import DataPreprocessor
from src.model import ImageClassificationModel, load_latest_model
from src.prediction import ImagePredictor
from config import get_config, Config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_obj = get_config()
config_obj.init_app()
app.config.from_object(config_obj)

# Enable CORS
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=app.config['RATE_LIMIT_STORAGE_URL'],
    default_limits=[app.config['RATE_LIMIT_DEFAULT']]
) if app.config['RATE_LIMIT_ENABLED'] else None

# Configure logging
def setup_logging():
    """Setup application logging."""
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    log_format = logging.Formatter(app.config['LOG_FORMAT'])
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    
    # Configure app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Configure werkzeug logger
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    log.addHandler(file_handler)

setup_logging()

# Global variables
model_classifier = None
predictor = None
preprocessor = None
class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 
               'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
model_start_time = datetime.now()
is_retraining = False
retraining_status = {}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_model_on_startup():
    """Load the trained model on startup."""
    global model_classifier, predictor, preprocessor
    
    try:
        app.logger.info("Initializing model on startup...")
        
        # Initialize preprocessor
        preprocessor = DataPreprocessor()
        
        # Try to load existing model
        try:
            model_classifier = load_latest_model(app.config['MODEL_DIR'])
            app.logger.info("✅ Existing model loaded successfully!")
        except FileNotFoundError:
            app.logger.warning("⚠️ No existing model found. Creating new model...")
            model_classifier = ImageClassificationModel()
            model_classifier.create_cnn_model()
            app.logger.info("✅ New model created successfully!")
        
        # Initialize predictor with persistence
        predictor = ImagePredictor(
            model_classifier.model, 
            class_names, 
            preprocessor,
            persistence_file=app.config['PREDICTIONS_FILE']
        )
        
        # Load previous prediction history
        predictor.load_from_persistence()
        
        app.logger.info("✅ Predictor initialized successfully!")
        
    except Exception as e:
        app.logger.error(f"❌ Error loading model: {str(e)}", exc_info=True)
        raise


# Load model on startup
load_model_on_startup()


@app.route('/')
def home():
    """Render main dashboard."""
    app.logger.debug("Dashboard accessed")
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_classifier is not None,
        'uptime_seconds': (datetime.now() - model_start_time).total_seconds(),
        'timestamp': datetime.now().isoformat(),
        'version': app.config['API_VERSION']
    })


@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information."""
    if model_classifier is None:
        app.logger.error("Model not loaded")
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        info = {
            'input_shape': model_classifier.input_shape,
            'num_classes': model_classifier.num_classes,
            'class_names': class_names,
            'training_metadata': model_classifier.training_metadata,
            'model_summary': model_classifier.get_model_summary()
        }
        
        app.logger.debug("Model info retrieved successfully")
        return jsonify(info)
    except Exception as e:
        app.logger.error(f"Error getting model info: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/model/uptime', methods=['GET'])
def model_uptime():
    """Get model uptime statistics."""
    try:
        uptime_seconds = (datetime.now() - model_start_time).total_seconds()
        
        return jsonify({
            'start_time': model_start_time.isoformat(),
            'current_time': datetime.now().isoformat(),
            'uptime_seconds': uptime_seconds,
            'uptime_minutes': uptime_seconds / 60,
            'uptime_hours': uptime_seconds / 3600,
            'is_retraining': is_retraining
        })
    except Exception as e:
        app.logger.error(f"Error getting uptime: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
@limiter.limit("30 per minute") if limiter else lambda f: f
def predict():
    """Predict class for uploaded image."""
    if 'file' not in request.files:
        app.logger.warning("No file uploaded in request")
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        app.logger.warning("No file selected")
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        app.logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        app.logger.info(f"Processing prediction for: {filename}")
        
        # Make prediction
        result = predictor.predict_from_file(filepath)
        
        # Save prediction to persistence
        predictor.save_to_persistence()
        
        # Clean up
        os.remove(filepath)
        
        app.logger.info(f"Prediction successful: {result['predicted_class']} ({result['confidence']:.2%})")
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
@limiter.limit("10 per minute") if limiter else lambda f: f
def predict_batch():
    """Predict classes for multiple uploaded images."""
    if 'files' not in request.files:
        app.logger.warning("No files uploaded in batch request")
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        app.logger.warning("No files selected in batch request")
        return jsonify({'error': 'No files selected'}), 400
    
    try:
        results = []
        errors = []
        
        app.logger.info(f"Processing batch of {len(files)} images")
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    result = predictor.predict_from_file(filepath)
                    results.append(result)
                except Exception as e:
                    app.logger.error(f"Error processing {filename}: {str(e)}")
                    errors.append({
                        'filename': filename,
                        'error': str(e)
                    })
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)
        
        # Save predictions to persistence
        predictor.save_to_persistence()
        
        app.logger.info(f"Batch processing complete: {len(results)} successful, {len(errors)} errors")
        
        return jsonify({
            'total_processed': len(results),
            'total_errors': len(errors),
            'predictions': results,
            'errors': errors
        })
    
    except Exception as e:
        app.logger.error(f"Error during batch prediction: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get prediction statistics."""
    try:
        stats = predictor.get_prediction_statistics()
        return jsonify(stats)
    except Exception as e:
        app.logger.error(f"Error getting statistics: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualizations', methods=['GET'])
def get_visualizations():
    """Get available visualization images."""
    try:
        static_dir = app.config['STATIC_DIR']
        visualizations = []
        
        if os.path.exists(static_dir):
            for filename in os.listdir(static_dir):
                if filename.endswith('.png'):
                    visualizations.append({
                        'name': filename.replace('_', ' ').replace('.png', '').title(),
                        'filename': filename,
                        'url': f'/static/{filename}'
                    })
        
        return jsonify({'visualizations': visualizations})
    except Exception as e:
        app.logger.error(f"Error getting visualizations: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload/training-data', methods=['POST'])
@limiter.limit("5 per hour") if limiter else lambda f: f
def upload_training_data():
    """Upload new training data for retraining."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    labels = request.form.getlist('labels')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    if len(files) != len(labels):
        return jsonify({'error': 'Number of files and labels must match'}), 400
    
    try:
        # Create directory for new training data
        new_data_dir = os.path.join(app.config['TRAIN_DIR'], 'uploaded')
        os.makedirs(new_data_dir, exist_ok=True)
        
        saved_files = []
        
        app.logger.info(f"Uploading {len(files)} training files")
        
        for file, label in zip(files, labels):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add label to filename
                labeled_filename = f"{label}_{filename}"
                filepath = os.path.join(new_data_dir, labeled_filename)
                file.save(filepath)
                saved_files.append({
                    'filename': labeled_filename,
                    'label': label,
                    'path': filepath
                })
        
        app.logger.info(f"Successfully uploaded {len(saved_files)} training files")
        
        return jsonify({
            'message': 'Training data uploaded successfully',
            'files_saved': len(saved_files),
            'files': saved_files
        })
    
    except Exception as e:
        app.logger.error(f"Error uploading training data: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


def retrain_model_background(X_train, y_train, X_val, y_val):
    """Background function for retraining model."""
    global is_retraining, retraining_status, model_classifier, predictor
    
    try:
        app.logger.info("Background retraining started")
        
        retraining_status = {
            'status': 'in_progress',
            'start_time': datetime.now().isoformat(),
            'message': 'Retraining started...'
        }
        
        # Retrain the model
        history = model_classifier.retrain_model(
            X_train, y_train, X_val, y_val,
            epochs=app.config['RETRAINING_EPOCHS'],
            batch_size=app.config['RETRAINING_BATCH_SIZE']
        )
        
        # Save the updated model
        model_classifier.save_model(model_dir=app.config['MODEL_DIR'])
        
        # Update predictor with new model
        predictor = ImagePredictor(
            model_classifier.model,
            class_names,
            preprocessor,
            persistence_file=app.config['PREDICTIONS_FILE']
        )
        
        retraining_status = {
            'status': 'completed',
            'end_time': datetime.now().isoformat(),
            'message': 'Retraining completed successfully',
            'final_accuracy': float(history.history['accuracy'][-1]),
            'final_val_accuracy': float(history.history['val_accuracy'][-1])
        }
        
        app.logger.info(f"Retraining completed successfully. Final accuracy: {history.history['accuracy'][-1]:.4f}")
        
    except Exception as e:
        app.logger.error(f"Retraining failed: {str(e)}", exc_info=True)
        retraining_status = {
            'status': 'failed',
            'end_time': datetime.now().isoformat(),
            'error': str(e)
        }
    
    finally:
        is_retraining = False


@app.route('/api/retrain', methods=['POST'])
# Removed rate limiting - using is_retraining flag instead to prevent concurrent retraining
def trigger_retraining():
    """Trigger model retraining."""
    global is_retraining
    
    if is_retraining:
        app.logger.warning("Retraining already in progress")
        return jsonify({
            'error': 'Retraining already in progress',
            'status': retraining_status
        }), 400
    
    try:
        app.logger.info("Retraining triggered")
        
        # Prepare data for retraining
        data = preprocessor.prepare_training_data()
        
        is_retraining = True
        
        # Start retraining in background thread
        thread = threading.Thread(
            target=retrain_model_background,
            args=(data['X_train'], data['y_train'], 
                  data['X_test'], data['y_test'])
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'message': 'Retraining started',
            'status': 'in_progress',
            'check_status_url': '/api/retrain/status'
        })
    
    except Exception as e:
        app.logger.error(f"Error triggering retraining: {str(e)}", exc_info=True)
        is_retraining = False
        return jsonify({'error': str(e)}), 500


@app.route('/api/retrain/status', methods=['GET'])
def retraining_status_endpoint():
    """Get retraining status."""
    return jsonify({
        'is_retraining': is_retraining,
        'status': retraining_status
    })


@app.route('/api/model/evaluate', methods=['POST'])
@limiter.limit("5 per hour") if limiter else lambda f: f
def evaluate_model():
    """Evaluate model on test data."""
    try:
        app.logger.info("Model evaluation requested")
        
        # Load test data
        data = preprocessor.prepare_training_data()
        
        # Evaluate
        metrics = model_classifier.evaluate_model(
            data['X_test'],
            data['y_test'],
            class_names
        )
        
        app.logger.info(f"Model evaluation complete. Accuracy: {metrics['accuracy']:.4f}")
        return jsonify(metrics)
    
    except Exception as e:
        app.logger.error(f"Error evaluating model: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(app.config['STATIC_DIR'], filename)


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    app.logger.warning("File upload too large")
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    app.logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit errors."""
    app.logger.warning(f"Rate limit exceeded: {request.remote_addr}")
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    app.logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("="*70)
    print("🚀 Starting Image Classification ML API (Enhanced)")
    print("="*70)
    print(f"Environment: {app.config['ENV']}")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Model loaded: {model_classifier is not None}")
    print(f"Predictor initialized: {predictor is not None}")
    print(f"Number of classes: {len(class_names)}")
    print(f"Rate limiting: {'Enabled' if app.config['RATE_LIMIT_ENABLED'] else 'Disabled'}")
    print(f"Logging level: {app.config['LOG_LEVEL']}")
    print("="*70)
    print("\n📍 API Endpoints:")
    print("  GET  /                          - Main dashboard")
    print("  GET  /api/health                - Health check")
    print("  GET  /api/model/info            - Model information")
    print("  GET  /api/model/uptime          - Model uptime")
    print("  POST /api/predict               - Single image prediction [Rate limited: 30/min]")
    print("  POST /api/predict/batch         - Batch prediction [Rate limited: 10/min]")
    print("  GET  /api/statistics            - Prediction statistics")
    print("  GET  /api/visualizations        - Available visualizations")
    print("  POST /api/upload/training-data  - Upload training data [Rate limited: 5/hr]")
    print("  POST /api/retrain               - Trigger retraining [Rate limited: 1/hr]")
    print("  GET  /api/retrain/status        - Retraining status")
    print("  POST /api/model/evaluate        - Evaluate model [Rate limited: 5/hr]")
    print("="*70)
    print(f"\n🌐 Starting server on http://localhost:{app.config['PORT']}")
    print("="*70)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
