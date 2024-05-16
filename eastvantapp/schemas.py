from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    latitude: float
    longitude: float


class AddressCreate(AddressBase):
    pass

class Adress(AddressBase):
    id:int

    class Config:
        orm_mode=True
