from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "msg": "This is an open source project available at https://github.com/lanterno/remote_python"
    }
