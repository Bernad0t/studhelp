from datetime import datetime
from pydantic import BaseModel

from db.sqhemas.dto.user import UserData
from db.sqhemas.enums.status_car import StatusCar


class CallsStatusDTO(BaseModel):
    id: int
    description: str


class CallsDTO(BaseModel):
    id: int
    time_call: datetime
    type: str
    status_rel: CallsStatusDTO


class CallsDispatcher(CallsDTO):
    dispatcher_id: int


class CallsMedStuffDTO(CallsDTO):
    brigade_id: int


class CarDTO(BaseModel):
    id: int
    status: StatusCar
    location: str


class CompositionBrigadeDTO(BaseModel):
    driver_rel: UserData
    paramedic_rel: UserData
    nurse_rel: UserData
    orderly_rel: UserData


class BrigadesDTO(BaseModel):
    id: int
    composition_rel: CompositionBrigadeDTO
    car_rel: CarDTO
