import logging

from sqlalchemy.orm import Session

from app.database.models import PizzaType


def ingredients_are_available(pizza_type: PizzaType):
    if pizza_type.dough.stock == 0:
        logging.warning(f'Pizza Type Dough {pizza_type.dough_id} Stock is 0')
        return False

    if pizza_type.sauce.stock == 0:
        logging.error(f'Pizza Type Sauce {pizza_type.sauce_id} Stock is 0')
        return False

    for topping_quantity in pizza_type.toppings:
        if topping_quantity.topping.stock < topping_quantity.quantity:
            logging.warning(f'Topping stock is smaller than topping quantity {topping_quantity.quantity} topping ID')
            return False
    logging.info(f'Topping stock is available for Pizza Type {pizza_type.name} with ID {pizza_type.id}')
    return True


def reduce_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock -= 1
    pizza_type.sauce.stock -= 1

    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock -= topping_quantity.quantity
    logging.info(f'Reduced stock of {pizza_type.dough_id}')
    db.commit()


def increase_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock += 1
    pizza_type.sauce.stock += 1

    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock += topping_quantity.quantity

    db.commit()
    logging.info(f'Increased stock of dough {pizza_type.dough_id}')
