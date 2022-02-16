from fastapi import APIRouter, File, UploadFile, Response

from openpyxl import load_workbook, Workbook

from io import BytesIO
from typing import List

router = APIRouter(prefix="/api/file", tags=["file"])

@router.get("/")
async def img_root():
    return "file root"

# file 작업 multifile 파일 수신
@router.post("/work")
async def file_work(files: List[UploadFile] = File(...)):
    
    write_wb = Workbook()
    write_ws = write_wb.active
    
    xlsx_files = list(filter(lambda file: True if file.filename.find('.xlsx') >= 0 else False, files))
    
    for xlsx_file in xlsx_files:
        wb = load_workbook(filename=BytesIO(xlsx_file.file.read()))
        ws = wb.active
        
        idx = 1;
        
        for row in ws.iter_rows(values_only=True):
            if idx != 1:
                write_ws.append(row)
            idx = idx + 1
            
    io = BytesIO()
    write_wb.save(io)
    
    headers = { 'Content-Disposition': 'attachment; filename="union.xlsx"' }
    
    return Response(io.getvalue(), headers=headers)