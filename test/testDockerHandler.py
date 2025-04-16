import unittest
import docker
import sys
import os
from io import StringIO
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import DockerHandler  # Assuming DockerHandler is in main.py


class TestDockerHandler(unittest.TestCase):

    def setUp(self):
        """Setup for the tests."""
        self.dockerfile_content = """
        # Use an official Python runtime as a parent image
        FROM python:3.12-slim

        # Set the working directory in the container
        WORKDIR /app

        # Copy the current directory contents into the container at /app
        COPY . /app

        RUN python app.py

        # Run the application when the container starts
        CMD ["python", "app.py"]
        """
        self.valid_app_code = "print('Test Passed')"  # Valid Python code
        self.invalid_app_code = "print('Test"  # Invalid Python code (missing closing parenthesis)
        self.image_tag = "python-docker-test"
        self.docker_handler = DockerHandler(self.dockerfile_content, self.valid_app_code, self.image_tag)

    def test_build_image_success_with_valid_code(self):
        """Test if Docker image build succeeds with valid Python code."""
        result = self.docker_handler.build_image()
        self.assertTrue(result)  # Expecting build to succeed

    def test_build_image_failure_with_invalid_code(self):
        """Test if Docker image build fails with invalid Python code."""
        invalid_docker_handler = DockerHandler(self.dockerfile_content, self.invalid_app_code, self.image_tag+"invalid")
        result = invalid_docker_handler.build_image()
        self.assertFalse(result)  # Expecting the build to fail

if __name__ == "__main__":
    unittest.main()
