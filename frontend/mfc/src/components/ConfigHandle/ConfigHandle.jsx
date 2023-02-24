import React, {useState, useEffect} from "react";
import axios from "axios";
import {apiUrl} from "../../config";
import {NavLink} from "react-router-dom";
import {getAuthCookie} from "../../modules";

const ConfigHandle = () => {
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
                        <NavLink style={{textDecoration: 'none', 'color': 'black'}} to={`/config/${lang.id}`}
                                 state={lang} role="button" className="collapsed text-center">
                            <h3>{lang.title}</h3>
                        </NavLink>
                    </div>
                )
            })}
        </div>
    )
}
    export default ConfigHandle;