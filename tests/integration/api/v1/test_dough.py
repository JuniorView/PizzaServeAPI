import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')  # fixture for database connection
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dough_create_read_delete(db):
    new_dough_name = 'Delicious Dough Test'
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    dough_data = {
        'name': new_dough_name,
        'price': 10,
        'description': 'Delicious homemade pizza dough',
        'stock': 100,
    }

    dough = DoughCreateSchema(**dough_data)

    # Act: Add dough to database
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    # Assert: One more dough in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before + 1

# Act: Re-read dough from database with id
    read_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct dough was stored in database
    assert read_dough.id == created_dough_id

    # Act: Re-read dough from database with name
    read_dough_name = dough_crud.get_dough_by_name(new_dough_name, db)

    # Assert: Correct dough was stored in database
    assert read_dough_name.id == created_dough_id

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None


def test_dough_create_update_delete(db):
    dough_name = 'Delicious Dough Update Test'
    dough_name_updated = 'Updated Dough Name'
    updated_description = 'Updated description'

    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    dough_data = {
        'name': dough_name,
        'price': 15,
        'description': 'Delicious pizza dough updated',
        'stock': 50,
    }

    dough = DoughCreateSchema(**dough_data)

    # Act: Add dough to database
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    # Act: Re-read dough from database with id
    read_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct dough was stored in database
    assert read_dough.id == created_dough_id
    assert read_dough.name == dough_name
    assert read_dough.price == 15
    assert read_dough.description == 'Delicious pizza dough updated'
    assert read_dough.stock == 50

    # Act: Update dough
    updated_dough_data = DoughCreateSchema(
        name=dough_name_updated,
        price=20,
        description=updated_description,
        stock=60,
    )
    updated_dough = dough_crud.update_dough(read_dough, updated_dough_data, db)

    # Assert: Dough was updated correctly
    assert updated_dough.name == dough_name_updated
    assert updated_dough.price == 20
    assert updated_dough.description == updated_description
    assert updated_dough.stock == 60

    # Act: Re-read updated dough from database with id
    read_updated_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct updated dough was stored in database
    assert read_updated_dough.id == created_dough_id
    assert read_updated_dough.name == dough_name_updated
    assert read_updated_dough.price == 20
    assert read_updated_dough.description == updated_description
    assert read_updated_dough.stock == 60

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None
