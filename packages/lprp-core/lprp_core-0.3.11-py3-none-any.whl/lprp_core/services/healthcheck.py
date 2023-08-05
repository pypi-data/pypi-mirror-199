from enum import Enum

import requests
from requests import Response

from lprp_core.service import Service, optionally_syncronized


class HealthStatus(Enum):
    HEALTHY = 0
    INCREASED_RISK = 1
    TEMPORARY_ISSUE = 2
    MAJOR_ISSUE = 3
    UNDEFINED = 4


class Healthcheck(Service):
    def __init__(self, address: str):
        self.address = address

    @optionally_syncronized
    async def is_available(self) -> bool:
        response = requests.get(f"{self.address}/is_available")
        return response.json()["is_available"]

    @optionally_syncronized
    async def get_health(self) -> HealthStatus:
        response = requests.get(f"{self.address}/health/")
        return HealthStatus(response.json()["health"])

    @optionally_syncronized
    async def put_healthcheck(self, service: Service, passive: bool = True) -> bool:
        response: Response = requests.put(f"{self.address}/healthcheck/",
                                          json={"registration": {"type": type(service).__name__,
                                                                 "address": service.address,
                                                                 "passive": passive}})
        return response.status_code == 200

    @optionally_syncronized
    async def delete_healthcheck(self, service: Service, passive: bool = True) -> bool:
        response: Response = requests.delete(f"{self.address}/healthcheck/",
                                             json={"registration": {"type": type(service).__name__,
                                                                    "address": service.address,
                                                                    "passive": passive}})
        return response.status_code == 200
