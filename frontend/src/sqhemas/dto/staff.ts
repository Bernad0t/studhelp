import { StatusCar } from "../enums/enums"
import { UserData } from "./user"

export interface CallsStatusDTO{
    id: number
    description: string
}

export interface CallsDTO{
    id: number
    time_call: Date
    type: string
    status_rel: CallsStatusDTO
}

export interface CallsDispatcher extends CallsDTO{
    dispatcher_id: number
}

export interface CallsMedStuffDTO extends CallsDTO{
    brigade_id: number
}

export interface CarDTO{
    id: number
    status: StatusCar
    location: string
}


export interface CompositionBrigadeDTO{
    staff_rel: UserData[]
}


export interface BrigadesDTO{
    id: number
    composition_rel: CompositionBrigadeDTO
    car_rel: CarDTO
}