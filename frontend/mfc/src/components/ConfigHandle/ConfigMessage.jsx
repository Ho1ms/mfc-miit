import React, {useState, useEffect} from 'react';
import {useLocation} from "react-router-dom";
import {apiUrl} from "../../config";
import axios from "axios";
import {getAuthCookie} from "../../modules";
import Message from "./Message";

const ConfigMessage = () => {

    const [messages, setMessages] = useState([])
    const lang = useLocation().state.id

    useEffect(()=> {
        axios.get(apiUrl+`/config/messages?lang=${lang}`,getAuthCookie())
            .then(resp => setMessages(resp.data))

    }, [])


    return (
        <div className={'container'}>
            <h1 className={'text-center my-3'}>Список сообщений</h1>
            {messages.map(message => <Message key={message.id} message={message}/>)}

        </div>
    )
}

export default ConfigMessage;
