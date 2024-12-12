import axios from "axios";
import { SERVER } from "../api_source";

export default async function getStudents(page, per_page, search, filter){
    return axios.get(`${SERVER}/`, {params: {page: page, per_page: per_page, search_template: JSON.stringify(search), order_by: filter}})
    .then(({data}) => {return data})
}