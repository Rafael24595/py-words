import uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.on_event('shutdown')
def shutdown_event():
    exit()

def init() -> None:    
    serve()
    
def serve():
    uvicorn.run(app, host='0.0.0.0', port=5000)

def exit() -> None:
    exit

if __name__ == '__main__':
    init()