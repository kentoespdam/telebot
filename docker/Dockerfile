FROM python:latest AS base

FROM base AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM base AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./.env .
COPY ./callbacks ./callbacks
COPY ./classes ./classes
COPY ./handlers ./handlers
COPY ./schedulers ./schedulers
COPY ./services ./services
COPY ./app.py .
COPY ./config.py .

ENV PATH=/root/.local:$PATH

CMD ["python", "app.py"]
