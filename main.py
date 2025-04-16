
import os
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'srcs'))
from srcs.pythonDockerHandler import DockerHandler

PYTHON_IMAGE_LIST = ["python:3.7-slim", "python:3.8-slim", "python:3.9-slim", "python:3.10-slim", "python:3.11-slim", "python:3.12-slim"]

def write_or_copy_code_to_workspace(option,source_code,user_directory,working_directory,filename="app.py") :

    # Delete previous workspace
    if os.path.normpath(user_directory) == os.path.normpath(working_directory):
        print("The user_directory and working_directory can not be equal.")
        return False
    if os.path.exists(working_directory):
       shutil.rmtree(working_directory)
    
    os.makedirs(working_directory)

    # Empty requirements.txt
    requirements_txt_path = os.path.join(working_directory, "requirements.txt")

    with open(requirements_txt_path, "w") as f:
        f.write("")  # Create an empty requirements.txt
        f.close()
        print(f"Empty requirements.txt created at {requirements_txt_path}.")

    if option == '1':
        # write the source code as filename which is app.py by default
        with open(os.path.join(working_directory, filename), "w") as f:
            f.write(source_code)
            f.close()
    if option == '2':
        # copy entire user directory to the workspace directory
        # first check if the directory contains app.py, then do the copying
        file_path = os.path.join(user_directory, "app.py")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            for item in os.listdir(user_directory):
                source_item = os.path.join(user_directory, item)
                dest_item = os.path.join(working_directory, item)
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item)
                else:
                    shutil.copy2(source_item, dest_item)
        else:
            print("You should have app.py in your project directory. If this is main.py, remane to app.py and then run.")
            return False
    return True
        
def main():
    # Dockerfile content for a Python-based image, including pip install for requirements.txt
    dockerfile_content = """
    # Use an official Python runtime as a parent image
    FROM {version}

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install dependencies from requirements.txt
    RUN pip install -r requirements.txt

    # Run app.py during the build process
    RUN python app.py

    # Run the application when the container starts
    CMD ["python", "app.py"]
    """

    while True:
        # Taking user input for the directory that should contain app.py
        userDirectory = ""
        userOption = '0'
        inputSourceCode = ""
        workingDirectory = "/tmp/executionWorkspace" # hard coded

        userOption = input("\n\nEnter 1 if you want to provide source code, Enter 2 if you want to provide the directory location where your app.py (main method) located \n\n")

        if userOption != '1' and userOption != '2':
            continue

        if userOption == '1':

            print("Input your source code line by line. Type 'END' (without quotes) to finish.")
            inputSourceCode = ""
            while True:
                line = input(">>> ")  # Prompt user with '>>> ' for each line
                if line == "END":
                    break
                inputSourceCode += line + "\n"  # Append each line to sourceCode
            #write_code_to_workspace (sourceCode, directory, "app.py")

        if userOption == '2':
            userDirectory = input("Enter the directory path where your app.py file is located (type 'exit' to quit): ")

            if userDirectory.lower() == 'exit':
                print("Exiting...")
                break

            # Check if the directory exists
            if not os.path.isdir(userDirectory):
                print(f"Error: The directory {userDirectory} does not exist.")
                continue
        
        write_or_copy_code_to_workspace(userOption,source_code=inputSourceCode,user_directory=userDirectory,working_directory=workingDirectory)

        # Define image tag
        imagName = input("Enter the docker image tag you want your docker image to tag with. No space and only small case english letter please,i.e:python-user-hello-world\n")

        image_tag = imagName

        # Create DockerHandler object and execute the steps
        print("Creating a Docker image based on your input. We'll attempt to use Python versions ranging from 3.7 to 3.12 to build the image")
        
        for version in PYTHON_IMAGE_LIST:
            dockerfile = dockerfile_content.replace("{version}", version)
            dockerHandler = DockerHandler(dockerfile, image_tag, "", workingDirectory)
            if dockerHandler.execute():
                print("Execution completed successfully with python version " + version)
                break
            else:
                print("Execution failed. Please check the logs for errors.")

if __name__ == "__main__":
    main()
