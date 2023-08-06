from pydantic import BaseModel


class HealthcheckRegistration(BaseModel):
    type: str  # name of service class
    address: str  # address of service

    def __init__(self, type: str, address: str, **data: any):
        self.type = type
        self.address = address
        super().__init__(**data)
