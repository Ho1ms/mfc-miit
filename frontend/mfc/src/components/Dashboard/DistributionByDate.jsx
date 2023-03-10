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
    if (!Object.keys(data).length) return

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    };
    const settings = {
        labels: data.dates.date.data,
        datasets: [...Object.entries(data.dates)].filter(([key, value]) => key !== 'date').map(([key, item]) => item)
    }
    return (
        <div className={'w-100 '} >
            <h2 >Заявки по дням</h2>
            <div>

                <Line data={settings} options={options}/>

            </div>
        </div>

    )
}
export default DistributionByDate