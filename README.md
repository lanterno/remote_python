# Remote Python
Remote Python execution service

This repo is an API that allows you to execute remotely python code.

## trying the API
Right now, the project is deployed on: <Link>

### how to use it
Make sure the code you're submitting have a `main` function.
This will be called by the remote execution service. 

### API documentation
The hosted API doesn't include a UI, however, it does include an OpenAPI schema. 
Access to this schema is available at <Link>.

To view this documentation, you can navigate to https://editor.swagger.io
and replace the content there with the response you got from the API.

## Running the project locally
The project uses docker, and docker compose. it also provides a make file to simplify remembering the commands.  
Assuming you already have docker installed, run the following command to fire up the server

```shell
>>> make up
```

## Architecture and design
On top of python, this project uses `uv` as a package manager, and `fastapi` as a framework of choice.

