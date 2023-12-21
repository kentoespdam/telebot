import json
from typing import List
import requests


class DiscoveredLabels:
    __address__: str
    __metrics_path__: str
    __scheme__: str
    __scrape_interval__: str
    __scrape_timeout__: str
    job: str

    def __init__(self, __address__, __metrics_path__, __scheme__, __scrape_interval__, __scrape_timeout__, job):
        self.__address__ = __address__
        self.__metrics_path__ = __metrics_path__
        self.__scheme__ = __scheme__
        self.__scrape_interval__ = __scrape_interval__
        self.__scrape_timeout__ = __scrape_timeout__
        self.job = job


class Labels:
    instance: str
    job: str

    def __init__(self, instance, job):
        self.instance = instance
        self.job = job


class ActiveTarget:
    discoveredLabels: DiscoveredLabels
    labels: Labels
    scrapePool: str
    scrapeUrl: str
    globalUrl: str
    lastError: str
    lastScrape: str
    lastScrapeDurationSeconds: str
    health: str
    scrapeInterval: str
    scrapeTimeout: str

    def __init__(self, discoveredLabels, labels, scrapePool, scrapeUrl, globalUrl, lastError, lastScrape, lastScrapeDurationSeconds, health, scrapeInterval, scrapeTimeout):
        self.discoveredLabels = discoveredLabels
        self.labels = labels
        self.scrapePool = scrapePool
        self.scrapeUrl = scrapeUrl
        self.globalUrl = globalUrl
        self.lastError = lastError
        self.lastScrape = lastScrape
        self.lastScrapeDurationSeconds = lastScrapeDurationSeconds
        self.health = health
        self.scrapeInterval = scrapeInterval
        self.scrapeTimeout = scrapeTimeout


class PromData:
    # activeTargets: List[ActiveTarget]
    # droppedTargets: List[ActiveTarget]
    # droppedTargetCounts: dict

    def __init__(self, activeTargets: List, droppedTargets, droppedTargetCounts):
        self.activeTargets = [x for activeTarget in activeTargets for x in activeTarget]
        self.droppedTargets = droppedTargets
        self.droppedTargetCounts = droppedTargetCounts

    def __str__(self) -> str:
        return f'activeTargets:{self.activeTargets}, droppedTargets:{self.droppedTargets}, droppedTargetCounts:{self.droppedTargetCounts}'


class PromResponse:
    # status: str
    # data: PromData

    def __init__(self, status: str, data: dict):
        self.status = status
        self.data = PromData(**data)

    def __str__(self) -> str:
        return f'status:{self.status}, data{self.data}'


# class PromTargetBuilder:
#     def __init__(self, json_string: str):
#         self.json_data = json_string

#     def build(self):
#         return PromResponse(self.json_data)


url = "https://prometheus.perumdamts.id/api/v1/targets"
response = requests.get(url)
json_string = response.json()

builder = PromResponse(**json_string)
# builder = json.loads(json_string)

print(builder.data.activeTargets[0].discoveredLabels)
