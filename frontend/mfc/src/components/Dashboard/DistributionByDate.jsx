import React from "react";
import {Line} from "react-chartjs-2";
import {Chart, Legend, Tooltip, Title, PointElement, LineElement, LinearScale, CategoryScale} from "chart.js";

Chart.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);
const DistributionByDate = ({data}) => {

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    };
    const settings = {
        labels: data.dates,
        datasets: [
            {
                label: 'Dataset 1',
                data: [432, 345, 234, 654, 232],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Dataset 2',
                data: [543, 234, 764, 345, 286],
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
            },
        ]
    }
    return (
        <div className={'w-100 '} style={{height: '450px'}}>
            <h2 >Заявки по дням</h2>
            <div className={'ms-auto'} style={{height: '400px'}}>

                <Line data={settings} options={options}/>

            </div>
        </div>

    )
}
export default DistributionByDate