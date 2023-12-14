from config import PROM

metrics = PROM.get_current_metric_value(
    metric_name="mysql_up")

for metric in metrics:
    value=bool(metric['value'][1])
    print(value)