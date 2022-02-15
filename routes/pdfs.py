from fastapi import APIRouter

router = APIRouter(prefix="/api/pdfs", tags=["pdfs"])

@router.get("/")
async def pdf_root():
    return "pdf root"