FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY app/requirements.txt ./

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 --shell /usr/sbin/nologin --create-home appuser

WORKDIR /project

COPY --from=builder /install /usr/local

COPY app /project/app

RUN chown -R appuser:appuser /project

USER appuser

EXPOSE 8080

CMD ["python", "-m", "app.main"]
