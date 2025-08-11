FROM ghcr.io/astral-sh/uv:python3.10-alpine

# 패키지 업데이트 및 PostgreSQL 및 PostGIS 설치
RUN apk update \
    && apk add \
        postgresql-client \
    && rm -rf /var/cache/apk/*

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 종속성 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# 애플리케이션 소스코드 복사
COPY . .

# 컨테이너 실행 명령 설정
ENV PYTHONPATH=/app/app
CMD ["uv", "run", "uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8080"]
