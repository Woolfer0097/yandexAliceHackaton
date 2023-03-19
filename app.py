from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from alice import (
    AliceResponse,
    main,
    first_message,
)

app = FastAPI()

connections = {}


@app.get("/", response_class=HTMLResponse)
async def root():
    # req = requests.post("http://127.0.0.1:8000/", data={"pog": "yep"})
    # return req
    return """
                <button type="submit">Submit</button>
                <button type="submit" formmethod="post">Submit using POST</button>
    """


@app.post("/")
async def root(req: Request):
    data = await req.json()
    if data["session"]["message_id"] == 0:
        return first_message()

    state = data["state"]["session"]["branch"]
    command = data["request"].get("payload", data["state"]["session"])["command"]
    user = data["session"].get("user", data["session"]["user_id"])
    if isinstance(user, dict):
        user = user["user_id"]
    match state:
        case "main":
            return main(command, data["state"]["session"], data["request"], user)
        case "practice":
            pass
        case "education":
            pass
