# Python 이미지 선택
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "src.siprofile.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]