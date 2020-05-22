# Cats Queue Management System
[![Build Status](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System.svg?branch=master)](https://travis-ci.org/JuiceFV/Cats_Queue_Management_System)
[![codecov](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System/branch/master/graph/badge.svg)](https://codecov.io/gh/JuiceFV/Cats_Queue_Management_System)
The repository represents the most integrall and most beautiful solution of the [task](https://github.com/JuiceFV/Cats_Queue_Management_System/blob/master/task-description.pdf) by [russian AAA Media Corporation Rambler&Co](https://ramblergroup.com/). The jot of tasks's description looks like: **"Queue Managment System akin with McDonalds orders giving or with Bank client's handling process. First, an user inquires for an unique token, then using this token obtains the required service."** The full description of the task represented below. 

## Table of Contents

- [Cats Queue Management System](#cats-queue-management-system)
  - [Table of Contents](#table-of-contents)
  - [Full Task's Description](#full-tasks-description)

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

