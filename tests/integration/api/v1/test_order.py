import pytest

import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.order.address.crud as address_crud
import app.api.v1.endpoints.user.crud as user_crud
from app.api.v1.endpoints.order.schemas import (
    OrderCreateSchema, OrderStatus,
)
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_update_delete(db):
    # Arrange: Create a new user
    new_user = UserCreateSchema(username='test user')
    user = user_crud.create_user(new_user, db)
    user_id = user.id

    # Arrange: Create a new address and user ID
    new_address = AddressCreateSchema(
        street='Test Street', post_code='12345', house_number=1, country='Test Country',
        town='Test Town', first_name='John', last_name='Doe',
    )

    # Create an address in the database (used by the order)
    address = address_crud.create_address(new_address, db)

    # Ensure number of orders before creating a new one
    number_of_orders_before = len(order_crud.get_all_orders(db))

    # Arrange: Instantiate a new order object
    new_order = OrderCreateSchema(address=address, user_id=user_id)

    # Act: Add order to database
    db_order = order_crud.create_order(new_order, db)
    created_order_id = db_order.id

    # Assert: Order was added to the database
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before + 1

    # Act: Re-read order from database
    read_order = order_crud.get_order_by_id(created_order_id, db)

    # Assert: Correct order was stored in database
    assert read_order.id == created_order_id
    assert read_order.user_id == user_id
    assert read_order.address == db_order.address
    assert read_order.order_status == OrderStatus.TRANSMITTED

    # Act: Update order status
    updated_status = OrderStatus.PREPARING
    updated_order = order_crud.update_order_status(read_order, updated_status, db)

    # Assert: Order status was updated
    assert updated_order.order_status == updated_status

    # Act: Delete order
    order_crud.delete_order_by_id(created_order_id, db)

    # Assert: Order was deleted from the database
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before

    # Assert: Correct order was deleted from database
    deleted_order = order_crud.get_order_by_id(created_order_id, db)
    assert deleted_order is None
