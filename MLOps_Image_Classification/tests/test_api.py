"""
Integration tests for the Flask API
"""

import pytest
import sys
import os
import io
from PIL import Image
import numpy as np

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import after path is set
from app import app as flask_app


@pytest.fixture
def app():
    """Create Flask app for testing."""
    flask_app.config['TESTING'] = True
    flask_app.config['RATE_LIMIT_ENABLED'] = False  # Disable rate limiting for tests
    return flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def create_test_image():
    """Create a test image file."""
    img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


class TestHealthEndpoints:
    """Test health check and info endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'model_loaded' in data
        assert 'uptime_seconds' in data
    
    def test_model_uptime(self, client):
        """Test model uptime endpoint."""
        response = client.get('/api/model/uptime')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'uptime_seconds' in data
        assert 'uptime_minutes' in data
        assert 'uptime_hours' in data
        assert 'is_retraining' in data


class TestPredictionEndpoints:
    """Test prediction endpoints."""
    
    def test_predict_no_file(self, client):
        """Test prediction without file."""
        response = client.post('/api/predict')
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
    
    def test_predict_with_file(self, client):
        """Test prediction with file."""
        img_bytes = create_test_image()
        
        response = client.post(
            '/api/predict',
            data={'file': (img_bytes, 'test.png')},
            content_type='multipart/form-data'
        )
        
        # Should return 200 or 500 depending on model state
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'predicted_class' in data
            assert 'confidence' in data
            assert 'prediction_time_ms' in data
    
    def test_batch_predict_no_files(self, client):
        """Test batch prediction without files."""
        response = client.post('/api/predict/batch')
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
    
    def test_statistics(self, client):
        """Test statistics endpoint."""
        response = client.get('/api/statistics')
        assert response.status_code in [200, 500]


class TestVisualizationEndpoints:
    """Test visualization endpoints."""
    
    def test_get_visualizations(self, client):
        """Test getting visualizations."""
        response = client.get('/api/visualizations')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'visualizations' in data
        assert isinstance(data['visualizations'], list)


class TestRetrainingEndpoints:
    """Test retraining endpoints."""
    
    def test_retrain_status(self, client):
        """Test retraining status endpoint."""
        response = client.get('/api/retrain/status')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'is_retraining' in data
        assert 'status' in data


class TestDashboard:
    """Test dashboard endpoint."""
    
    def test_dashboard_loads(self, client):
        """Test that dashboard loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Image Classification' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
