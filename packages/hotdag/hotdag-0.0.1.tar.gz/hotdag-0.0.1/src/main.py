from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/manifest")
async def from_manifest(

):
    return {"message": "Hello World"}
