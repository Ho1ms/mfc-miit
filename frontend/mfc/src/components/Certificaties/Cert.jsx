import React, {useState, useEffect} from "react";
import axios from "axios";
import {useLocation} from "react-router-dom";

import {getAuthCookie} from "../../modules";
import {apiUrl, statuses, statuses_buttons, statuses_styles} from "../../config";

const Cert = ({cert, setRows}) => {
    const cert_type = useLocation().state.type
    function nextStatus() {
        axios.post(apiUrl + '/status/next', {id: cert.id, type: cert_type},getAuthCookie())
            .then(resp => {
                setRows(rows => {
                    return [...rows].map(row => {
                        if (row.id===cert.id){
                            return {
                                ...row,
                                status:resp.data.status
                            }
                        }
                        return row
                    })
                })
            })
    }

    return (
        <tr>
            <td>{cert.id}</td>
            <td>{cert.last_name}</td>
            <td>{cert.name}</td>
            <td>{cert.father_name}</td>
            <td>{cert.email}</td>
            <td>{cert.birthday}</td>
            <td>{cert.group_name}</td>
            {cert_type==='2' && <td >{cert.date_start}-{cert.date_end}</td>}

            <td>{cert.create_at}</td>
            <td>{statuses[cert.status]}</td>
            <td>
                <button className={`btn btn-${statuses_styles[cert.status]}`} disabled={cert.status === 'closed'}
                        onClick={nextStatus}>
                    {statuses_buttons[cert.status]}
                </button>
            </td>
        </tr>
    )
}
export default Cert