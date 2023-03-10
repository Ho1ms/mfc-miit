import axios from "axios";
import {Routes, Route} from "react-router-dom";
import React, {useEffect, useState} from "react";

import {apiUrl} from "../config";
import {authContext} from './Context';
import {getAuthCookie, isAuth} from "../modules";

import Login from "./Login";
import Navbar from "./Navbar";
import LoadingPage from "./LoadingPage";

import {routes} from "../config";

function App() {
    const [loading, setLoading] = useState(true)
    const [User, setUser] = useState({})

    useEffect(() => {
        axios.get(apiUrl + '/auth/me', getAuthCookie())
            .then(resp => {
                setUser(resp.data)
                setLoading(false)
            })
    }, [])

    if (loading) {
        return <LoadingPage/>
    }
    const userAuth = (User.resultCode === 2 || Object.keys(User).length === 0)
    return (
        <div>
            <authContext.Provider value={{
                User, setUser
            }}>
                {!userAuth && <Navbar/>}
                <div className={'container'}>

                    <Routes>
                        {userAuth && <Route path='*' element={<Login/>}/>}
                        {routes.map((route, index) => {
                                if (isAuth(User, route)) {
                                    return <Route key={index} element={route.module} exact
                                                  path={route.link + (route.link_params?.length > 0 ? '/:' + route.link_params.join('/:') : '')}/>
                                }
                            }
                        )}
                    </Routes>

                </div>
            </authContext.Provider>
        </div>
    );
}

export default App;
