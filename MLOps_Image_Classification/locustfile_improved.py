"""
Improved Locust Load Testing File for Image Classification API

This file simulates flood of requests to test the model's performance
under various load conditions with CORRECT API endpoints.

Usage:
    # With Web UI
    locust -f locustfile_improved.py --host=http://localhost:5000
    
    # Headless mode
    locust -f locustfile_improved.py --host=http://localhost:5000 --users 100 --spawn-rate 10 --run-time 5m --headless
    
    # With Docker containers
    locust -f locustfile_improved.py --host=http://localhost --users 200 --spawn-rate 20 --run-time 5m --headless
"""

from locust import HttpUser, task, between
import random
import io
from PIL import Image
import numpy as np
import os


class ImageClassificationUser(HttpUser):
    """
    Simulates users making requests to the image classification API.
    
    Tasks:
    1. Single image prediction (highest weight)
    2. Get model uptime
    3. Get statistics
    4. View dashboard
    5. Get visualizations
    """
    
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a simulated user starts"""
        print("User started - generating test image")
        self.test_image_data = self._generate_test_image()
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image for testing"""
        # Create random image data
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    @task(10)
    def predict_image(self):
        """
        Test the prediction endpoint (highest priority task)
        Weight: 10 (this will be called 10x more than weight-1 tasks)
        """
        files = {'file': ('test_image.png', self._generate_test_image(), 'image/png')}
        
        with self.client.post(
            "/api/predict",
            files=files,
            catch_response=True,
            name="/api/predict [POST]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "predicted_class" in result and "confidence" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except Exception as e:
                    response.failure(f"JSON decode error: {str(e)}")
            elif response.status_code == 429:
                response.failure("Rate limit exceeded")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(3)
    def get_uptime(self):
        """
        Test the model uptime endpoint
        Weight: 3
        """
        with self.client.get(
            "/api/model/uptime",
            catch_response=True,
            name="/api/model/uptime [GET]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "uptime_seconds" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def get_statistics(self):
        """
        Test the statistics endpoint
        Weight: 2
        """
        with self.client.get(
            "/api/statistics",
            catch_response=True,
            name="/api/statistics [GET]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def view_dashboard(self):
        """
        Test the dashboard page
        Weight: 1
        """
        with self.client.get(
            "/",
            catch_response=True,
            name="/ [GET] Dashboard"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def get_health(self):
        """
        Test the health check endpoint
        Weight: 1
        """
        with self.client.get(
            "/api/health",
            catch_response=True,
            name="/api/health [GET]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "status" in result and result["status"] == "healthy":
                        response.success()
                    else:
                        response.failure("Service not healthy")
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def get_visualizations(self):
        """
        Test the visualizations endpoint
        Weight: 1
        """
        with self.client.get(
            "/api/visualizations",
            catch_response=True,
            name="/api/visualizations [GET]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")


class BatchPredictionUser(HttpUser):
    """
    Simulates users making batch predictions.
    Use this for testing batch prediction performance.
    """
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """Called when a simulated user starts"""
        print("Batch user started")
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image"""
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    @task
    def batch_predict(self):
        """Test batch prediction with 5 images"""
        files = []
        for i in range(5):
            files.append(
                ('files', (f'test_image_{i}.png', self._generate_test_image(), 'image/png'))
            )
        
        with self.client.post(
            "/api/predict/batch",
            files=files,
            catch_response=True,
            name="/api/predict/batch [POST]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "total_processed" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except Exception:
                    response.failure("Invalid JSON response")
            elif response.status_code == 429:
                response.failure("Rate limit exceeded")
            else:
                response.failure(f"Got status code {response.status_code}")


class HighLoadUser(HttpUser):
    """
    Simulates intensive users that only make prediction requests
    with minimal wait time for stress testing.
    """
    
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    def on_start(self):
        """Called when a simulated user starts"""
        self.test_image_data = self._generate_test_image()
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image"""
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    @task
    def predict_intensive(self):
        """Only predict - intensive mode"""
        files = {'file': ('test.png', self._generate_test_image(), 'image/png')}
        self.client.post("/api/predict", files=files, name="/api/predict [INTENSIVE]")


class BurstLoadUser(HttpUser):
    """
    Simulates burst load patterns with rapid requests followed by idle periods.
    """
    
    wait_time = between(5, 10)  # Longer wait between bursts
    
    def on_start(self):
        """Called when a simulated user starts"""
        print("Burst load user started")
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image"""
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    @task
    def burst_predict(self):
        """Send burst of 10 predictions rapidly"""
        for _ in range(10):
            files = {'file': ('test.png', self._generate_test_image(), 'image/png')}
            self.client.post("/api/predict", files=files, name="/api/predict [BURST]")


"""
=================================================================================
LOAD TESTING SCENARIOS - CORRECTED FOR ACTUAL API ENDPOINTS
=================================================================================

1. NORMAL LOAD (Standard usage pattern):
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 50 --spawn-rate 5 --run-time 5m --headless \\
       --csv=results/normal_load

2. MEDIUM LOAD (Moderate traffic):
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 100 --spawn-rate 10 --run-time 5m --headless \\
       --csv=results/medium_load

3. HIGH LOAD (Heavy traffic):
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 200 --spawn-rate 20 --run-time 5m --headless \\
       --csv=results/high_load

4. STRESS TEST (Use HighLoadUser for maximum load):
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 300 --spawn-rate 30 --run-time 3m --headless \\
       --user-classes HighLoadUser \\
       --csv=results/stress_test

5. BURST TEST (Simulates burst patterns):
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 100 --spawn-rate 50 --run-time 5m --headless \\
       --user-classes BurstLoadUser \\
       --csv=results/burst_test

6. BATCH PREDICTION TEST:
   locust -f locustfile_improved.py --host=http://localhost:5000 \\
       --users 20 --spawn-rate 5 --run-time 5m --headless \\
       --user-classes BatchPredictionUser \\
       --csv=results/batch_test

=================================================================================
DOCKER CONTAINER SCALING TESTS
=================================================================================

Test the same scenario with different numbers of containers to compare performance:

A. Single Container:
   docker-compose up -d ml-api-1
   locust -f locustfile_improved.py --host=http://localhost:5001 \\
       --users 50,100,200 --spawn-rate 10 --run-time 5m --headless \\
       --csv=results/single_container

B. Two Containers with Load Balancer:
   docker-compose up -d ml-api-1 ml-api-2 nginx
   locust -f locustfile_improved.py --host=http://localhost \\
       --users 50,100,200 --spawn-rate 10 --run-time 5m --headless \\
       --csv=results/two_containers

C. Three Containers with Load Balancer:
   docker-compose up -d
   locust -f locustfile_improved.py --host=http://localhost \\
       --users 50,100,200 --spawn-rate 10 --run-time 5m --headless \\
       --csv=results/three_containers

=================================================================================
MONITORING METRICS
=================================================================================

Key metrics to record:
- Response times (min, max, average, median, 95th percentile, 99th percentile)
- Requests per second (RPS)
- Failure rate (%)
- CPU and memory usage per container
- Network throughput
- Model prediction latency

Expected Results:
- Single container: Higher latency, lower throughput, may see failures at 200 users
- Two containers: ~2x improvement in throughput, better latency
- Three containers: ~3x improvement in throughput, best latency

=================================================================================
"""
