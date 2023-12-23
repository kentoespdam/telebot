FROM python:latest AS base

FROM base AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM base AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY .env .env
COPY . .

ENV PATH=/root/.local:$PATH

CMD ["python", "main.py"]