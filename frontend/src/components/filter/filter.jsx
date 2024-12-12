import MySelect from "../../UI/MySelect/MySelect";

export default function Filter({params, setFilter}){
    const keys = Object.keys(params)
    return(
        <div style={{display: "flex", width: "60px"}}>
            <MySelect name="" id="" onChange={e => setFilter(e.target.value)}>
                <option value={""} seleсted>Без фильтра</option>
                {keys.map(key => <option value={key}>{params[key]}</option>)}
            </MySelect>
        </div>
    )
}