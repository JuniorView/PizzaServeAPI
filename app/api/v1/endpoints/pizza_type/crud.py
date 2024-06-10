import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.pizza_type.schemas import \
    PizzaTypeCreateSchema, \
    PizzaTypeToppingQuantityCreateSchema
from app.database.models import PizzaType, PizzaTypeToppingQuantity


def create_pizza_type(schema: PizzaTypeCreateSchema, db: Session):
    entity = PizzaType(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Pizza type created with Name {} and ID {}'.format(entity.name, entity.id))
    return entity


def get_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.id == pizza_type_id).first()
    if entity:
        logging.info('Pizza type with ID {} was found'.format(entity.id))
    else:
        logging.warning('Pizza type with ID {} was not found'.format(pizza_type_id))
    return entity


def get_pizza_type_by_name(pizza_type_name: str, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.name == pizza_type_name).first()
    if entity:
        logging.info('Pizza type with name {} was found'.format(entity.name))
    else:
        logging.warning('pizza type not found with name {}'.format(pizza_type_name))
    return entity


def get_all_pizza_types(db: Session):
    entities = db.query(PizzaType).all()
    return entities


def update_pizza_type(pizza_type: PizzaType, changed_pizza_type: PizzaTypeCreateSchema, db: Session):
    for key, value in changed_pizza_type.dict().items():
        setattr(pizza_type, key, value)

    db.commit()
    db.refresh(pizza_type)
    logging.info('updated pizza type with id {}'.format(pizza_type))
    return pizza_type


def delete_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = get_pizza_type_by_id(pizza_type_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Deleted pizza type with ID {}'.format(pizza_type_id))
    else:
        logging.warning('No pizza type found with ID {}'.format(pizza_type_id))


def create_topping_quantity(
        pizza_type: PizzaType,
        schema: PizzaTypeToppingQuantityCreateSchema,
        db: Session,
):
    entity = PizzaTypeToppingQuantity(**schema.dict())
    pizza_type.toppings.append(entity)
    db.commit()
    db.refresh(pizza_type)
    logging.info('Created topping quantity for pizza type with ID {}'.format(pizza_type.id))
    return entity


def get_topping_quantity_by_id(
        pizza_type_id: uuid.UUID,
        topping_id: uuid.UUID,
        db: Session,
):
    entity = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.topping_id == topping_id,
                PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id) \
        .first()
    if entity:
        logging.info('Retrieved topping quantity with ID {} for pizza type {}'.format(topping_id, pizza_type_id))
    else:
        logging.warning('No topping quantity found with ID {} for pizza type {}'.format(topping_id, pizza_type_id))
    return entity


def get_joined_topping_quantities_by_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session,
):
    entities = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id)
    if entities:
        logging.info('Retrieved topping quantities for pizza type {}'.format(pizza_type_id))
    else:
        logging.warning('No topping quantities found for pizza type {}'.format(pizza_type_id))
    return entities.all()
