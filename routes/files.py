from fastapi import APIRouter, File, UploadFile, Response

from openpyxl import load_workbook, Workbook
from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

from io import BytesIO

import re
import math

from typing import List

router = APIRouter(prefix="/api/file", tags=["file"])

@router.get("/")
async def img_root():
    return "file root"

@router.post("/xlsxtopdf")
async def xlsxtopdf(files: List[UploadFile] = File(...)):
    
    # filtering text
    regex = re.compile(r'\d*[가-힣].*')
    regex_count = re.compile(r'數量: \d+')
    
    xlsx_files = list(filter(lambda file: True if file.filename.find('.xlsx') >= 0 else False, files))
    pdf_files = list(filter(lambda file: True if file.filename.find('.pdf') >= 0 else False, files))
    
    for xlsx_file in xlsx_files:
        
        file_name = re.sub(".xlsx", "", xlsx_file.filename)
        pdf_file = list(filter(lambda file: True if file.filename.find('{}.pdf'.format(file_name)) >= 0 else False, pdf_files))
        pdf_file = pdf_file[0]
        
        wb = load_workbook(filename=BytesIO(xlsx_file.file.read()))
        ws = wb.active
        pdf = PdfFileReader(pdf_file)
    return 

# file 작업 multifile 파일 수신
@router.post("/merge_xlsx")
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
            
    bio = BytesIO()
    write_wb.save(bio)
    
    headers = { 'Content-Disposition': 'attachment; filename="union.xlsx"' }
    
    return Response(bio.getvalue(), headers=headers)