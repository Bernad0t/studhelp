import axios from "axios";
import { SERVER } from "../api_source";

export default async function getStudents(page, per_page){
    return axios.get(`${SERVER}/`, {params: {page: page, per_page: per_page}})
    .then(({data}) => {return data})
}