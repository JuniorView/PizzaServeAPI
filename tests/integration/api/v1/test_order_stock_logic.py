import uuid

import pytest

from app.api.v1.endpoints.order.stock_logic.stock_beverage_crud import beverage_is_available, change_stock_of_beverage
from app.database.connection import SessionLocal
from app.database.models import Beverage


# Fixture
@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_stock_logic(db):
    # Arrange: Create beverage with a unique name
    beverage_name = 'Test_Beverage'
    beverage = Beverage(name=beverage_name, stock=10, price=1.00, description='Test beverage')
    db.add(beverage)
    db.commit()
    beverage_id = beverage.id

    # Act & Assert: Check if beverage is available (10)
    assert beverage_is_available(beverage_id, 5, db) is True
    assert beverage_is_available(beverage_id, 10, db) is True
    assert beverage_is_available(beverage_id, 11, db) is False

    # Act & Assert: Check if non-existent beverage is not available
    non_existent_beverage_id = uuid.uuid4()
    assert beverage_is_available(non_existent_beverage_id, 1, db) is False

    # Act & Assert: Reduce stock of beverage
    assert change_stock_of_beverage(beverage_id, -5, db) is True
    assert beverage_is_available(beverage_id, 5, db) is True
    assert beverage_is_available(beverage_id, 6, db) is False

    # Act & Assert: Fail to reduce stock of beverage below zero
    assert change_stock_of_beverage(beverage_id, -6, db) is False

    # Act & Assert: Increase stock of beverage
    assert change_stock_of_beverage(beverage_id, 10, db) is True
    assert beverage_is_available(beverage_id, 15, db) is True

    # Cleanup: Remove test data
    db.delete(beverage)
    db.commit()
