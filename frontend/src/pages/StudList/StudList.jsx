import { useEffect, useState } from "react"
import css from "./css.module.css"
import PaginationMenu from "../../components/pagination/pagination"
import getStudents from "../../api/getStudents/getStudents"

export default function StudList(){
    const name_columns = {last_name: "Фамилия", name:  "Имя", fatherland: "Отчество", grade: "Курс", group: "Группа", institute: "Факультет"}
    const [students, setStudents] = useState(undefined)
    const [numberStudents, setNumberStudents] = useState(0)
    useEffect(() => {
        getStudents(1, 10).then((data) => {
            data = JSON.parse(data)
            setNumberStudents(data["number_students"])
            setStudents(data["students"])
        })
    }, [])

    function ChangePagination(page, per_page){
        getStudents(page, per_page).then((data) => {
            data = JSON.parse(data)
            setNumberStudents(data["number_students"])
            setStudents(data["students"])
        })
    }

    return(
        <div className={css.table_stud}>
            <PaginationMenu count_students={numberStudents} CallBack={ChangePagination}/>
            <OneRow data={name_columns} style={{backgroundColor: "#AFAFAF"}}/>
            {students !== undefined && students.map(student => <OneRow data={student}/>)}
        </div>
    )
}

function OneRow({data, style}){
    const keys = ["last_name", "name", "fatherland", "grade", "group", "institute"]
    return(
        <div className={css.one_row}>
            {keys.map(name => <OneColumnName name={data[name]} style={style}/>)}
        </div>
    )
}

function OneColumnName({name, style}){
    return(
        <div className={css.column} style={style}> 
            {name}
        </div>
    )
}