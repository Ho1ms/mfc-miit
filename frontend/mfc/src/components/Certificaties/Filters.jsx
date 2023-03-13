import React from "react";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import {useLocation} from "react-router-dom";

const Filters = ({filter, setFilter}) => {
    const state = useLocation().state

    function sortHandle({target:{value, checked}}) {
        setFilter({
            ...filter,
            [value]: checked
        })
    }
    function filterHandle({target:{value, name, checked}}) {
        console.log(filter, value, name)
        if (name==='status') {
            let array = [...filter.statuses]

            if (checked) {
                array.push(value)
            } else {
                array = array.filter(status => status !== value)
            }

            setFilter({
                ...filter,
                statuses: array
            })

        } else {
            setFilter({
                ...filter,
                [name]:value
            })
        }
    }

    return (
        <>

        <div className="offcanvas offcanvas-end p-3" data-bs-scroll="true" tabIndex="-1"
             id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
            <h3>Фильтры</h3>
            <div>
                <div className="mb-3">
                    <label className="form-label">Поиск по номеру</label>
                    <input type="number" defaultValue={filter.number} onBlur={filterHandle} name='id' className="form-control"/>

                </div>
                <div className="mb-3">
                    <label className="form-label">По группе</label>
                    <input type="text" defaultValue={filter.group_name} onBlur={filterHandle} name='group_name' className="form-control"/>
                </div>
                <div className="mb-3">
                    <label className="form-label">По ФИО</label>
                    <input type="text" defaultValue={filter.author} onBlur={filterHandle} name='author' className="form-control"/>

                </div>
                <div className='mb-3'>
                    <label className="form-label">По статусу</label>

                    <div className="list-group">

                        <label className="list-group-item">
                            <input className="form-check-input me-1" type="checkbox" defaultChecked={filter.statuses.includes('new')} onChange={filterHandle} value="new" name='status'/>
                            Новые
                        </label>
                        <label className="list-group-item">
                            <input className="form-check-input me-1" type="checkbox" defaultChecked={filter.statuses.includes('active')} onChange={filterHandle} value="active" name='status'/>
                            В работе
                        </label>
                        <label className="list-group-item">
                            <input className="form-check-input me-1" type="checkbox" defaultChecked={filter.statuses.includes('ready')} onChange={filterHandle} value="ready" name='status'/>
                            Готова
                        </label>
                        <label className="list-group-item">
                            <input className="form-check-input me-1" type="checkbox" defaultChecked={filter.statuses.includes('closed')} onChange={filterHandle} value="closed" name='status'/>
                            Выданы
                        </label>
                    </div>
                    </div>
                <div className="mb-3">
                    <label className="form-label">Лимит</label>
                    <select  defaultValue={filter.limit} onChange={filterHandle} name='limit' className="form-control">
                        {[50,100,250, 500].map((val, index) => {
                            return (
                                <option value={val} key={index} defaultChecked={filter.limit === val}>{val}</option>
                            )
                        })}
                    </select>

                </div>

            </div>
            <h3>Сортировать</h3>

            <div className="form-check">
                <input className="form-check-input" type="checkbox" defaultChecked={filter.sort_by_new} onChange={sortHandle} value="sort_by_new"/>
                <label className="form-check-label" >
                    Сначала сначала новые
                </label>
            </div>
        </div>
        </>
    )
}

export default Filters;