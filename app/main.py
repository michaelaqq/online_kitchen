import fastapi
import uvicorn

from app.api.api_v1.api import api_router

app = fastapi.FastAPI()

app.include_router(api_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
