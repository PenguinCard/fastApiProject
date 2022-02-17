from fastapi import APIRouter, File, UploadFile, Response

from openpyxl import load_workbook, Workbook
from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

from io import BytesIO
from zipfile import ZipFile

import re
import math

from typing import List

router = APIRouter(prefix="/api/file", tags=["file"])

# add Font
pdfmetrics.registerFont(TTFont("D2Coding", "D2Coding.ttf"))

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
    
    zio = BytesIO()
    zips = ZipFile(zio, 'w')
    
    for xlsx_file in xlsx_files:
        # Write pdf
        output = PdfFileWriter()
        
        file_name = re.sub(".xlsx", "", xlsx_file.filename)
        pdf_file = list(filter(lambda file: True if file.filename.find('{}.pdf'.format(file_name)) >= 0 else False, pdf_files))
        pdf_file = pdf_file[0]
        
        wb = load_workbook(filename=BytesIO(xlsx_file.file.read()))
        ws = wb.active
        pdf = PdfFileReader(BytesIO(pdf_file.file.read()))
        
        for num in range(pdf.getNumPages()):
            print(num)
            # col
            xlsx_num_data = "C{}".format(num + 2)
            str_list = str(ws[xlsx_num_data].value).split('\n')
            count_list = list(map(regex_count.findall, str_list))
            str_list = list(map(regex.findall, str_list))
            str_list = list(map(lambda s: s[0], str_list))
            # make tuple to lists
            str_list = list(zip(count_list, str_list))
            
            posY = 75
            posY_chk = posY

            # create pdf Text
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("D2Coding", 7)  # set Font: D2Coding, Size: 7
            
            # posY 미리 계산기능 추가
            for idx, (count, str_data) in enumerate(str_list):  # drawing Text, idx, str_data, exception case: G01305644544
                if posY_chk < 0:
                    posY_chk = posY_chk + 10
                    posY = posY + 10
                texts = re.sub(".*:|;.*", "", str_data).strip().split(',')
                text_len = math.ceil(len(texts) / 3)
                if text_len > 1:
                    for i in range(text_len):
                        posY_chk -= 10
                else:
                    posY_chk -= 10

            for idx, (count, str_data) in enumerate(str_list):  # drawing Text, idx, str_data, exception case: G01305644544
                texts = re.sub(".*:|;.*", "", str_data).strip().split(',')
                counts = re.sub('數量: ', " ", count[0])
                text_len = math.ceil(len(texts) / 3)
                if text_len > 1:
                    for i in range(text_len):
                        startPoint = i * 3
                        endPoint = (i + 1) * 3
                        write_text = ",".join(texts[startPoint:endPoint])
                        if i is text_len - 1:
                            write_text = write_text + counts
                        can.drawString(65, posY, write_text)
                        posY -= 10
                else:
                    can.drawString(65, posY, ",".join(texts) + counts)
                    posY -= 10
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            
            # get Page
            page = pdf.getPage(num)
            # page Merging
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            
        headers = { 'Content-Disposition': 'attachment; filename="union.zip"' }
            
        bio = BytesIO()
        output.write(bio)
            
        print(bio)
        zips.writestr('{}.pdf'.format(file_name), bio.getbuffer())
        
    zips.close()
    bio = BytesIO()
        
    return Response(zio.getvalue(), headers=headers)
    
    

# file 작업 multifile 파일 수신
@router.post("/merge_xlsx")
async def file_work(files: List[UploadFile] = File(...)):
    
    write_wb = Workbook()
    write_ws = write_wb.active
    
    xlsx_files = list(filter(lambda file: True if file.filename.find('.xlsx') >= 0 else False, files))
    
    for xlsx_file in xlsx_files:
        wb = load_workbook(filename=BytesIO(xlsx_file.file.read()))
        ws = wb.active
        
        idx = 1
        
        for row in ws.iter_rows(values_only=True):
            if idx != 1:
                write_ws.append(row)
            idx = idx + 1
            
    bio = BytesIO()
    write_wb.save(bio)
    
    headers = { 'Content-Disposition': 'attachment; filename="union.xlsx"' }
    
    return Response(bio.getvalue(), headers=headers)