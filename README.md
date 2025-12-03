# Todolist

Simple todolist with API endpoints and a deprecated command line interface.   

## Deprecation Notice (CLI)

The command-line interface (CLI) used in earlier phases is now **deprecated**.

## How It's Made:
**Tech Used:** python , python-dotenv , prompt-toolkit , colorama , poetry , PostgreSQL , docker , fastAPI , uvicorn
<br />
<br />
This is a simple object-orianted , layered and user-friendly todolist application implemented with pyhton. The services are provided via fastAPI endpoints. The data are also stored in PostgreSQL database containerized with docker.    

## What's left:

The lack of front-end is appearant. Dockerizing the project is also a top priority to have consistent runs on every device.  


## How to run:

### Requirments 

- pyhton 3. 10 and above 
- poetry to install the dependencies and run the app
- docker to run the database


### set up

1. first you need to install and set up poetry on your system. go through the [official website](https://python-poetry.org/docs/#installation) for more details.
    
2. after cloning the repo , install the dependencies with the commaid below. this will install all the dependencies listed on `pyproject.toml`
    ```bash
    poetry install
    ```

3. create the .env file from .env.example. you can change the variables to suit your needs
    ```bash
    cp .env.example .env
    ```

4. run the database in a docker container
    ```bash
    docker run --name todo-db \
    -e POSTGRES_USER=todo_user \
    -e POSTGRES_PASSWORD=todo_password \
    -e POSTGRES_DB=todo_db \
    -p 5432:5432 \
    -d postgres:16
    ```
    after this run
    ```bash
    docker ps
    ```
    to make sure it's running.<br><br>
    And if you already have the image , run 
    ```bash
    docker start todo-db
    ```

4. run the application (API endpoints)
    ```bash
    poetry run uvicorn api_main:app --reload
    ```
    after this you will have the server running. go to `http://127.0.0.1:8000/docs` to have the documentation for the API endpoints.


5. run the application (CLI - DEPRECATED)
    ```bash
    poetry run python main.py
    ```
    After this you'll enter the ClI
    <br>
    Enter `help` to have the full list of available commands
    <br>
    `exit` to leave.
    <br>
    and `clear` to clear the shell.

6. here are some example commands:

    project managment:

    ```
    project create study | exam prepration
    project list
    project edit <project_id> | "new name" | 
    project delete <project_id>
    ```

    task managment:

    ```
    task add <project_id> | "Read chapter 5" | "Finish by tomorrow" | 2026-10-18
    task list <project_id>
    task status <task_id> | done
    task delete <task_id>
    ```



### environment variales

in .env.example file there are 4 environment variables. each pushing a constraints on the app

`MAX_NUMBER_OF_PROJECTS` : the max number of projects that can exist at the same time in the app 
`MAX_NUMBER_OF_TASKS` : the max number of tasks that can exist at the same time in the app 
`MAX_NAME_WORD_LENGTH` : the max word length of any name (project and task) 
`MAX_DESC_WORD_LENGTH` : the max  word length of any description (project and task)

### CLI enhancementes

this CLI supported colored outputs and logs. on top of that the is a command history which can be travesed with arrow key up and down. 