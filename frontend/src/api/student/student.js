import axios from "axios";
import { SERVER } from "../api_source";

export async function setStudent(data){
    return axios.post(`${SERVER}/set-student`, null, {withCredentials: true, params: {data: JSON.stringify(data)}})
    .then(() => {return })
}

export async function deleteStudent(id) {
    return axios.delete(`${SERVER}/delete-student`, {params: {id: id}})
    .then(() => {return })
}

export async function updateStudent(data) {
    return axios.patch(`${SERVER}/update-student`, null, {params: {data: JSON.stringify(data)}})
    .then(() => {return })
}