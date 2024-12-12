export default function MyInput({onChange, value, ...props}){
    return(
        <input type="text" value={value} onChange={onChange} {...props} style={{width: '100%', height: "100%", backgroundColor: "#AFAFAF", border: "1 px solid #000", borderRadius: "5px", paddingLeft: '5px'}}/>
    )
}