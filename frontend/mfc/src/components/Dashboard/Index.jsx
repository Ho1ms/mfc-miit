import React, {useState, useEffect} from 'react';
import axios from "axios";
import DistributionByType from "./DistributionByType";
import DistributionByDate from "./DistributionByDate";
const Index = () => {
    const data_by_percent = {
        count:300,
        labels:['Справки об обучении в ВУЗе','Справки о размере стипендии'],
        rows:[30,20],
        colors:['#FF0000','#FF7400']
    }
    const data_by_date = {
        dates: ['01.03','02.03','03.03','04.03','05.03'],
        data: [54,32,45,87,23]
    }
    return (
        <div>
            <h1 className={'my-5 text-center'}>Статистика</h1>
            <div className={'d-flex justify-content-between'}>
                <DistributionByType data={data_by_percent}/>
                <DistributionByDate data={data_by_date}/>
            </div>
        </div>
    )
}
export default Index