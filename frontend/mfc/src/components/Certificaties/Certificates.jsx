import React, {useState, useEffect} from 'react';
import {useLocation} from "react-router-dom";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import Body from "./Body";
import Filters from "./Filters";

const Certificates = () => {
    const type = useLocation().state.type
    const [rows, setRows] = useState([])
    const [filter, setFilter] = useState({
        id: '',
        group_name: '',
        author: '',
        statuses: ['new', 'active'],
        birthday: '',
        sort_by_new: true
    })

    useEffect(() => {
        axios.get(apiUrl+`/form/get-forms?type=${type}`,getAuthCookie())
            .then(resp => setRows(resp.data?.resultCode === 2 ? [] : resp.data))
    }, [])

    return (
        <div className='row my-5'>
            <Body certificates={rows} filter={filter}/>
            <Filters filter={filter} setFilter={setFilter}/>
        </div>
    )
}
export default Certificates