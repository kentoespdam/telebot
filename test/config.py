import os
from dotenv import load_dotenv
from prometheus_api_client import PrometheusConnect

load_dotenv()

PROM = PrometheusConnect(url=str(os.getenv("PROMETHEUS_URL")))
