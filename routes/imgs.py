from fastapi import APIRouter

router = APIRouter(prefix="/api/imgs", tags=["imgs"])

@router.get("/")
async def img_root():
    return "img root"