import enum
import uuid

from pydantic import BaseModel


# Enum for Spiciness
class Spiciness(str, enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class SauceBaseSchema(BaseModel):
    name: str
    price: float
    description: str
    spiciness: Spiciness

    class Config:
        orm_mode = True


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID
    spiciness: Spiciness


class SauceListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
