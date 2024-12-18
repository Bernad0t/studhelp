import { useState } from "react";
import { UserCreate, UserLogin } from "../../sqhemas/dto/user";
import { getUserCreateEmpty, getUserLoginEmpty } from "../../utils/createEmptyObj/user";
import MyButton from "../../UI/MyButton/MyButton";
import { Role } from "../../sqhemas/enums/enums";
import axios from "axios";
import { SERVER } from "../../api/server";
import { useNavigate } from "react-router-dom";

import "./styles.css"

enum placeHolders{
    login = "логин",
    password = "пароль"
} 



async function submit(data: UserCreate | UserLogin, path: string){
    return axios.post(`${SERVER}/${path}`, data, {withCredentials: true})
    .then(() => {return})
}

export default function Authorization(){
    const [isReg, setIsReg] = useState(true)
    return(
        <div className="cont_auth">
            <div style={{width: "50%"}}>
                <div style={{width: "300px", display: "flex", justifyContent: "space-around"}}>
                    <div style={{width: "100px", height: "30px"}}>
                        <MyButton onClick={() => setIsReg(false)}>Вход</MyButton>
                    </div>
                    <div style={{width: "100px", height: "30px"}}>
                        <MyButton onClick={() => setIsReg(true)}>Регистрация</MyButton>
                    </div>
                </div>
                <div style={{display: isReg ? "none" : ""}}>
                    <Login/>
                </div>
                <div style={{display: isReg ? "" : "none"}}>
                    <Register/>
                </div>
            </div>
        </div>
    )
}

function Login(){
    const [user, setUser] = useState<UserLogin>(getUserLoginEmpty())
    const keys = Object.keys(placeHolders)

    const navigate = useNavigate()
    return(
        <div className="auth">
            {keys.map(key => <OneRow field={key} user={user} setUser={setUser}/>)}
            <div className="auth_submit">
                <MyButton onClick={() => submit(user, "sign-in").then(() => navigate("/"))}>Войти</MyButton>
            </div>
        </div>
    )
}

function Register(){
    const [user, setUser] = useState<UserCreate>(getUserCreateEmpty())
    const keys = [...Object.keys(placeHolders), "name"]

    const navigate = useNavigate()
    return(
        <div className="auth">
            {keys.map(key => <OneRow field={key} user={user} setUser={setUser}/>)}
            <div style={{display: "flex", justifyContent: "space-between"}}>
                <div>
                    Зарегистрироваться как
                </div>
                <div>
                    <select name="" id="" onChange={(e) => setUser({...user, role: Role[e.target.value as keyof typeof Role]})}>
                        <option disabled selected>Роль</option>
                        {Object.keys(Role).map(role => <option value={role}>{Role[role as keyof typeof Role]}</option>)}
                    </select>
                </div>
            </div>
            <div className="auth_submit">
                <MyButton onClick={() => submit(user, "sign-up").then(() => navigate("/"))}>Зарегистрироваться</MyButton>
            </div>
        </div>
    )
}

function OneRow<T extends UserLogin>({field, user, setUser}: {field: string, user: T, setUser:  React.Dispatch<React.SetStateAction<T>>}){
    return(
        <div className="auth_row">
            <input type="text" 
                value={user[field as keyof typeof user] as string} 
                onChange={(e) => setUser({...user, [field]: e.target.value})}
                placeholder={field}
                className="auth_input"
            />
        </div>
    )
}