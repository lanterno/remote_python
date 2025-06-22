# Remote Python
Remote Python execution service

This repo is an API that allows you to execute remotely python code.

## trying the API
Right now, the project is deployed on: <Link>

### how to use it
Make sure the code you're submitting have a `main` function.
This will be called by the remote execution service. 

### API documentation
OpenAPI (swagger UI) documenation is available at `/api/v1/docs`

## Running the project locally
The project uses docker, and docker compose. it also provides a make file to simplify remembering the commands.  
Assuming you already have docker installed, run the following command to fire up the server

### For local development, using docker compose is advised
```shell
>>> make up
```

### For production, the image is also deployable using a docker run command
```bash
>>> docker run -p 8080:8080 ghcr.io/lanterno/remote_python:latest
``` 

## Architecture and design
On top of python, this project uses `uv` as a package manager, and `fastapi` as a framework of choice.

