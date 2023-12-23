import os
from dotenv import load_dotenv
from prometheus_api_client import PrometheusConnect

load_dotenv()

PROM_URL=str(os.getenv("PROMETHEUS_URL"))

PROM_QUERY= PrometheusConnect(url=PROM_URL)