from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import files

app = FastAPI()

######## CORS 이슈 방지용 미들웨어
origins = [
    "http://localhost",
    "http://54.180.119.10:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#############################

######## 라우팅 추가 ###########
app.include_router(files.router)

#############################


@app.get("/")
async def main_root():
    return { "Hello": "World" }

@app.get("/default/{item_id}")
async def read_item(item_id: int):
    return { "item_id": item_id }