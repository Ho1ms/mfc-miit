import React from "react";
import Certificaties from "./Certificaties";

const Main = () => {
    return (
        <div className='container'>
            <h1 className={'text-center my-5'}>Список заявок</h1>
            <Certificaties/>
            <p>Тут будут ещё вкладки и дэшборд с аналиткиой разной, а пока просто заявки на получение справки</p>
        </div>

    )
}
export default Main