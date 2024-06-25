import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.database.models import Sauce


def create_sauce(schema: SauceCreateSchema, db: Session):
    entity = Sauce(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Sauce created with name {} and ID {}'.format(entity.name, entity.id))
    return entity


def get_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = db.query(Sauce).filter(Sauce.id == sauce_id).first()
    if entity:
        logging.info('get sauce by id {}'.format(sauce_id))
    else:
        logging.warning('no sauce by id {}'.format(sauce_id))
    return entity


def get_sauce_by_name(sauce_name: str, db: Session):
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    if entity:
        logging.info('get sauce by name {}'.format(sauce_name))
    else:
        logging.warning('no sauce by name {}'.format(sauce_name))
    return entity


def get_all_sauces(db: Session):
    return db.query(Sauce).all()


def update_sauce(sauce: Sauce, changed_sauce: SauceCreateSchema, db: Session):
    for key, value in changed_sauce.dict().items():
        setattr(sauce, key, value)

    db.commit()
    db.refresh(sauce)
    logging.info('Sauce updated with name {} and ID {}'.format(sauce.name, sauce.id))
    return sauce


def delete_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = get_sauce_by_id(sauce_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Sauce deleted with name {} and ID {}'.format(entity.name, entity.id))
    else:
        logging.warning('cannot delete sauce.no sauce by id {}'.format(sauce_id))
