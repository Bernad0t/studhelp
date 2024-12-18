import { UserCreate, UserLogin } from "../../sqhemas/dto/user";

export function getUserLoginEmpty(): UserLogin{
    return(
        {
            login: "",
            password: ""
        }
    )
}

export function getUserCreateEmpty(): UserCreate{
    return(
        {
            login: "",
            password: "",
            name: "",
            role: undefined,
            qualification: undefined
        }
    )
}