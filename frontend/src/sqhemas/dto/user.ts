import { Qualification, Role } from "../enums/enums"

export interface UserLogin{
    login: string
    password: string
}
export interface UserCreate extends UserData, UserLogin{}

export interface UserData{
    role: Role | undefined
    name: string
    qualification: Qualification | undefined
}