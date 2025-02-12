FROM python:3.10-slim

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . /app
WORKDIR /app

# 실행 명령어 설정
CMD ["python", "main.py"]