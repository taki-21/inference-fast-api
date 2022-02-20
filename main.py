from fastapi import FastAPI

app = FastAPI()

 # @はデコレーター
@app.get('/countries/{country_name}')
async def country(country_name):
    return {'country_name': country_name}
