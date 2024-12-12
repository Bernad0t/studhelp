export default function getEmpytyObject(keys){
    let res = {}
    keys.forEach(key => {res = {...res, [key]: undefined}})
    return res
}