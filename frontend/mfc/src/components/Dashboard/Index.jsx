import React, {useState, useEffect} from 'react';
import axios from "axios";
import DistributionByType from "./DistributionByType";
import DistributionByDate from "./DistributionByDate";
import {apiUrl} from "../../config";
import {getAuthCookie} from "../../modules";

const Index = () => {

    const [data, setData] = useState({})

    useEffect(()=>{
        axios.get(apiUrl+'/dashboard/',getAuthCookie())
            .then(resp => setData(resp.data))
    },[])

    return (
        <div>
            <h1 className={'my-5 text-center'}>Статистика</h1>
            <div className={'row'}>
                <div className="col-3">
                    <DistributionByType data={data}/>
                </div>
                <div className="col-9">
                    <DistributionByDate data={data}/>
                </div>
            </div>
            <h3 className={'mt-5'}>Информация об услугах:</h3>

                <table className={'table table-hover my-3'}>
                    <thead>
                    <tr>
                        <th>Типы справки</th>

                        <th>Новых</th>
                        <th>В работе</th>
                        <th>Готовы к выдаче</th>
                        <th>Выдано</th>
                        <th>Всего</th>
                        <th>|</th>
                        <th>В работе</th>
                        <th>Готовы к выдаче</th>
                        <th>Выдано</th>
                        <th>Суммарно</th>
                    </tr>
                    </thead>
                    <tbody>
                    {data?.rows?.map((row, index) => {
                        return (
                            <tr key={index}>
                                <td>{data.labels[index]}</td>

                                <td>{row.new}</td>
                                <td>{row.active}</td>
                                <td>{row.ready}</td>
                                <td>{row.closed}</td>
                                <td>{row.total}</td>
                                <td>|</td>
                                <td>{row.avg_active}</td>
                                <td>{row.avg_ready}</td>
                                <td>{row.avg_closed}</td>
                                <td>{row.avg_total}</td>
                            </tr>
                        )
                    })}

                    </tbody>
                </table>

        </div>
    )
}
export default Index