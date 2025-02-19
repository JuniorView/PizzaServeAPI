import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.database.models import Address


def create_address(schema: AddressCreateSchema, db: Session):
    entity = Address(**schema.dict())

    db.add(entity)
    db.commit()
    logging.info(f'Added new address: {entity.id} for user {entity.last_name} {entity.first_name}')
    return entity


def get_address_by_id(address_id: uuid.UUID, db: Session):
    entity = db.query(Address).filter(Address.id == address_id).first()
    logging.info(f'Retrieved address: {entity.id}')
    return entity


def delete_address_by_id(address_id: uuid.UUID, db: Session):
    entity = get_address_by_id(address_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info(f'Deleted address: {entity.id}')


def update_address(address: Address, changed_address: AddressCreateSchema, db: Session):
    for key, value in changed_address.dict().items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    logging.info(f'Updated address: {address.id}')
    return address


def get_all_addresses(db: Session):
    return db.query(Address).all()
