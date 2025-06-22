from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Remote Python Executor",
    description="""
    This is a simple FastAPI application that allows you to execute Python scripts remotely.
    The scripts must define a `main()` function that returns a JSON-serializable object (dict or list).
    The execution environment is limited to a safe namespace with standard libraries
     specifically os, pandas, and numpy for now.
    """,
    summary="Execute Python scripts remotely - Demo app",
    version="0.0.1",
    contact={
        "name": "Lanterno",
        "url": "http://github.com/lanterno/",
        "email": "a@elghareeb.space",
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
)


@app.get("/")
def read_root():
    return {
        "msg": "This is an open source project available at https://github.com/lanterno/remote_python"
    }


class ScriptRequest(BaseModel):
    script: str


@app.post("/execute")
async def execute_script(request: ScriptRequest):
    # Basic validation
    if not request.script.strip():
        raise HTTPException(status_code=400, detail="Script cannot be empty.")

    # Prepare a safe namespace with standard libs
    local_namespace = {}
    allowed_globals = {
        "__builtins__": __builtins__,
        "os": __import__("os"),
        "pandas": __import__("pandas"),
        "numpy": __import__("numpy"),
    }

    try:
        exec(request.script, allowed_globals, local_namespace)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing script: {e}")

    if "main" not in local_namespace or not callable(local_namespace["main"]):
        raise HTTPException(
            status_code=400, detail="Script must define a callable main() function."
        )

    try:
        result = local_namespace["main"]()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calling main(): {e}")

    if not isinstance(result, (dict, list)):
        raise HTTPException(
            status_code=400,
            detail="main() must return a JSON-serializable object (dict or list).",
        )

    return result
