from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi import FastAPI

from commons.configuration.configurator import configurator
from index.infrastructure.controller_index import controller_index 
from app.infrastructure.controller_app import controller_app

app = FastAPI()

@app.on_event('shutdown')
def shutdown_event():
    exit()

def init() -> None: 
    configurator.initialize()
    serve()
    
def serve():
    ci = controller_index()
    controller_app(ci)
    app.include_router(ci.router())
    app.mount("/assets/static", StaticFiles(directory="assets"), name="assets")
    uvicorn.run(app, host='0.0.0.0', port=5000)

def exit() -> None:
    exit

if __name__ == '__main__':
    init()