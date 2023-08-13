from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi import FastAPI

from index.infrastructure.controller import controller_index 

app = FastAPI()

@app.on_event('shutdown')
def shutdown_event():
    exit()

def init() -> None:    
    serve()
    
def serve():
    ci = controller_index()
    app.include_router(ci.get_router())
    app.mount("/assets/static", StaticFiles(directory="src/assets"), name="assets")
    uvicorn.run(app, host='0.0.0.0', port=5000)

def exit() -> None:
    exit

if __name__ == '__main__':
    init()