import pytest

import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create_read_delete(db):
    new_pizza_type_name = 'Pizza type test name'
    number_of_pizza_type_before = len(pizza_type_crud.get_all_pizza_types(db))

    # Arrange: Instantiate a new dough object for pizza type
    dough_data = {
        'name': 'Dough test name',
        'price': 10,
        'description': 'Dough test description',
        'stock': 20,
    }

    dough = DoughCreateSchema(**dough_data)
    db_dough = dough_crud.create_dough(dough, db)

    # Arrange: Instantiate a new pizza type object
    pizza_type_data = {
        'name': new_pizza_type_name,
        'price': 25,
        'description': 'Pizza type test description',
        'dough_id': db_dough.id,
    }

    pizza_type = PizzaTypeCreateSchema(**pizza_type_data)

    # Act: Add pizza type to database
    db_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    created_pizza_type_id = db_pizza_type.id

    # Assert: One more pizza type in database
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_type_before + 1

    # Act: Re-read pizza type from database
    read_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct pizza type was stored in database
    assert read_pizza_type.id == created_pizza_type_id
    assert read_pizza_type.name == new_pizza_type_name

    # Act: Re-read pizza_type from database with name
    read_pizza_type_name = pizza_type_crud.get_pizza_type_by_name(new_pizza_type_name, db)

    # Assert: Correct pizza_type was stored in database
    assert read_pizza_type_name.id == created_pizza_type_id

    # Act: Delete pizza type
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct number of pizza types in database after deletion
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_type_before

    # Assert: Correct pizza type was deleted from database
    deleted_pizza_type = pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)
    assert deleted_pizza_type is None
