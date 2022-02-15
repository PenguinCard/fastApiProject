from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users, items, xlsxs, pdfs, imgs, csvs

app = FastAPI()

######## CORS 이슈 방지용 미들웨어
origins = [
    "http://localhost",
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

app.include_router(users.router)
app.include_router(items.router)
app.include_router(xlsxs.router)
app.include_router(pdfs.router)
app.include_router(imgs.router)
app.include_router(csvs.router)

@app.get("/")
async def main_root():
    return { "Hello": "World" }

@app.get("/default/{item_id}")
async def read_item(item_id: int):
    return { "item_id": item_id }