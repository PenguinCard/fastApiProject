
### 라이브러리 설치

<br>

#### fastapi 설치
    pip install fastapi
<br>

#### python-multipart 설치 (fast api 파일 수신 부)
    pip install python-multipart
<br>
    
#### python 서버    
    pip install uvicorn
<br>

#### openpyxl 설치(엑셀파일 읽고 쓰기)
    pip install openpyxl
<br>

#### pyspark 설치
    pip install pyspark
<br>

#### PyPDF2 설치 PDF 병합
    pip install PyPDF2
<br>

#### pdfplumber 설치 PDF 텍스트 추출
    pip install pdfplumber
<br>

#### bs4 설치 html 데이터 추출
    pip install bs4


<br>
<br>
    
### 서버 실행

#### development
    uvicorn app:app --reload 

#### production
    python3 -m uvicorn app:app --reload --host=0.0.0.0 --port=8000