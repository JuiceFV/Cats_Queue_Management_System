# Cats Queue Management System
[![Build Status](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System.svg?branch=master)](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System)
[![codecov](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System/branch/master/graph/badge.svg)](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System)

The repository represents the most integrall and most beautiful solution of the [task](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/task-description.pdf) by [russian AAA Media Corporation Rambler&Co](https://ramblergroup.com/). The jot of task's description looks like: **"Queue Managment System akin with McDonalds orders giving or with Bank client's handling process. First, an user inquires for an unique token, then using this token obtains the required service."** The full description of the task represented [below](#full-tasks-description). 

## Table of Contents

- [Cats Queue Management System](#cats-queue-management-system)
  - [Table of Contents](#table-of-contents)
  - [Full Task's Description](#full-tasks-description)
  - [Pre-Installation requirements](#pre-installation-requirements)
  - [Installation](#installation)
    - [Instalation using Docker](#instalation-using-docker)
    - [Instalation using setuptools](#instalation-using-setuptools)
    - [Installation using Pipfile](#installation-using-pipfile)
  - [Advanced configuration](#advanced-configuration)
    - [Configuration File](#configuration-file)
    - [Cmd/Terminal parameters](#cmdterminal-parameters)
  - [Usage](#usage)
  - [Demeanor description](#demeanor-description)
  - [Issues I haven't solved, yet](#issues-i-havent-solved-yet)

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
* The second option is to use setup.py. In this purpose merely install the [python 3](https://www.python.org/downloads/). Also we shall to have [PostgreSQL](https://www.postgresql.org/) database.
* The third way is prettiy akin with second one, hence you also need the [python 3](https://www.python.org/downloads/) and [PostgreSQL](https://www.postgresql.org/).

## Installation
The common steps for all 3 cases are:

>\> git clone https://github.com/JuiceFV/Cats_Queue_Management_System.git

>\> cd Cats_Queue_Management_System
### Instalation using Docker

<h4>0. Application's configuration for Docker</h4>

It's important to check configuration. If you going to use docker, I created the configuration specified for docker. There is the definition in the [Dockerfile](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/Dockerfile) which copies the configuration from [config_for_docker.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/config_for_docker.yaml) to [basic configuration file](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/config.yaml):
```docker
RUN cat ./config_for_docker.yaml > ./application/config.yaml
```
Modify [config_for_docker.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/config_for_docker.yaml) as you want so. However, if you wish to launch the application set *run_type* as **debug** or **release**. In purpose to familiarize to configuration file [follow ahead](#configuration-file).

<h4>1. Docker Launching</h4>

Launch the docker. It depends on OS.

<details>
<summary><b>Linux</b></summary>

>\> sudo service docker start

</details>

<details>
<summary><b>Windows</b></summary>

Press on *Docker Desktop* then wait until the whale's icon become stable.

![image](https://user-images.githubusercontent.com/35202460/82753528-fb1c9680-9dce-11ea-92e9-d0df50ecbfcc.png)
![image](https://user-images.githubusercontent.com/35202460/82753541-15ef0b00-9dcf-11ea-872a-89d3087f10b8.png)

**Note:** If you're installing the repository not to the C-drive (I mean the drive where the Docker placed, in my case it is "C"), then you should add up whether your drive or the path to the cloned repository in the *Docker Dashboard -> Settings -> Resources -> File Sharing* as exploring directory.

![image](https://user-images.githubusercontent.com/35202460/82753884-0c1ad700-9dd2-11ea-99a7-fb53f9ada099.png)
![image](https://user-images.githubusercontent.com/35202460/82753940-64ea6f80-9dd2-11ea-8d1b-0c40a812ff8e.png)


</details>

Then build the docker container using this command:
>\> docker-compose up application

<h4>
2. Harvesting the result
</h4>

Then, whereas the docker build will has freezed merely follow the link.
> http:\\\localhost:8080 

### Instalation using setuptools

<h4>
0. Preparing virtual enviroment
</h4>

First, install virtual enviroment.
>\> pip install virtualenv

Then sets virtual enviroment up:
>\> python3 -m venv env

The start the enviroment up:

<details>
<summary><b>Linux</b></summary>

>\> source env/bin/activate

</details>

<details>
<summary><b>Windows</b></summary>

>\> cd env/Scripts

>\> activate

>\> cd ../..

</details>

Then you should install required packages.
>\> pip install -r requirements.txt

<h4>
1. Build the application
</h4>

The next step is building the app:

>\> python3 setup.py develop

**Note**: Please do not use the *python3 setup.py install*. I do not fucking aware why it doesn't work.

<h4>
2. Preparing PostgreSQL database
</h4>

Before the application starting you should create the database. For this use the command below:
>\> createdb -U postgres CatsQMS

Then initializing the [table](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/sources/database/init.sql)
>\> psql -U postgres -d CatsQMS -f application/sources/database/init.sql

**Note:** if you don't want to modify the [config.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/config.yaml) - set the password of PostgreSQL as **12345qwerty**, because this one I used.

<h4>
3. Start the application
</h4>

Launch the application:
1. --test - test-mode, launches the tests for the application.
2. --debug - debug-mode, launches the application with actions's logging.
3. --release - release-mode, does the same as the debug-mode but without logging.
>\> start_app --debug

Follow the link:
> http:\\\localhost:8080 

### Installation using Pipfile

<h4>
0. Preparing virtual enviroment
</h4>

The installation is pretty similar with previous one.
First:
>\> pip install pipenv

Then instead of `python -m venv env` just seize:
>\> pipenv shell

As soon as you type it, virtual enviroment will already activated. 
Then install required packages:
>\> pipenv install --dev


<h4>
1. Preparing PostgreSQL database
</h4>

Before the application starting you should create the database. For this purpose use the command below:
>\> createdb -U postgres CatsQMS

Then initializing the [table](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/sources/database/init.sql)
>\> psql -U postgres -d CatsQMS -f application/sources/database/init.sql

<h4>
2. Start the application
</h4>

Then start the application:
>\> python3 application/entry.py --debug

Follow the link:
> http:\\\localhost:8080 

## Advanced configuration
A little bit regard the configuration of the application.
### Configuration File
This file placed at [application-dir](https://github.com/JuiceFV/Cats_Queue_Management_System/tree/master/application). Let's take it apart:
```yaml
database_config:
  host: localhost
  user: postgres
  password: 12345qwerty
  port: 5432
  database: CatsQMS

run_type: debug
```
- *database_config* - it's the configuration for your database. The config could be represented in two ways. First one is the *uri link*. In the [PostgreSQL docs](https://www.postgresql.org/docs/9.3/libpq-connect.html#AEN39692) it's clearly described. The second one is the list of metadata, as so I did.
  - *host* - the host where database is placed. Default is the localhost.
  - *user* - the user of database. Default user is *postgres*.
  - *password* - the password you set when you were installing PostgreSQL.
  - *port* - listening port for connection between database and application. Default is *5432*.
  - *database* - the name of database to which you want to connect.

For obtaining more information about database configuration's parameters - just follow the [link](https://magicstack.github.io/asyncpg/current/api/index.html#connection)

- *run_type* - apparently it is the type which defines some changes of application's demeanor.
  - *test* - the service doesn't launch, however tests for the entire application do.
  - *debug* - application launches with loggin of users's actions.
  - *release* - virtually the same as the debug except the logging.

**Configuration file for Docker**
My advice for you: DO NOT MODIFY FIELDS EXCEPT *run_type*.
The configuration is pretty akin with main config, except *database_config*:*host*. In the [docker-compose.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/docker-compose.yaml) you can emphasize the string, where database service named as *db*. The Docker writes the name of the db-service into the `etc/hosts` as *ip-psqlserver: db*. The *run_type* works likelihood as in the basic [config.yaml](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/config.yaml)
```yaml
services: 
    db:
        image: postgres
        volumes: 
            - ./application/sources/database/:/docker-entrypoint-initdb.d/
        environment:
            - POSTGRES_DB=CatsQMS
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=12345qwerty
```
### Cmd/Terminal parameters
In the [entry.py](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/entry.py) defined the parser which parses command line arguments:
```python
parser.add_argument('--host', help="Host to listen", default='0.0.0.0')
parser.add_argument('--port', help="Port to accept connection", default=8080)
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Path to configuration file")
parser.add_argument('--test', help="The run-type sets as test", action='store_true')
parser.add_argument('--debug', help="The run-type sets as debug", action='store_true')
parser.add_argument('--release', help="The run-type sets as release", action='store_true')
```
Let's scuttle across them:
* *--host* - the host for the application, default is 0.0.0.0. The example: `start_app --host 127.0.0.1`
* *--port* - the port to accept connection. default is 8080. The example: `start_app --port 6080`
* *--config* - the custom config file, which adding up to the basick config file. 
The example: `start_app --config <path to your custom config>`
* *--test* - the application will have launched in the test-mode. The example: `start_app --test`
* *--debug* - the application will have launched in the debug-mode. The example: `start_app --debug`
* *--release* - the application will have launched in the debug-mode. The example: `start_app --release`

## Usage
The full demeanor description follows [ahead](#demeanor-description).
Ok, let's consider that we've went through the [installation](#installation). You should see such web page.

There is the only index page you get when following the link.
![image](https://user-images.githubusercontent.com/35202460/82739615-789dc380-9d49-11ea-98a5-31456a4be8be.png)

So, let's take apart each part.
1. *Dark Blue* - there is the only button which returns your unique token.
2. *Orange* - this part represents the queue. Each column able to contain for 16 tokens.
3. *Green* - the part where you can obtain an image.
![image](https://user-images.githubusercontent.com/35202460/82739604-63289980-9d49-11ea-99a1-d451e0f9107b.png)

When you pressed the "Get-Token" button, a token will has been representing for you only for 15 seconds. You can copy your token.
![image](https://user-images.githubusercontent.com/35202460/82739623-9539fb80-9d49-11ea-9f91-5e8b7ae2f041.png)

Tokens's queue representing the entire tokens's queue. The behavior made by using the [SSE](https://en.wikipedia.org/wiki/Server-sent_events) ([Server Sent Events](https://en.wikipedia.org/wiki/Server-sent_events)). As I said earlier each column holds only 16 tokens, if the position of a token is higher than 64, therefore this token will be represented as soon as the available place appears in the forth column.
![image](https://user-images.githubusercontent.com/35202460/82739636-b1d63380-9d49-11ea-978f-73d8f745bde4.png)

After you typed the token and send a request. In proper case you shall get the kitty-image which will be available for 60 seconds. Also you can download this image.
![image](https://user-images.githubusercontent.com/35202460/82739644-cf0b0200-9d49-11ea-9102-78a6adb7a6d2.png)

## Demeanor description
Here I represent the detailed-described behavior.
So, I would like to begin from that the service represents the [Queue Data Structure](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)). The structure works according FIFO rule.
1. If an user took a token, he should seize it within 60 seconds from the moment when it became first. When 60 seconds out - his token will automatically popped from a queue.
2. If an user used his token and now he is interacting with an image, then the timer (60 seconds) for the new first place is freezing until the user which interacting with image finishes.
3. If user's token is not first in a queue and you trying to get an image, then an user will obtain the alert, that it's not his turn.
4. If an user trying to obtain an image using not existing token - then he will be banned. YES, AND I DO NOT CARE IF YOU WRONG.
5. If database is empty and an user trying to get an image then he will get appropriate alert.
6. If an user was banned then he can't use the service. His ip will shoved into [.ip_banlist](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/application/.ip_banlist)
7. An user has the only 60 seconds to interact with image.

That's all as I think so. However if I recall something then I will add it up.
## Issues I haven't solved, yet

Fill usage explanations