import { isPlainObject } from "@reduxjs/toolkit"
import "./styles.css"


function getTableFromObj(obj: Object): Object{
    const keys = Object.keys(obj)
    let res = {}
    for (const key of keys){
        if (isPlainObject(obj[key as keyof typeof obj])){
            res = {...getTableFromObj(obj[key as keyof typeof obj]), ...res}
        }
        else
            res = {...res, [key]: obj[key as keyof typeof obj]}
    }
    return res
}

export default function TableForm({data}: {data: Object[]}){
    return(
        <div className="table_stud">
            <div style={{width: "100%"}}>
                <div className="one_row" style={{backgroundColor: "#AFAFAF"}}>
                    {data.length > 0 && Object.keys(data[0]).map(name => <OneColumnName><>{name}</></OneColumnName>)}
                </div>
                {data.map(d => <OneRow data={getTableFromObj(d)}/>)}
            </div>
        </div>
    )
}

function OneRow({data}: {data: Object}){
    const keys = Object.keys(data)
    return(
        <div style={{display: "flex", alignItems: "center"}}>
            <div className="one_row">
                {keys.map(name => <OneColumnName><>{data[name as keyof typeof data].toString()}</></OneColumnName>)}
            </div>
        </div>
    )
}

function OneColumnName({children}: {children: JSX.Element}){
    return(
        <div className="column"> 
            {children}
        </div>
    )
}