from fastapi import APIRouter, File, UploadFile

from typing import List

router = APIRouter(prefix="/api/file", tags=["file"])

@router.get("/")
async def img_root():
    return "file root"

@router.post("/work")
async def file_work(file: List[UploadFile] = File(...)):
    print(file)
    # for f in file:
    #     content = await f.read()
    #     print(str(content))
    return "file work"