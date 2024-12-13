import { useEffect, useState } from "react"
import css from "./css.module.css"
import PaginationMenu from "../../components/pagination/pagination"
import getStudents from "../../api/getStudents/getStudents"
import Filter from "../../components/filter/filter"
import getEmpytyObject from "../../utils/getEmptyObject"
import MyInput from "../../UI/MyInput/MyInput"
import MyButton from "../../UI/MyButton/MyButton"
import { deleteStudent, setStudent, updateStudent } from "../../api/student/student"
import MyModal from "../../components/modal/modal"

export default function StudList(){
    const name_columns = {last_name: "Фамилия", name:  "Имя", fatherland: "Отчество", grade: "Курс", group: "Группа",
         institute: "Факультет"}
    const [students, setStudents] = useState(undefined)
    const [numberStudents, setNumberStudents] = useState(0)
    const [search, setSearch] = useState(getEmpytyObject(Object.keys(name_columns)))
    const [filter, setFilter] = useState("")
    const [page, setPage] = useState(1)
    const [perPage, setPerPage] = useState(10)
    const [change, setChange] = useState(undefined)

    useEffect(() => {
        getStudents(page, perPage, {...search, grade: isNaN(Number(search.grade)) ? undefined : Number(search.grade)}, filter)
        .then((data) => {
            data = JSON.parse(data)
            setNumberStudents(data["number_students"])
            setStudents(data["students"])
        })
    }, [filter, search, page, perPage])

    function onDelete(id){
        deleteStudent(id)
        .then(() => setStudents(students.filter(stud => stud.id !== id)))
    }

    return(
        <>
        <div style={{width: "100%"}}>
            <div style={{width: "100%", padding: "10px", display: "flex", justifyContent: "center"}}>
                <InsertForm name_fiedls={name_columns}/>
            </div>
            <div className={css.table_stud}>
                <PaginationMenu count_students={numberStudents} setLimit={setPerPage} setPage={setPage} limit={perPage}/>
                <div className={css.cont_table_and_filter}>
                    <NavigateRow data={name_columns} search={search} setSearch={setSearch}/>
                    <Filter params={name_columns} setFilter={setFilter}/>
                </div>
                {students !== undefined && students.map(student => <OneRow data={student} callDelete={onDelete} callUpdate={(data) => setChange(data)}/>)}
            </div>
        </div>
        <ChangeForm data={change} setData={setChange} name_fiedls={name_columns} 
            callBack={(data) => setStudents(students.map(stud => stud.id === data.id ? data : stud))}
        />
        </>
    )
}

function ChangeForm({data, setData, name_fiedls, callBack}){
    const [showModal, setShowModal] = useState(false)
    const keys = Object.keys(name_fiedls)

    useEffect(() => {
        setShowModal(data !== undefined)
    }, [data])
    useEffect(() => {
        if (!showModal)
            setData(undefined)
    }, [showModal])

    function submit(){
        updateStudent(data).then(() => {callBack(data); setData(undefined)})
    }

    return(
        <MyModal showModal={showModal} setShowModal={setShowModal}>
            {data && <div className={css.insert}>
                {keys.map(key => <FieldInsert field={key} placeholder={name_fiedls[key]} data={data} setData={setData}/>)}
                <div style={{width: "100%", justifyContent: "center", display: "flex"}}>
                    <div style={{width: '100px', height: "30px"}}>
                        <MyButton onClick={submit}>Сохранить</MyButton>
                    </div>
                </div>
            </div>}
        </MyModal>
    )
}

function InsertForm({name_fiedls}){
    const keys = Object.keys(name_fiedls)
    const [data, setData] = useState(getEmpytyObject(keys))
    function submit(){
        for (const key of keys){
            if (data[key] === undefined)
                return
        }
        if (isNaN(Number(data.grade)))
            return
        setStudent({...data, grade: Number(data.grade)})
        .then(() => setData(getEmpytyObject(keys)))
    }
    return(
        <div className={css.insert}>
            {keys.map(key => <FieldInsert field={key} placeholder={name_fiedls[key]} data={data} setData={setData}/>)}
            <div style={{width: "100%", justifyContent: "center", display: "flex"}}>
                <div style={{width: '100px', height: "30px"}}>
                    <MyButton onClick={submit}>Сохранить</MyButton>
                </div>
            </div>
        </div>
    )
}

function FieldInsert({field, placeholder, data, setData}){
    return(
        <div style={{width: "100%", padding: "5px"}}>
            <div>
                {placeholder}
            </div>
            <div style={{width: "100%", height: "25px"}}>
                <MyInput value={data[field] ? data[field] : ""} placeholder={placeholder} onChange={(e) => setData({...data, [field]: e.target.value})}/>
            </div>
        </div>
    )
}

function NavigateRow({data, search, setSearch}){
    const keys = Object.keys(data)
    return(
        <div className={css.one_row}>
            {keys.map(key => 
            <OneColumnName style={{backgroundColor: "#AFAFAF"}}>
                <div style={{width: "100%"}}>
                    <div style={{width: "100%"}}>
                        {data[key]}
                    </div>
                    <div style={{width: "100%", height: "30px", padding: "5px"}}>
                        <MyInput value={search[key]} onChange={
                            (e) => setSearch({...search, [key]: e.target.value.length === 0 ? undefined : e.target.value})
                        } placeholder="Найти"/>
                    </div>
                </div>
            </OneColumnName>)}
        </div>
    )
}

function OneRow({data, callDelete, callUpdate}){
    const keys = Object.keys(data)
    return(
        <div style={{display: "flex", alignItems: "center"}}>
            <div className={css.one_row}>
                {keys.map(name => name !== "id" && <OneColumnName>{data[name]}</OneColumnName>)}
            </div>
            <div style={{display: "flex"}}>
                <div style={{width: "50px", height: "30px"}}>
                    <MyButton onClick={() => callUpdate(data)}>Ред.</MyButton>
                </div>
                <div style={{width: "50px", height: "30px"}}>
                    <MyButton onClick={() => callDelete(data.id)}>Удалить</MyButton>
                </div>
            </div>
        </div>
    )
}

function OneColumnName({children, style}){
    return(
        <div className={css.column} style={style}> 
            {children}
        </div>
    )
}