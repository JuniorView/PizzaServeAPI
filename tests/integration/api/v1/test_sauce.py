import pytest

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')  # fixture for database connection
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_sauce_create_read_delete(db):
    new_sauce_name = 'Delicious Sauce Test'
    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    sauce_data = {
        'name': new_sauce_name,
        'price': 10,
        'description': 'Delicious homemade pizza sauce',
        'stock': 100,
        'sauce_spiciness': 'LOW',
    }

    sauce = SauceCreateSchema(**sauce_data)

    # Act: Add sauce to database
    db_sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = db_sauce.id

    # Assert: One more sauce in database
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before + 1

# Act: Re-read sauce from database with id
    read_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct sauce was stored in database
    assert read_sauce.id == created_sauce_id

    # Act: Re-read sauce from database with name
    read_sauce_name = sauce_crud.get_sauce_by_name(new_sauce_name, db)

    # Assert: Correct sauce was stored in database
    assert read_sauce_name.id == created_sauce_id

    # Act: Delete sauce
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of sauces in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct sauce was deleted from database
    deleted_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_sauce is None


def test_sauce_create_update_delete(db):
    sauce_name = 'Delicious Sauce Update Test'
    sauce_name_updated = 'Updated Sauce Name'
    updated_description = 'Updated description'
    updated_spiciness = 'MEDIUM'

    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    sauce_data = {
        'name': sauce_name,
        'price': 15,
        'description': 'Delicious pizza sauce updated',
        'stock': 50,
        'sauce_spiciness': 'LOW',
    }

    sauce = SauceCreateSchema(**sauce_data)

    # Act: Add sauce to database
    db_sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = db_sauce.id

    # Act: Re-read sauce from database with id
    read_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct sauce was stored in database
    assert read_sauce.id == created_sauce_id
    assert read_sauce.name == sauce_name
    assert read_sauce.price == 15
    assert read_sauce.description == 'Delicious pizza sauce updated'
    assert read_sauce.stock == 50

    # Act: Update sauce
    updated_sauce_data = SauceCreateSchema(
        name=sauce_name_updated,
        price=20,
        description=updated_description,
        stock=60,
        sauce_spiciness=updated_spiciness,
    )
    updated_sauce = sauce_crud.update_sauce(read_sauce, updated_sauce_data, db)

    # Assert: Sauce was updated correctly
    assert updated_sauce.name == sauce_name_updated
    assert updated_sauce.price == 20
    assert updated_sauce.description == updated_description
    assert updated_sauce.stock == 60
    assert updated_sauce.sauce_spiciness == updated_spiciness

    # Act: Re-read updated sauce from database with id
    read_updated_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct updated sauce was stored in database
    assert read_updated_sauce.id == created_sauce_id
    assert read_updated_sauce.name == sauce_name_updated
    assert read_updated_sauce.price == 20
    assert read_updated_sauce.description == updated_description
    assert read_updated_sauce.stock == 60
    assert read_updated_sauce.sauce_spiciness == updated_spiciness

    # Act: Delete sauce
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of sauces in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct sauce was deleted from database
    deleted_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_sauce is None
