from pydantic import BaseModel
from lprp_core.service import Service


class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service