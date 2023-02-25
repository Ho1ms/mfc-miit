import React, {useState} from "react";
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";

const Search = ({setUsers}) => {
    const [query, setQuery] = useState('')

    function search(){
        axios.get(apiUrl+`/config/users?q=${query}`, getAuthCookie())
            .then(resp => setUsers(resp.data))
    }

    function getSearch({target:{value}}) {
        setQuery(value)
    }

    return (
        <div>
            <div className="input-group my-4" style={{maxWidth: '500px'}}>

                <input type="text" name="search" className="form-control" placeholder="Найти пользователя"
                       aria-label="Запрос" aria-describedby="button-addon2" onBlur={getSearch}/>
                <button className="btn btn-outline-primary" type="submit" onClick={search}>Поиск</button>
            </div>
        </div>
    )
}
export default Search