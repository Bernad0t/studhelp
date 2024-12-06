export default function GetPaginationButtons(limit, this_page){
    let arr = []
    for (let i = this_page - 5 >= 1 ? this_page - 5 : 1; i < (this_page + 5 >= 10 ? this_page + 5 : 10); i++){
        if (i > limit && i !== 1)
            break
        if (i === this_page)
            arr.push({id: i, active: true})
        else
            arr.push({id: i, active: false})
    }
    console.log(limit, this_page, arr, "arr")
    return arr
}