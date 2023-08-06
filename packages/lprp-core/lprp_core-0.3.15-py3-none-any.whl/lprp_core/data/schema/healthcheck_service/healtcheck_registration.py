from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from lprp_core.service import Service


@dataclass
class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service
