import { InputHTMLAttributes } from "react";

export default function MyButton({onClick, children}: InputHTMLAttributes<HTMLButtonElement>){
    return(
        <button onClick={onClick} style={{width: "100%", height: "100%", backgroundColor: "#AFAFAF", border: "1px solid #000", borderRadius: "5px"}}>{children}</button>
    )
}