import axios from "axios";
import React, {useState, useRef} from 'react';

import {apiUrl} from "../../config";
import {getAuthCookie, formHandle} from "../../modules";

const Message = ({message}) => {

    const [msg, setMsg] = useState({...message, img_del:false})
    const fileInput = useRef(null)
    const delInput = useRef(null)

    async function saveData() {
        const setHeaders = {
            headers: {
                ...getAuthCookie().headers,
                'Content-Type': 'multipart/form-data'
            }
        }

        let filename = null

        if (fileInput) {
            const resp = await axios.post(apiUrl + '/upload/messages', {'files': fileInput.current.files[0]}, setHeaders)
            filename = resp.data?.files?.slice(0)[0]
        }

        axios.put(apiUrl + '/config/messages', {...msg, 'attachment': filename}, getAuthCookie()).then(resp => {

            setMsg(m => {
                const obj = {
                    ...m,
                    ...resp.data,
                }

                if (obj.img_del) {
                    delete obj.attachment
                }

                return {
                    ...obj,
                    img_del:false
                }
            })
            alert('Данные успешно сохранены!')
        }).catch(e => {
            alert(`Возникла ошибка на сервере: ${e}`)
        })
        fileInput.current.value = ''
        delInput.current.checked = false
    }


    return (
        <div key={msg.id}>
            <a style={{textDecoration: 'none', color: 'black'}} data-bs-toggle="collapse" href={`#msg-${message.id}`}
               role="button"
               aria-expanded="true" aria-controls={msg.id} className=""><h3>Тип: {msg.type}</h3></a>
            <div
                className="pt-3 pb-2 mb-3 border-bottom multi-collapse collapse" id={`msg-${msg.id}`}>
                <h4 className="h4">Заголовок:</h4>

                <input className="form-control" type="text" style={{width: '100%', marginBottom: '10px'}}
                       name="title"
                       defaultValue={msg.title} onBlur={(e) => formHandle(setMsg, e)}/>
                <textarea className="form-control" rows="5"
                          style={{width: '100%', height: '200px', marginBottom: '10px'}}
                          name="text" defaultValue={msg.text} onBlur={(e) => formHandle(setMsg, e)}/>

                {msg.attachment && <img src={`${apiUrl}/static/messages/${msg.attachment}`}
                                        className="card-img-bottom"
                                        style={{
                                            width: '100%',
                                            maxHeight: '600px',
                                            objectFit: 'scale-down',
                                            objectPosition: '50% 50%'
                                        }}/>}

                <input type='checkbox' className="form-check-input" name='img_del' ref={delInput} defaultChecked={msg.img_del}
                       onChange={(e) => formHandle(setMsg, e)}/> Удалить
                изображение
                <input ref={fileInput} className="form-control my-3" name='attachment' type="file"/>
                <button className="btn btn-primary" onClick={saveData}>Сохранить
                </button>
            </div>
            <hr/>
        </div>
    )
}

export default Message