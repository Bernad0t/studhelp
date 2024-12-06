import { useEffect, useState } from "react"
import GetPaginationButtons from "../../utils/GetPaginationButtons/GetPaginationButtons"

import css from "./css.module.css"

export default function PaginationMenu({count_students, CallBack}){
    const [limit, setLimit] = useState(10)
    const [buttons, setButtons] = useState([])

    useEffect(() => {
        setButtons(GetPaginationButtons(Math.ceil(count_students / limit), 1))
    }, [count_students, limit])

    function NextPage(id){
        setButtons(GetPaginationButtons(Math.ceil(count_students / limit), id))
        CallBack(id, limit)
    }

    return(
        <div className={css.pagination}>
            <Buttons buttons={buttons} CallBack={NextPage}/>
            <div className={css.cont_select}>
                <select name="" id="" onChange={e => {setLimit(e.target.value); CallBack(1, e.target.value)}} className={css.my_select}>
                    <option disabled>Чел/стр</option>
                    <option selected value={10}>{"10/стр"}</option>
                    <option value={15}>{"15/стр"}</option>
                </select>
            </div>
        </div>
    )
}

function Buttons({buttons, CallBack}){

    function click(id){
        CallBack(id)
    }

    return(
        <div className={css.cont_buttons}>
            <div className={css.buttons}>
                {buttons.map(but => OneButton(but, click))}
            </div>
            <div style={{color: "#AFAFAF"}}>
                {buttons.length > 10 && <>...</>}
            </div>
        </div>
    )
}

function OneButton(but, click){
    return(
        <div className={css.one_but_cont}>
            <button className={css.one_but} style={but.active ? {backgroundColor: "#FFF", color: "#000"} : {}} onClick={() => click(but.id)}>{but.id}</button>
        </div>
    )
}
