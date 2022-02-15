from fastapi import APIRouter

router = APIRouter(prefix="/api/csvs", tags=["csvs"])

@router.get("/")
async def csv_root():
    return "csv root"