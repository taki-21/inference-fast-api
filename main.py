from fastapi import FastAPI

app = FastAPI()

 # @はデコレーター
@app.get('/')
async def index():
    return {'message': 'Hello world'}
