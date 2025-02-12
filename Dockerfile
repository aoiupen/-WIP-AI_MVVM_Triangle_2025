# 베이스 이미지 선택
ARG OS_TYPE=linux  # 기본값: linux
FROM python:3.10-slim

# pip 업그레이드
RUN pip install --upgrade pip

# 빌드 시 OS_TYPE에 따라 다른 requirements 파일 복사
ARG OS_TYPE
COPY requirements-${OS_TYPE}.txt /tmp/requirements-${OS_TYPE}.txt

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r /tmp/requirements-${OS_TYPE}.txt

# 코드 복사
COPY . /app
WORKDIR /app

# 실행 명령어 설정
CMD ["python", "main.py"]
