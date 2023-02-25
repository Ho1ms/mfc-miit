import React, {useState, useEffect} from "react";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import User from "./User";
import Form from "./Form";
import Search from "./Search"
const Tickets = () => {
    const [roles, setRoles] = useState([])
    const [users, setUsers] = useState([])
    const [target, setTarget] = useState({})

    useEffect(() => {
        axios.get(apiUrl + '/config/roles', getAuthCookie())
            .then(resp => setRoles(resp.data))
        axios.get(apiUrl + '/config/users', getAuthCookie())
            .then(resp => setUsers(resp.data))
    }, [])

    return (
        <div className="justify-content-between flex-wrap flex-md-nowrap  pt-3 pb-2 mb-3 border-bottom">
            <h1 className="h2">Список сотрудников:</h1>
            <Search setUsers={setUsers}/>
            {users.map((user) => <User key={user.id} user={user} setTarget={setTarget} roles={roles}/>)}
            <Form target={target} setTarget={setTarget} roles={roles} setUsers={setUsers}/>
        </div>
)
}
export default Tickets;