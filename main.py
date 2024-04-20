from fastapi import FastAPI

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def message():
    return {"message": "Hello World"}
