import os
from dotenv import load_dotenv
from prometheus_pandas import query

load_dotenv()

PROM_URL=str(os.getenv("PROMETHEUS_URL"))

PROM_QUERY= query.Prometheus(PROM_URL)