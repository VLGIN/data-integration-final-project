from pydantic import BaseModel


class PhoneSpecs(BaseModel):
    name: str
    ram: str
    storage: str
    color: str
