export default function MyButton({onClick, children, ...props}){
    return(
        <button onClick={onClick} {...props} style={{width: "100%", height: "100%", backgroundColor: "#AFAFAF", border: "1px solid #000", borderRadius: "5px"}}>{children}</button>
    )
}