from config import PROM_QUERY

label_config = {"instance": "192.168.230.84:3307"}
metric_data = PROM_QUERY.get_current_metric_value(
    metric_name="mysql_up", label_config=label_config)
print(metric_data)
value = metric_data[0]['value'][1]
print("value", value)

metric_data2= PROM_QUERY.get_current_metric_value(
    metric_name="mysql_version_info", label_config=label_config)
print(metric_data2)
version = metric_data2[0]['metric']['version']
print("version", version)