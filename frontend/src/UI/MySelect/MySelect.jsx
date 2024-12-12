export default function MySelect({children, onChange, ...props}){
    return(
        <select onChange={onChange} style={{width: "100%", height: "100%"}} {...props}>
            {children}
        </select>
    )
}