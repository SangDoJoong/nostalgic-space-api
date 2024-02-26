# FROM python:3.10

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 종속성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 복사
COPY ./app /app

# 컨테이너 실행 명령 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
