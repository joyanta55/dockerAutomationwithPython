# dockerAutomationwithPython

#### Prerequisite: `Docker` 

Before proceeding, ensure that Docker is accessible in a `rootless` environment on your host. To check if Docker is running in `rootless` mode, try running the following command: `docker run hello-world`. If this runs without requiring sudo, you're good to go.

## Steps
Create a python 3.12 virtual environment, and activate it.
```
python3.12 -m venv myenv dockercheck

source dockercheck/bin/activate
```


Install the pre-requisite
```
pip install -r requirements.txt
```

Run the code 

```
python main.py
```
### Docker Steps
If you don't want the complexity of creating venv, installing dependencies, Follow the Docker approach. If you have `docker` in your machine. First run

```
docker build -t dockercheck .
```
Follwed by 
```
docker run -v /tmp:/tmp -v /var/run/docker.sock:/var/run/docker.sock -v /usr/local/bin/docker:/usr/local/bin/docker -it dockercheck
```
The above command does two things. 1) Mounts the host `/tmp` directory with the docker image `/tmp` directory, 2) allow container to communicate with the host Docker daemon (a.k.a `Docker-in-Docker`). 

## What it does
This code takes two types of input.
#### Source code input
The user input their python code on console
#### Source code directory where `app.py` located on your host machine.
The user input the file system location where app.py resides.
#### Validation and Docker Image Generation
In both cases, the tool will validate your code or project directory by creating a Docker image based on that source code, building it against different Python versions. The resulting Docker image is then pushed to your host's Docker registry.

Let's go step by step. After running the tool using the docker or python command, the following prompt will ask you to make a choice:
```
Enter 1 if you want to provide source code, Enter 2 if you want to provide the directory location where your app.py (main method) located
```

If you put `1`, then the console will allow you put your python code. When you finish typing your source code, put a END at the end. This tool will validate and generate a Docker image based on the provided source code, then upload it to the host machine's Docker image list.

Here's the console log, you may find it useful
```
Enter 1 if you want to provide source code, Enter 2 if you want to provide the directory location where your app.py (main method) located 

1
Input your source code line by line. Type 'END' (without quotes) to finish.
>>> print("hello Wolrd")
>>> END
Empty requirements.txt created at /tmp/executionWorkspace/requirements.txt.
Enter the docker image tag you want your docker image to tag with. No space and only small case english letter please,i.e:python-user-hello-world
sampleimage
Creating a Docker image based on your input. We'll attempt to use Python versions ranging from 3.7 to 3.12 to build the image
Copying contents to /tmp/executionWorkspace...
Building Docker image with tag: sampleimage from /tmp/executionWorkspace...
Docker image sampleimage built successfully.
Running the container with image: sampleimage...
Container logs:
 
Container 2779ef8877923b2de05aae4598226ceec129bc90a993fa03d398aa8376e2d640 stopped successfully.
Container 2779ef8877923b2de05aae4598226ceec129bc90a993fa03d398aa8376e2d640 removed successfully.
Successful Dockerfile content saved to /tmp/executionWorkspace/Dockerfile
Execution completed successfully with python version python:3.7-slim
```
After finishing you can check your created docker image using command `docker images`

If you put `2`, then the cosole will alow you to upload a python project directory, which you want to create a docker image from. For your convenience, I uploaded a sample python project name `python_code` in this repo. If you want to use that `python_code` to check this option `2`, first copy the entire directory to `/tmp` directory.

```
cp -r python_code /tmp
```
Then in the prompt provide `/tmp/python_code` and check the validation and docker image creation. For example, the `python_code` I shared, it doesn't run on `python 3.7`, but `python 3.8`. Check the logs to understand the process.
Here's my console log, hope that helps

```
Enter 1 if you want to provide source code, Enter 2 if you want to provide the directory location where your app.py (main method) located 

2
Enter the directory path where your app.py file is located (type 'exit' to quit): /tmp/python_code
Empty requirements.txt created at /tmp/executionWorkspace/requirements.txt.
Enter the docker image tag you want your docker image to tag with. No space and only small case english letter please,i.e:python-user-hello-world
dockerfromproject
Creating a Docker image based on your input. We'll attempt to use Python versions ranging from 3.7 to 3.12 to build the image
Copying contents to /tmp/executionWorkspace...
Building Docker image with tag: dockerfromproject from /tmp/executionWorkspace...
Build failed: The command '/bin/sh -c pip install -r requirements.txt' returned a non-zero code: 1
Execution failed. Please check the logs for errors.
Copying contents to /tmp/executionWorkspace...
Building Docker image with tag: dockerfromproject from /tmp/executionWorkspace...
Docker image dockerfromproject built successfully.
Running the container with image: dockerfromproject...
Container logs:
 
Container 91ee7890fbfa1d7a7af97f6c69170137ee599962ea163107fe361a3e45e4dfb2 stopped successfully.
Container 91ee7890fbfa1d7a7af97f6c69170137ee599962ea163107fe361a3e45e4dfb2 removed successfully.
Successful Dockerfile content saved to /tmp/executionWorkspace/Dockerfile
Execution completed successfully with python version python:3.8-slim
```
Again you can chek the created docker image using `docker images` command.


