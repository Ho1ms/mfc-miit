import React, {useEffect, useState} from 'react';
import axios from "axios";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";
import {useLocation} from "react-router-dom";
import FAQ from './FAQ'
import AddFAQ from "./AddFAQ";
const FAQMessages = () => {
    const [faq, setFAQ] = useState([])
    const lang = useLocation().state.id

    useEffect(()=> {
        axios.get(apiUrl+`/config/faq?lang=${lang}`,getAuthCookie())
            .then(resp => setFAQ(resp.data))
    }, [])

    return (
        <div className={'container'}>
            <h1 className={'text-center my-3'}>Список часто задаваемых вопросов</h1>
            <AddFAQ setFAQ={setFAQ}/>
            {faq.map(faq_message => <FAQ key={faq_message.id} faq={faq_message} setFAQ={setFAQ}/>)}
        </div>
    )
}
export default FAQMessages;
