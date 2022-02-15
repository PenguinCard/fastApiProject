from fastapi import APIRouter

router = APIRouter(prefix="/api/items", tags=["items"])

@router.get("/")
async def item_root():
    return "item root"