import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema, ToppingListItemSchema
from app.database.models import Topping


def create_topping(schema: ToppingCreateSchema, db: Session):
    entity = Topping(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Topping created with name {} and ID {}'.format(entity.name, entity.id))
    return entity


def get_topping_by_id(topping_id: uuid.UUID, db: Session):
    entity = db.query(Topping).filter(Topping.id == topping_id).first()
    if not entity:
        logging.error('Topping not found with ID {}'.format(topping_id))
    return entity


def get_topping_by_name(topping_name: str, db: Session):
    entity = db.query(Topping).filter(Topping.name == topping_name).first()
    if not entity:
        logging.error('Topping not found with name {}'.format(topping_name))
    return entity


def get_all_toppings(db: Session):
    entities = db.query(Topping).all()
    if entities:
        return_entities = []
        for entity in entities:
            list_item_entity = ToppingListItemSchema(
                **{'id': entity.id, 'name': entity.name, 'price': entity.price, 'description': entity.description})
            return_entities.append(list_item_entity)
        return return_entities
    else:
        logging.warning('No toppings found.')
    return entities


def update_topping(topping: Topping, changed_topping: ToppingCreateSchema, db: Session):
    for key, value in changed_topping.dict().items():
        setattr(topping, key, value)

    db.commit()
    db.refresh(topping)
    logging.info('Topping updated with ID {}'.format(topping.id))
    return topping


def delete_topping_by_id(topping_id: uuid.UUID, db: Session):
    entity = get_topping_by_id(topping_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Topping deleted with ID {}'.format(topping_id))
