# Cats Queue Management System
[![Build Status](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System.svg?branch=master)](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System)
[![codecov](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System/branch/master/graph/badge.svg)](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System)

The repository represents the most integrall and most beautiful solution of the [task](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/task-description.pdf) by [russian AAA Media Corporation Rambler&Co](https://ramblergroup.com/). The jot of tasks's description looks like: **"Queue Managment System akin with McDonalds orders giving or with Bank client's handling process. First, an user inquires for an unique token, then using this token obtains the required service."** The full description of the task represented below. 

## Table of Contents

- [Cats Queue Management System](#cats-queue-management-system)
  - [Table of Contents](#table-of-contents)
  - [Full Task's Description](#full-tasks-description)
  - [Pre-Installation requirements](#pre-installation-requirements)
  - [Installation](#installation)
    - [Instalation using Docker](#instalation-using-docker)
    - [Instalation using setuptools](#instalation-using-setuptools)
    - [Installation using Pipfile](#installation-using-pipfile)
  - [Configuration File](#configuration-file)

## Full Task's Description
If be more accurate I translate the task from [task-description.pdf](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/task-description.pdf) over here.


>It is necessary to implement a web service of the queue management system for viewing kitties using aiohttp along the REST API.
The service provides two resources:
>- Get a token
>- Get a kitty
>
>An user, firstly, makes a GET request and gets his number in the queue. Next step, using this number, he makes a POST request to the second resource.
>* If his turn came up, then he gets a picture of a kitty.
>* If his turn did not fit, then a response is returned with a proposal to repeat request later.
>* If an user is a cheater and tries to get a kitty by a nonexistent number, then you need to deal with it with the full severity of the HTTP protocol.
>* If you took a number, but did not come for the kitty, the rest should not wait eternity. 
>
>The result should be an sdist archive suitable for installation in a virtual environment, as well as instructions in README with a description of how the service
to use.
>
>It’s not necessary for execution, but as a pros for you will be counted: a working docker file, deployment service; good code coverage with tests; web page for viewing a cat (that is, a client for a written service).

So, it's been the full description of the task.

## Pre-Installation requirements
It depends on method how you will install the application.
* The easiest way is to use [Docker](https://www.docker.com/), therefore just install the Docker and follow [ahead](#instalation-using-docker).
* The second option is to use setup.py. In this purpose merely install the [python 3](https://www.python.org/downloads/).
* The third way is prettiy akin with second one, hence you also need the [python 3](https://www.python.org/downloads/).

## Installation
The common steps for all 3 cases are:

>\> git clone https://github.com/JuiceFV/Cats_Queue_Management_System.git

>\> cd Cats_Queue_Management_System
### Instalation using Docker
It's important to check configuration. If you going to use docker, I created the configuration specified for docker. There is the definition in the [Dockerfile](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/Dockerfile) which copies the configuration from [config_for_docker.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/config_for_docker.yaml) to [basic configuration file](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/config.yaml):
```docker
RUN cat ./config_for_docker.yaml > ./application/config.yaml
```
Modify [config_for_docker.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/config_for_docker.yaml) as you want so. However, if you wish to launch the application set *run_type* as **debug** or **release**. In purpose to familiarize to configuration file [follow ahead](#configuration-file).
Launch the docker. It depends on OS.
**Linux**
>\> sudo service docker start

**Windows**
Press on *Docker Desktop* then wait until the whale's icon become stable.

Then build the docker container using this command:
>\> docker-compose up application

Then, whereas the docker build will has freezed merely follow the link.
> http:\\\localhost:8080 

### Instalation using setuptools
First, install virtual enviroment.
>\> pip install virtualenv

Then sets virtual enviroment up:
>\> python3 -m venv env

The start the enviroment up:
**Linux**
>\> source env/bin/activate

**Windows**
>\> cd env/Scripts
>\> activate
>\> cd ../..

Then you should install required packages.
>\> pip install -r requirements.txt

The next step is building the app:
**Note**: Please do not use the *python3 setup.py install*. I do not fucking aware why it doesn't work.
>\> python3 setup.py develop

As soon it finished - use the console script:
>\> start_app -d

Follow the link:
> http:\\\localhost:8080 
### Installation using Pipfile

## Configuration File


