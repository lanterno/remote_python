from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


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
