import React, {useState, useEffect} from 'react';
import axios from "axios";
import {apiUrl} from "../config";
import {getAuthCookie} from "../modules";
const Certificaties = () => {
    const [rows, setRows] = useState([])

    useEffect(() => {
        axios.get(apiUrl+'/form/get-forms',getAuthCookie())
            .then(resp => setRows(resp.data?.resultCode === 2 ? [] : resp.data))
    }, [])

    return (
        <table className={'table table-striped table-dark'} >
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">ФИО</th>
                <th scope="col">Почта</th>
                <th scope="col">Дата рождения</th>
                <th scope="col">Группа</th>
                <th scope="col">Дата запроса</th>
                <th scope="col">Написать</th>
            </tr>
            </thead>
            <tbody>
            {rows?.map((row, index) =>
                <tr key={index}>
                    <td>{row.id}</td>
                    <td>{row.author}</td>
                    <td>{row.email}</td>
                    <td>{row.birthday}</td>
                    <td>{row.group_name}</td>
                    <td>{row.create_at}</td>
                    <td><a className={'btn btn-primary'} target="_blank" href={`https://t.me/${row.username}`}>Написать в TG</a></td>
                </tr>
            )}
            </tbody>
        </table>
    )
}
export default Certificaties