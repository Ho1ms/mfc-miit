import React, {useEffect, useState} from "react";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import {NavLink} from "react-router-dom";

const Tickets = () => {
    const [langs, setLangs] = useState([])

    useEffect(() => {
        axios.get(apiUrl + '/config/localisations',getAuthCookie())
            .then(resp => setLangs(resp.data))
    }, [])

    return (
        <div>
            <h2 className={'text-center my-5'}>Выберите язык</h2>
            {langs.map((lang, index) => {
                return (
                    <div key={index} className={'card my-3 p-3 w-50 mx-auto'}>
                        <NavLink style={{textDecoration: 'none', 'color': 'black'}} to={`/faq/${lang.id}`}
                                 state={lang} role="button" className="collapsed text-center">
                            <h3>{lang.title}</h3>
                        </NavLink>
                    </div>
                )
            })}
        </div>
    )
}
export default Tickets;