from fastapi import APIRouter

router = APIRouter(prefix="/api/xlsxs", tags=["xlsxs"])

@router.get("/")
async def xlsx_root():
    return "xlsx root"

@router.post("/read")
async def xlsx_read():
    return "xlsx read"