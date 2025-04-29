from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import src.upload_demo as upload_demo

app = FastAPI()

app.include_router(upload_demo.router)


@app.get("/")
async def root_post():
    return RedirectResponse(url=upload_demo.router.prefix)
