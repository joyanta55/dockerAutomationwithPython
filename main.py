import docker
import os
import shutil
import tempfile

PYTHON_IMAGE_LIST = ["python:3.7-slim", "python:3.8-slim", "python:3.9-slim", "python:3.10-slim", "python:3.11-slim", "python:3.12-slim"]

class DockerHandler:
    def __init__(self, dockerfile_content, image_tag, directory):
        self.dockerfile_content = dockerfile_content.strip()  # Strip any extra spaces around the content
        self.image_tag = image_tag
        self.directory = directory  # Directory where app.py should be
        self.client = docker.from_env()  # Docker client initialization
        self.temp_dir = None  # Will store temporary directory for cleanup

    def validate_directory(self):
        """Ensure that app.py exists in the given directory."""
        app_path = os.path.join(self.directory, "app.py")
        if not os.path.isfile(app_path):
            print(f"Error: app.py not found in the directory {self.directory}.")
            return False
        return True

    def copy_directory(self):
        """Copy the directory contents to a temporary location."""
        try:
            # Create a temporary directory to copy files to
            self.temp_dir = tempfile.mkdtemp(dir="/tmp", prefix="test_")
            print(f"Copying contents to {self.temp_dir}...")

            # Copy all files from the source directory to the temp directory
            for item in os.listdir(self.directory):
                source_item = os.path.join(self.directory, item)
                dest_item = os.path.join(self.temp_dir, item)
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item)
                else:
                    shutil.copy2(source_item, dest_item)

            # Also write the Dockerfile in the temp directory
            with open(os.path.join(self.temp_dir, "Dockerfile"), "w") as f:
                f.write(self.dockerfile_content)

            return self.temp_dir
        except Exception as e:
            print(f"Error copying directory: {e}")
            self.cleanup_temp_dir()  # Clean up if something goes wrong
            return None

    def build_image(self, temp_dir):
        """Build the Docker image from the temporary directory."""
        try:
            print(f"Building Docker image with tag: {self.image_tag} from {temp_dir}...")
            image, build_log = self.client.images.build(path=temp_dir, tag=self.image_tag)
            for line in build_log:
                if 'error' in line:
                    print(f"Build error: {line.get('error')}")
                    self.cleanup_temp_dir()  # Clean up on failure
                    return False  # Return False if there is a build error
            print(f"Docker image {self.image_tag} built successfully.")
            return True
        except docker.errors.BuildError as e:
            print(f"Build failed: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return False
        except Exception as e:
            print(f"Error building the image: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return False

    def run_container(self):
        """Run the Docker container."""
        try:
            print(f"Running the container with image: {self.image_tag}...")
            container = self.client.containers.run(self.image_tag, detach=True)
            return container
        except docker.errors.ContainerError as e:
            print(f"Error running the container: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return None
        except Exception as e:
            print(f"Error running the container: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return None

    def get_logs(self, container):
        """Get the logs from the running container."""
        try:
            logs = container.logs()
            print("Container logs:\n", logs.decode())
            return True
        except Exception as e:
            print(f"Error fetching container logs: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return False

    def stop_container(self, container):
        """Stop the container if it's running."""
        try:
            container.stop()
            print(f"Container {container.id} stopped successfully.")
            return True
        except Exception as e:
            print(f"Error stopping the container: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return False

    def remove_container(self, container):
        """Remove the container after use."""
        try:
            self.stop_container(container)  # Ensure the container is stopped first
            container.remove()
            print(f"Container {container.id} removed successfully.")
            return True
        except Exception as e:
            print(f"Error removing the container: {e}")
            self.cleanup_temp_dir()  # Clean up on failure
            return False

    def cleanup_temp_dir(self):
        """Delete the temporary directory to clean up."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"Temporary directory {self.temp_dir} cleaned up.")
            except Exception as e:
                print(f"Error cleaning up temporary directory {self.temp_dir}: {e}")
        else:
            print(f"No temporary directory to clean up or it already exists.")

    def execute(self):
        """Main method to validate, copy files, build image, run container, and fetch logs."""
        if not self.validate_directory():
            return False

        temp_dir = self.copy_directory()
        if not temp_dir:
            return False

        if not self.build_image(temp_dir):
            return False

        container = self.run_container()

        if container:
            if not self.get_logs(container):
                return False
            if not self.remove_container(container):
                return False
            # Save the successful Dockerfile content to /tmp/executionWorkspace
            dockerfile_path = os.path.join(self.directory, "Dockerfile")
            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)
            print(f"Successful Dockerfile content saved to {dockerfile_path}")
            # Cleanup temporary directory after the operation is complete
            self.cleanup_temp_dir()
            return True
        return False

def main():
    # Dockerfile content for a Python-based image
    dockerfile_content = """
    # Use an official Python runtime as a parent image
    FROM {version}

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    RUN python app.py

    # Run the application when the container starts
    CMD ["python", "app.py"]
    """

    while True:
        # Taking user input for the directory that should contain app.py

        inputOption = input("Enter 1 if you want to provide source code, Enter 2 if you want to provide the directory location where your app.py (main method) located \n")

        if inputOption != '1' and inputOption != '2':
            continue

        if inputOption == '1':

            directory = "/tmp/executionWorkspace"

            if not os.path.exists(directory):
                os.makedirs(directory)
            print("Input your source code line by line. Type 'END' (without quotes) to finish.")
            sourceCode = ""
            while True:
                line = input(">>> ")  # Prompt user with '>>> ' for each line
                if line == "END":
                    break
                sourceCode += line + "\n"  # Append each line to sourceCode
            with open(os.path.join(directory, "app.py"), "w") as file:
                file.write(sourceCode)

        if inputOption == '2':
            directory = input("Enter the directory path where your app.py file is located (type 'exit' to quit): ")

            if directory.lower() == 'exit':
                print("Exiting...")
                break

            # Check if the directory exists
            if not os.path.isdir(directory):
                print(f"Error: The directory {directory} does not exist.")
                continue

        # Define image tag
        imagName = input("Enter the docker image tag you want your docker image to tag with. No space and only small case english letter please,i.e:python-user-hello-world\n")

        image_tag = imagName

        # Create DockerHandler object and execute the steps
        print("Creating a Docker image based on your input. We'll attempt to use Python versions ranging from 3.7 to 3.12 to build the image")
        
        for version in PYTHON_IMAGE_LIST:
            dockerfile = dockerfile_content.replace("{version}", version)
            dockerHandler = DockerHandler(dockerfile, image_tag, directory)
            if dockerHandler.execute():
                print("Execution completed successfully with python version " + version)
                break
            else:
                print("Execution failed. Please check the logs for errors.")

if __name__ == "__main__":
    main()
