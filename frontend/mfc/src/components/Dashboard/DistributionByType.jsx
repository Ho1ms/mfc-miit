import React from "react";
import {Doughnut} from "react-chartjs-2";
import {Chart, CategoryScale, ArcElement, Legend, Tooltip,Title} from "chart.js";
Chart.register(CategoryScale, ArcElement, Legend, Title,Tooltip)
const DistributionByType = ({data}) => {
    if (!Object.keys(data).length) return

    const plugins = [{
        beforeDraw: function(chart) {
            const width = chart.width,
                height = chart.height ,
                ctx = chart.ctx;

            ctx.restore();
            const fontSize = (height / 100).toFixed(2);

            ctx.font = fontSize + "em sans-serif";
            ctx.textBaseline = "top";
            const text = data.rows[0].total + data.rows[1].total,
                textX = Math.round((width - ctx.measureText(text).width) / 2),
                textY = height / 2 - 55

            ctx.fillText(text, textX, textY);
            ctx.save();
        }
    }]

    console.log(data)
    const settings = {
        legend:{
            display:true
        },
        labels: data.labels,
        datasets: [{
            label:'Заявок',
            data: [data.rows[0].total, data.rows[1].total],
            backgroundColor: data.colors,
            hoverOffset: 10
        }]
    };
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom' ,
            }

        },
    };

    return (
        <div >
            <h2 className={'text-center'}>Поступило заявок</h2>
            <Doughnut data={settings} plugins={plugins} options={options} height={'400px'} width={'400px'}/>
        </div>

    )
}

export default DistributionByType