from pydantic import BaseModel


class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service
