import React from "react";

import Main from "./components/Main";
import Certificaties from "./components/Certificaties/Certificaties";

export const apiUrl = 'http://localhost:3005'
// export const apiUrl = 'https://mfc.api.ginda.info'

export const statuses = {
    'new':'Новая',
    'active':'В работе',
    'ready':'Готова',
    'closed':'Выдана',
}

export const routes = [
    {title:'Главная',module: <Main/>, link: '/', roles: [0]},
    {title:'Справки',module: <Certificaties/>, link: '/certs', roles: [1,2,3]}
]
