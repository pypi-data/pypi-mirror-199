from pydantic import BaseModel


class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service

    def __init__(self, type: str, address: str, **data: Any):
        super().__init__(**data)
        self.type = type
        self.address = address