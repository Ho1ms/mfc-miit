import React, {useState, useEffect} from 'react';
import {useLocation} from "react-router-dom";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import Body from "./Body";
import Filters from "./Filters";

const Certificates = () => {

    const state = useLocation().state
    const [rows, setRows] = useState([])
    const [filter, setFilter] = useState({
        id: '',
        group_name: '',
        author: '',
        statuses: ['new', 'active'],
        sort_by_new: true,
        limit:50
    })

    useEffect(() => {
        axios.get(apiUrl+`/form/get-forms?type=${state.type}&filter=${JSON.stringify(filter)}`,getAuthCookie())
            .then(resp => setRows(resp.data?.resultCode === 2 ? [] : resp.data))
    }, [filter])

    return (
        <div className=' my-5'>
            <Body certificates={rows} filter={filter} setRows={setRows}/>

            <Filters filter={filter} setFilter={setFilter} />
        </div>
    )
}
export default Certificates