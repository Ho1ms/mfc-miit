import React from 'react';
import {useLocation} from "react-router-dom";
import {statuses,statuses_buttons, statuses_styles} from "../../config";
import Cert from "./Cert";

const Body = ({certificates, filter, setRows}) => {
    const state = useLocation().state



    return (
        <div className=''>
            <h3>Справки {state.title}:</h3>
            <button className="btn btn-outline-dark my-3 px-5" type="button" data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">Фильтры
            </button>
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
            {certificates?.map(row => {
                return <Cert key={row.id} cert={row} setRows={setRows}/>
            }

            )}
            </tbody>
        </table>
            </div>
    )
}

export default Body;