import axios from "axios";
import {NavLink} from "react-router-dom";
import React, {useState, useEffect} from "react";

import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import Certificates from "./Certificates";


const CertificatesList = () => {
    const [certTypes, setCertTypes] = useState([])

    useEffect(() => {
        axios.get(apiUrl + '/form/cert-list', getAuthCookie())
            .then(resp => setCertTypes(resp.data))
            .catch(e => console.log(e))
    }, [])

    return (
        <div>
            <h1 className="text-center my-4">Список справок</h1>

            {
                certTypes.map((cert, index) => {
                    return (
                        <div key={index}  className={'card my-3 p-3 w-50 mx-auto text-center'}>
                            <NavLink style={{textDecoration: 'none', 'color': 'black'}} to={`/certs/${cert.type}`}
                                     state={cert} role="button" className="collapsed">
                                <h3>Справки {cert.title}</h3>
                            </NavLink>

                        </div>
                    )
                })
            }

        </div>
    )
}

    export default CertificatesList