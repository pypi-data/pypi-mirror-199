from pydantic import BaseModel
from lprp_core.service import Service


class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service
    passive: bool = True  # if passive is False, the issuing service needs to ping the active_availability method,
    # if True, the service is pinged by the healthcheck service via the is_available method