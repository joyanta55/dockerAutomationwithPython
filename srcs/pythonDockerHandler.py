import docker
import os

class DockerHandler:
    def __init__(self, dockerfileContent, image_tag, userDirectory="", workingDirectory="/tmp"):
        self.dockerfile_content = dockerfileContent.strip()  # Strip any extra spaces around the content
        self.image_tag = image_tag
        self.userDirectory = userDirectory  # User input project directory where app.py should be
        self.client = docker.from_env()  # Docker client initialization
        self.workingDirectory = workingDirectory  # temporary file location where DockerHandler does it's operation. Copies content from self.userDirectory and put in self.workingDirectory before proceeding.

    def validate_directory(self):
        """Ensure that app.py exists in the given directory."""
        app_path = os.path.join(self.workingDirectory, "app.py")
        if not os.path.isfile(app_path):
            print(f"Error: app.py not found in the directory {self.workingDirectory}.")
            return False
        return True

    def create_temp_directory(self):
        # already done creating temp in write_or_copy_code_to_workspace
        
        return self.workingDirectory

    def copy_directory(self):
        """Copy the directory contents to the temporary location."""
        try:
            temp_dir = self.create_temp_directory() ##mainly the self.workingDirectory 
            print(f"Copying contents to {temp_dir}...")

            with open(os.path.join(temp_dir, "Dockerfile"), "w") as f:
                f.write(self.dockerfile_content)

            return temp_dir
        except Exception as e:
            print(f"Error copying directory: {e}")
            return None

    def build_image(self, temp_dir):
        """Build the Docker image from the temporary directory."""
        try:
            print(f"Building Docker image with tag: {self.image_tag} from {temp_dir}...")
            image, build_log = self.client.images.build(path=temp_dir, tag=self.image_tag)
            for line in build_log:
                if 'error' in line:
                    print(f"Build error: {line.get('error')}")
                    return False  # Return False if there is a build error
            print(f"Docker image {self.image_tag} built successfully.")
            return True
        except docker.errors.BuildError as e:
            print(f"Build failed: {e}")
            return False
        except Exception as e:
            print(f"Error building the image: {e}")
            return False

    def run_container(self):
        """Run the Docker container."""
        try:
            print(f"Running the container with image: {self.image_tag}...")
            container = self.client.containers.run(self.image_tag, detach=True)
            return container
        except docker.errors.ContainerError as e:
            print(f"Error running the container: {e}")
            return None
        except Exception as e:
            print(f"Error running the container: {e}")
            return None

    def get_logs(self, container):
        """Get the logs from the running container."""
        try:
            logs = container.logs()
            print("Container logs:\n", logs.decode())
            return True
        except Exception as e:
            print(f"Error fetching container logs: {e}")
            return False

    def stop_container(self, container):
        """Stop the container if it's running."""
        try:
            container.stop()
            print(f"Container {container.id} stopped successfully.")
            return True
        except Exception as e:
            print(f"Error stopping the container: {e}")
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
            return False

    def cleanup_temp_dir(self):
        """Delete the temporary directory to clean up."""
        pass
        # if os.path.exists(self.temp_dir):
        #     try:
        #         shutil.rmtree(self.temp_dir)
        #         print(f"Temporary directory {self.temp_dir} cleaned up.")
        #     except Exception as e:
        #         print(f"Error cleaning up temporary directory {self.temp_dir}: {e}")
        # else:
        #     print(f"No temporary directory to clean up or it already exists.")

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
            dockerfile_path = os.path.join(self.workingDirectory, "Dockerfile")
            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)
            print(f"Successful Dockerfile content saved to {dockerfile_path}")
            # Cleanup temporary directory after the operation is complete
            self.cleanup_temp_dir()
            return True
        return False