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
The above command does two things. 1) Mounts the host /tmp directory with the docker image /tmp directory, 2) allow container to communicate with the host Docker daemon (a.k.a `Docker-in-Docker`). 

### What it does
This code takes two types of input.
#### Source code input
The user input their python code on console
#### Source code directory where `app.py` located on your host machine.
The user input the file system location where app.py resides.
### Validation and Docker Image Generation
In both cases, the tool will validate your code or project directory by creating a Docker image based on that source code, building it against different Python versions. The resulting Docker image is then pushed to your host's Docker registry.

Once built, you can run your application anywhere by simply executing:
```
docker run -it YourApplication
```
