# 베이스 이미지로 Python 3.9 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY src ./src

# uvicorn 설치
RUN pip install uvicorn

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "src.siprofile.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]