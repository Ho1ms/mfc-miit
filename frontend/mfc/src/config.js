import React from "react";

import Main from "./components/Main";
import CertificatesList from "./components/Certificaties/CertificatesList";
import Certificates from "./components/Certificaties/Certificates";
import Tickets from './components/Tickets/Tickets.jsx'
import ConfigHandle from './components/ConfigHandle/ConfigHandle.jsx'
import FAQHandle from './components/FAQHandle/FAQHandle.jsx'
import Users from './components/Users/Users.jsx'
import ConfigMessage from "./components/ConfigHandle/ConfigMessage";
import FAQMessages from "./components/FAQHandle/FAQMessages";

export const apiUrl = 'http://localhost:3005'
// export const apiUrl = 'https://mfc.api.ginda.info'

export const statuses = {
    'new':'Новая',
    'active':'В работе',
    'ready':'Готова',
    'closed':'Выдана',
}
export const statuses_buttons = {
    'new':'Взять в работу',
    'active':'Готова к выдаче',
    'ready':'Выдать',
    'closed':'Выдана'
}

export const statuses_styles = {
    'new':'primary',
    'active':'warning',
    'ready': 'danger',
    'closed':'success'
}
export const routes = [
    {title:'Главная',module: <Main/>, link: '/', roles: [null, 1,2,3], navbar:true},
    {title:'Справки',module: <CertificatesList/>, link: '/certs', roles: [1,2,3], navbar:true},
    {title:'Тикеты',module: <Tickets/>, link: '/tickets', roles: [1,2,3], navbar:true},
    {title:'Настройки',module: <ConfigHandle/>, link: '/config', roles: [1], navbar:true},
    {title:'Настройки',module: <ConfigMessage/>, link: '/config', link_params:['id'], roles: [1]},
    {title:'FAQ',module: <FAQHandle/>, link: '/faq', roles: [1,2], navbar:true},
    {title:'FAQ',module: <FAQMessages/>, link: '/faq',link_params:['id'], roles: [1,2]},
    {title:'Сотрудники',module: <Users/>, link: '/users', roles: [1], navbar:true},
    {title:'Заявки на получение справки',module: <Certificates/>, link: '/certs', link_params:['type'], roles: [1,2,3]},
]
