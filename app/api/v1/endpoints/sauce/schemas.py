import enum
import uuid

from pydantic import BaseModel


# Enum for SauceSpiciness
class SauceSpiciness(str, enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class SauceBaseSchema(BaseModel):
    name: str
    price: float
    description: str
    sauce_spiciness: SauceSpiciness

    class Config:
        orm_mode = True


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID
    sauce_spiciness: SauceSpiciness


class SauceListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
