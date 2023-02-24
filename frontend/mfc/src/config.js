import React from "react";

import Main from "./components/Main";
import CertificatesList from "./components/Certificaties/CertificatesList";
import Certificates from "./components/Certificaties/Certificates";

export const apiUrl = 'http://localhost:3005'
// export const apiUrl = 'https://mfc.api.ginda.info'

export const statuses = {
    'new':'Новая',
    'active':'В работе',
    'ready':'Готова',
    'closed':'Выдана',
}

export const routes = [
    {title:'Главная',module: <Main/>, link: '/', roles: [0], navbar:true},
    {title:'Справки',module: <CertificatesList/>, link: '/certs', roles: [1,2,3], navbar:true},
    {title:'Заявки на получение справки',module: <Certificates/>, link: '/certs', link_params:['type'], roles: [1,2,3]},
]
