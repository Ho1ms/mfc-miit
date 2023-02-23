import React from 'react';
import {statuses} from "../../config";

const Body = ({certificates, filter}) => {

    function sortHandle(x, y) {
        return filter.sort_by_new ? y.id - x.id : x.id - y.id
    }
    function filterHandler(filter, cert) {
        const fullname = `${cert.last_name} ${cert.name} ${cert.father_name}`
        console.log(cert.id.toString(),filter.id)
        if (!cert.id.toString().includes(filter.id)) return false
        if (!cert.group_name.toLowerCase().includes(filter.group_name.toLowerCase())) return false
        if (!fullname.includes(filter.author)) return false
        if (!filter.statuses.includes(cert.status)) return false

        return true
    }

    function make_author(row) {
        return `${row.last_name} ${row.name[0]}.${row.father_name !== '' ? ' '+row.father_name[0]+'.' : ''}`
    }

    return (
        <div className='col-md-9 col-lg-10 px-md-4'>
            <h3>Список заявок</h3>

        <table className={'table table-hover'}>
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">ФИО</th>
                <th scope="col">Почта</th>
                <th scope="col">Дата рождения</th>
                <th scope="col">Группа</th>
                <th scope="col">Дата запроса</th>
                <th scope="col">Статус</th>
            </tr>
            </thead>
            <tbody>
            {certificates?.sort(sortHandle)?.map((row, index) => {
                if (filterHandler(filter, row)) {
                    return (<tr key={index} style={{cursor:'pointer'}}>
                        <td>{row.id}</td>
                        <td>{make_author(row)}</td>
                        <td>{row.email}</td>
                        <td>{row.birthday}</td>
                        <td>{row.group_name}</td>
                        <td>{row.create_at}</td>
                        <td>{statuses[row.status]}</td>
                    </tr>)
                }
            }

            )}
            </tbody>
        </table>
            </div>
    )
}

export default Body;