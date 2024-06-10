import uuid
import logging
from typing import List

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageSchema, BeverageCreateSchema, BeverageListItemSchema
from app.database.connection import SessionLocal

beverage_not_found = 'Beverage not found'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get('', response_model=List[BeverageListItemSchema], tags=['beverage'])
def get_all_beverages(db: Session = Depends(get_db)):
    beverages = beverage_crud.get_all_beverages(db)
    logging.info(f'Got {len(beverages)} beverages')
    return beverages


@router.post('', response_model=BeverageSchema, status_code=status.HTTP_201_CREATED, tags=['beverage'])
def create_beverage(beverage: BeverageCreateSchema,
                    request: Request,
                    db: Session = Depends(get_db)):
    beverage_found = beverage_crud.get_beverage_by_name(beverage.name, db)

    if beverage_found:
        logging.error('Beverage already exists with name {}'.format(beverage_found.name))
        url = request.url_for('get_beverage', beverage_id=beverage_found.id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_beverage = beverage_crud.create_beverage(beverage, db)
    logging.info('Beverage created with name {}'.format(new_beverage.name))
    return new_beverage


@router.put('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def update_beverage(
        beverage_id: uuid.UUID,
        changed_beverage: BeverageCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    beverage_found = beverage_crud.get_beverage_by_id(beverage_id, db)

    if beverage_found:
        if beverage_found.name == changed_beverage.name:
            beverage_crud.update_beverage(beverage_found, changed_beverage, db)
            logging.error('No changes detected for beverage with Name {}'.format(beverage_found.name))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            beverage_name_found = beverage_crud.get_beverage_by_name(changed_beverage.name, db)
            if beverage_name_found:
                url = request.url_for('get_beverage', beverage_id=beverage_name_found.id)
                logging.error('Beverage already exists with name {}'.format(beverage_found.name))
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_beverage = beverage_crud.create_beverage(changed_beverage, db)
                response.status_code = status.HTTP_201_CREATED
                logging.info('Beverage updated with name {}'.format(updated_beverage.name))
    else:
        logging.error(f'Beverage not found with id {beverage_id}')
        raise HTTPException(status_code=404, detail=beverage_not_found)

    return updated_beverage


@router.get('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def get_beverage(
        beverage_id: uuid.UUID,
        db: Session = Depends(get_db),
):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        logging.error(f'Beverage not found with id {beverage_id}')
        raise HTTPException(status_code=404, detail=beverage_not_found)
    logging.info('Beverage found with id {}'.format(beverage_id))
    return beverage


@router.delete('/{beverage_id}', response_model=None, tags=['beverage'])
def delete_beverage(
        beverage_id: uuid.UUID,
        db: Session = Depends(get_db)):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        logging.error(f'Beverage not found with id {beverage_id}')
        raise HTTPException(status_code=404, detail=beverage_not_found)

    beverage_crud.delete_beverage_by_id(beverage_id, db)
    logging.info('Beverage deleted with id {}'.format(beverage_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
