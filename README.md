# Todolist

Simple todolist with userfriendly command line interface.   

## How It's Made:
**Tech Used:** python , python-dotenv , prompt-toolkit , colorama , poetry 
<br />
<br />
This is a simple object-orianted , layered and user-friendly todolist application implemented with pyhton. Currently has a cli , will add more interfaces in the future. the app has in-memory storage and after exiting the data is lost.   

## What's left:

Firstly the stroage method needs to become persistent. For that matter db implementation will be required. other than that , though careful methods has been considered to male the command line interface user-friendy , but still the lack of front-end is appearant. API end points need to be implemented. Dockerizing the project is also a top priority to have consistent runs on every device.  


## How to run:

### Requirments 

- pyhton 3. 10 and above 
- poetry to install the dependencies and run the app

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

4. run the application 
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

5. here are some example commands:

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