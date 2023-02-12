import React, {useEffect, useState} from "react";
import LoadingPage from "./LoadingPage";
import axios from "axios";
import {getAuthCookie, isAuth} from "../modules";
import {apiUrl} from "../config";
import Login from "./Login";
import {Routes, Route} from "react-router-dom";
import Main from './Main'
import {authContext} from './Context'

const routes = [
    {module: <Main/>, link: '/', roles: [0]}
]

function App() {
    const [loading, setLoading] = useState(true)
    const [User, setUser] = useState({})

    console.log(User)
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

    return (
        <div>
            <authContext.Provider value={{
                User, setUser
            }}>
                <Routes>
                    {User.resultCode === 2 && <Route path='*' element={<Login/>}/>}
                    {routes.map((route, index) => {
                        if (isAuth(User, route)) {
                            return <Route key={index} element={route.module} exact
                                          path={route.link + (route.link_params?.length > 0 ? '/:' + route.link_params.join('/:') : '')}/>
                        }
                    })}
                </Routes>
            </authContext.Provider>
        </div>
    );
}

export default App;
