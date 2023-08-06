from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from lprp_core.data.schema.healthcheck_service.healtcheck_registration import HealthcheckRegistration


class AvailabilityPing(BaseModel):
    healthcheck_registration: HealthcheckRegistration
    unix_time_of_sending: int

    def __init__(self, healthcheck_registration: HealthcheckRegistration, unix_time_of_sending: int, **data: any):
        super().__init__(**data)
        self.healthcheck_registration = healthcheck_registration
        self.unix_time_of_sending = unix_time_of_sending