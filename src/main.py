from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi import FastAPI

from commons.configuration.configurator import configurator
from infrastructure.controller.index.controller_index import controller_index 
from infrastructure.controller.app.controller_app import controller_app

app = FastAPI()

@app.on_event('shutdown')
def shutdown_event():
    exit()

def init() -> None: 
    configurator.initialize()
    serve()
    
def serve():
    ci = controller_index()
    ca = controller_app()
    app.include_router(ci.router())
    app.include_router(ca.router())
    app.mount("/assets/static", StaticFiles(directory="assets"), name="assets")
    uvicorn.run(app, host='0.0.0.0', port=5000)

def exit() -> None:
    exit

if __name__ == '__main__':
    init()