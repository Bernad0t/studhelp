import { useEffect, useState } from "react";
import { BrigadesDTO, CallsDispatcher, CallsMedStuffDTO } from "../../sqhemas/dto/staff";
import { ReportsDTO } from "../../sqhemas/dto/reports";
import axios from "axios";
import { SERVER } from "../../api/server";
import { NavigateFunction, useNavigate } from "react-router-dom";
import MyButton from "../../UI/MyButton/MyButton";
import TableForm from "../../components/table/table";

async function getApiData<T extends Object[]>(path: string, navigate: NavigateFunction){
    return(
        axios.get<T>(`${SERVER}/${path}`, {withCredentials: true})
        .then(({data}) => {return data})
        .catch(error => {
            console.log(error)
            if (error.status === 401)
                navigate("/auth")
            else
                return []
        })
    )
}

function useTables(): [CallsDispatcher[], CallsMedStuffDTO[], BrigadesDTO[], ReportsDTO[]]{
    const [callsDispatcher, setCallsDispatcher] = useState<CallsDispatcher[]>([])
    const [callsMedStuffDTO, setCallsMedStuffDTO] = useState<CallsMedStuffDTO[]>([])
    const [brigadesDTO, setBrigadesDTO] = useState<BrigadesDTO[]>([])
    const [reportsDTO, setReportsDTO] = useState<ReportsDTO[]>([])

    const navigate = useNavigate()

    useEffect(() => {
        getApiData<CallsDispatcher[]>("get-calls-dispatcher", navigate).then(data => data && setCallsDispatcher(data))
        getApiData<CallsMedStuffDTO[]>("get-tasks-med", navigate).then(data => data && setCallsMedStuffDTO(data))
        getApiData<BrigadesDTO[]>("get-brigades", navigate).then(data => data && setBrigadesDTO(data))
        getApiData<ReportsDTO[]>("get-reports", navigate).then(data => data && setReportsDTO(data))
    }, [])

    return [callsDispatcher, callsMedStuffDTO, brigadesDTO, reportsDTO]
}

export default function Main(){
    const tables = useTables()
    const navigate = useNavigate()

    console.log(tables, "tab")
    return(
        <div style={{width: "100%"}}>
            <div style={{width: "100%", height: "40px", display: "flex", justifyContent: "flex-end"}}>
                <div style={{width: "100px", height: "40px"}}>
                    <MyButton onClick={() => navigate("/auth")}>Авторизация</MyButton>
                </div>
            </div>
            <div style={{width: "100%", marginBottom: "30px"}}>
                {tables.map(table => <TableForm data={table}/>)}
            </div>
        </div>
    )
}