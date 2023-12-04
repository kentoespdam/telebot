from datetime import datetime
from ping3 import ping, verbose_ping


class PingResult:
    def __init__(self, host: str, result: str, status: bool):
        self.host = host
        self.result = result
        self.status = status

    def __str__(self):
        return f'Host: {self.host} Result: {self.result}, Status: {self.status}'

    def __repr__(self):
        return f'Host: {self.host} Result: {self.result}, Status: {self.status}'


def ping_host(name, host):
    result = ping(host)
    print(f"{datetime.now()} - {name} - {host} - {result}")
    # if result == False or result == None:
    #     return PingResult(host, 'Host *[{serverName}]* _{host}_ is DOWN ❌', False)
    if result != None or result == False:
        time = round(result*1000)
        return PingResult(host, f'Host *[{name}]* _{host}_ is UP ✅ with {time} ms', True)
    return PingResult(host, f'Host *[{name}]* _{host}_ is DOWN ❌', False)
