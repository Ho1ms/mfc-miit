import axios from "axios";
import React, {useContext} from "react";
import {NavLink} from "react-router-dom";

import {apiUrl, routes} from "../config";
import {authContext} from "./Context";
import {getAuthCookie, isAuth} from "../modules";
import logo from "../static/logo_white.png";

const Navbar = () => {
    const {User, setUser} = useContext(authContext)

    function logout() {
        axios.get(apiUrl + '/auth/logout', getAuthCookie())
        window.localStorage.removeItem('hash')
        setUser({})
    }

    return (
        <nav className='navbar navbar-expand-lg navbar-dark' style={{backgroundColor:'#1B365D'}}>
            <div className="container-fluid">
                <NavLink to={'/'} className={'nav-brand'}>
                    <img alt={'rut-miit'} src={logo} width="256px" height="55px" className=' navbar-brand'/>
                </NavLink>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        {routes.map((route, index) => {
                            if (isAuth(User, route)) {
                                return (
                                    <li className="nav-item">
                                        <NavLink to={route.link} className={'nav-link'}>{route.title}</NavLink>
                                    </li>
                                )
                            }
                        })}


                    </ul>
                    <button className="btn btn-outline-light" onClick={logout}>Выйти</button>
                </div>
            </div>
        </nav>
    )
}
export default Navbar;