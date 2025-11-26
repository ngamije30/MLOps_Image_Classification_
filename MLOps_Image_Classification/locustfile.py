"""
Locust Load Testing File for Image Classification API

This file simulates flood of requests to test the model's performance
under various load conditions.

Usage:
    locust -f locustfile.py --host=http://localhost:5000
    
    Then open browser at http://localhost:8089 to configure:
    - Number of users
    - Spawn rate
    - Run time
"""

from locust import HttpUser, task, between
import random
import json
import base64
import io
from PIL import Image
import numpy as np


class ImageClassificationUser(HttpUser):
    """
    Simulates users making requests to the image classification API.
    
    Tasks:
    1. Predict single image
    2. Get model status
    3. View dashboard
    """
    
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a simulated user starts"""
        print("User started")
        # Generate a dummy image for testing
        self.test_image = self._generate_test_image()
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image for testing"""
        # Create random image data
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return img_base64
    
    @task(5)
    def predict_image(self):
        """
        Test the prediction endpoint (highest priority task)
        Weight: 5 (this will be called 5x more than other tasks)
        """
        # Prepare payload
        payload = {
            "image": self.test_image
        }
        
        # Make POST request
        with self.client.post(
            "/predict",
            json=payload,
            catch_response=True,
            name="/predict [POST]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "predicted_class" in result and "confidence" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def get_status(self):
        """
        Test the model status endpoint
        Weight: 2
        """
        with self.client.get(
            "/api/status",
            catch_response=True,
            name="/api/status [GET]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "status" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
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
    def get_metrics(self):
        """
        Test the metrics endpoint
        Weight: 1
        """
        with self.client.get(
            "/api/metrics",
            catch_response=True,
            name="/api/metrics [GET]"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "accuracy" in result:
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Got status code {response.status_code}")


class IntensiveUser(HttpUser):
    """
    Simulates intensive users that only make prediction requests
    with minimal wait time.
    
    Use this class for stress testing.
    """
    
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    def on_start(self):
        """Called when a simulated user starts"""
        self.test_image = self._generate_test_image()
    
    def _generate_test_image(self):
        """Generate a random 32x32 RGB image for testing"""
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return img_base64
    
    @task
    def predict_only(self):
        """Only predict - intensive mode"""
        payload = {"image": self.test_image}
        self.client.post("/predict", json=payload, name="/predict [INTENSIVE]")


# Custom shape classes for different load patterns

class RampUpUser(HttpUser):
    """
    Gradually increases request rate
    Good for testing how the system handles increasing load
    """
    wait_time = between(0.5, 2)
    
    def on_start(self):
        self.test_image = self._generate_test_image()
    
    def _generate_test_image(self):
        img_array = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    @task
    def predict(self):
        payload = {"image": self.test_image}
        self.client.post("/predict", json=payload)


"""
LOAD TESTING SCENARIOS:

1. NORMAL LOAD:
   locust -f locustfile.py --host=http://localhost:5000 --users 10 --spawn-rate 2 --run-time 5m
   
2. MEDIUM LOAD:
   locust -f locustfile.py --host=http://localhost:5000 --users 50 --spawn-rate 5 --run-time 5m
   
3. HEAVY LOAD:
   locust -f locustfile.py --host=http://localhost:5000 --users 100 --spawn-rate 10 --run-time 5m

4. STRESS TEST (Use IntensiveUser):
   locust -f locustfile.py --host=http://localhost:5000 --users 200 --spawn-rate 20 --run-time 3m

5. HEADLESS MODE (No Web UI):
   locust -f locustfile.py --host=http://localhost:5000 --users 50 --spawn-rate 10 --run-time 2m --headless --csv=results

MONITORING:
- Response times (min, max, average, median)
- Requests per second (RPS)
- Failure rate
- Different percentiles (50th, 66th, 75th, 80th, 90th, 95th, 98th, 99th, 100th)

DOCKER CONTAINER TESTING:
1. Run with 1 container: docker-compose up --scale app=1
2. Test with Locust and record results
3. Run with 2 containers: docker-compose up --scale app=2
4. Test again and compare
5. Run with 4 containers: docker-compose up --scale app=4
6. Test and record final results

Compare latency, throughput, and failure rates across different configurations.
"""
