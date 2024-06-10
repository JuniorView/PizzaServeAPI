import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.models import Beverage


def create_beverage(schema: BeverageCreateSchema, db: Session):
    entity = Beverage(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Beverage created with name {} and ID {}'.format(entity.name, entity.id))
    return entity


def get_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = db.query(Beverage).filter(Beverage.id == beverage_id).first()
    if entity:
        logging.info('get beverage by id {}'.format(beverage_id))
    else:
        logging.warning('no beverage found with id {}'.format(beverage_id))
    return entity


def get_beverage_by_name(beverage_name: str, db: Session):
    entity = db.query(Beverage).filter(Beverage.name == beverage_name).first()
    if entity:
        logging.info('get beverage by name {}'.format(beverage_name))
    else:
        logging.warning('no beverage found with name {}'.format(beverage_name))
    return entity


def get_all_beverages(db: Session):
    #return db.query(Beverage).all()
    beverages = db.query(Beverage).all()
    logging.info('Retrieved all beverages, count: {}'.format(len(beverages)))
    return beverages

def update_beverage(beverage: Beverage, changed_beverage: BeverageCreateSchema, db: Session):
    for key, value in changed_beverage.dict().items():
        setattr(beverage, key, value)

    db.commit()
    db.refresh(beverage)
    logging.info('Beverage updated with name {} and ID {}'.format(beverage.name, beverage.id))
    return beverage


def delete_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = get_beverage_by_id(beverage_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Beverage deleted with name {} and ID {}'.format(entity.name, entity.id))
    else:
        logging.warning('no beverage found to delete with id {}'.format(beverage_id))

