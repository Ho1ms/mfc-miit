import React from 'react';
import {useLocation} from "react-router-dom";
import {statuses,statuses_buttons, statuses_styles} from "../../config";
import Cert from "./Cert";

const Body = ({certificates, filter, setRows}) => {
    const state = useLocation().state
    function sortHandle(x, y) {
        return filter.sort_by_new ? y.id - x.id : x.id - y.id
    }
    function filterHandler(filter, cert) {
        const fullname = `${cert.last_name} ${cert.name} ${cert.father_name}`
        if (!cert.id.toString().includes(filter.id)) return false
        if (!cert.group_name.toLowerCase().includes(filter.group_name.toLowerCase())) return false
        if (!fullname.includes(filter.author)) return false
        if (!filter.statuses.includes(cert.status)) return false

        return true
    }


    return (
        <div className='col-md-9 col-lg-10 px-md-4'>
            <h3>Справки {state.title}:</h3>

        <table className={'table table-hover'}>
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Фамилия</th>
                <th scope="col">Имя</th>
                <th scope="col">Отчество</th>
                <th scope="col">Почта</th>
                <th scope="col">Дата рождения</th>
                <th scope="col">Группа</th>
                {state.type==='2' && <th scope="col">Период</th>}
                <th scope="col">Кол-во</th>
                <th scope="col">Дата запроса</th>
                <th scope="col">Статус</th>
                <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
            {certificates?.sort(sortHandle)?.map(row => {
                if (filterHandler(filter, row)) {
                    return <Cert key={row.id} cert={row} setRows={setRows}/>
                }
            }

            )}
            </tbody>
        </table>
            </div>
    )
}

export default Body;