import uuid

import pytest

import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.order.address.crud as address_crud
import app.api.v1.endpoints.user.crud as user_crud
from app.api.v1.endpoints.order.schemas import (
    OrderCreateSchema, OrderStatus,
)
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.api.v1.endpoints.order.stock_logic.stock_beverage_crud import beverage_is_available, change_stock_of_beverage
from app.api.v1.endpoints.order.stock_logic.stock_ingredients_crud import increase_stock_of_ingredients, \
    reduce_stock_of_ingredients, ingredients_are_available
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal
from app.database.models import Beverage, PizzaType, Topping, Dough, PizzaTypeToppingQuantity


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_stock_management(db):
    # Arrange: Create a new beverage
    new_beverage = Beverage(name='Test Beverage', price=2.5, stock=10)
    db.add(new_beverage)
    db.commit()
    db.refresh(new_beverage)
    beverage_id = new_beverage.id

    # Act & Assert: Check if the beverage is available
    assert beverage_is_available(beverage_id, 5, db) == True
    assert beverage_is_available(beverage_id, 10, db) == True
    assert beverage_is_available(beverage_id, 11, db) == False

    # Act & Assert: Check if a non-existent beverage is available
    non_existent_beverage_id = uuid.uuid4()
    assert beverage_is_available(non_existent_beverage_id, 1, db) == False

    # Act & Assert: Change stock of the beverage
    assert change_stock_of_beverage(beverage_id, -5, db) == True
    assert beverage_is_available(beverage_id, 5, db) == True
    assert beverage_is_available(beverage_id, 6, db) == False

    # Act & Assert: Change stock to a negative value (should fail)
    assert change_stock_of_beverage(beverage_id, -6, db) == False

    # Act & Assert: Increase stock of the beverage
    assert change_stock_of_beverage(beverage_id, 10, db) == True
    assert beverage_is_available(beverage_id, 15, db) == True

    # Cleanup: Remove the test beverage
    db.delete(new_beverage)
    db.commit()

    # Act & Assert: Check if the deleted beverage is available
    assert beverage_is_available(beverage_id, 1, db) == False
