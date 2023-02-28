import React, {useState,useRef} from 'react';
import {useLocation} from 'react-router-dom'
import {formHandle, getAuthCookie} from "../../modules";
import {apiUrl} from "../../config";
import axios from "axios";

const AddFAQ = ({setFAQ}) => {
    const [form, setForm] = useState({
        title:'',
        text:''
    })
    const fileInput = useRef()
    const lang = useLocation().state.id

    async function addData() {
        if (form.text === '' || form.title === '') {
            alert('Вы не заполнили все поля')
            return
        }

        const setHeaders = {
            headers: {
                ...getAuthCookie().headers,
                'Content-Type': 'multipart/form-data'
            }
        }

        let filename = null

        if (fileInput.current.files.length === 1) {
            const resp = await axios.post(apiUrl + '/upload/faq', {'files': fileInput.current.files[0]}, setHeaders)
            filename = resp.data?.files?.slice(0)[0]
        }

        axios.post(apiUrl+'/config/faq', {...form, attachment:filename, lang:lang}, getAuthCookie())
            .then(resp => {
                setFAQ(prev => {
                    return [
                        resp.data,
                        ...prev
                    ]
                })
            })
        setForm({
            title:'',
            text:''
        })
        fileInput.current.value = ''
    }
    return (
        <div className={'my-5'}>
            <a  data-bs-toggle="collapse" href={`#add`}
               role="button"
               aria-expanded="true" aria-controls={'add'} className="btn btn-outline-primary btn-lg">Добавить вопрос</a>
            <div id={'add'} className={'multi-collapse collapse my-3'}>
                <h4 className="h4">Вопрос:</h4>

                <input className="form-control" type="text" style={{width: '100%', marginBottom: '10px'}}
                       name="title" value={form.title} onChange={(e) => formHandle(setForm, e)} />
                <h4 className="h4">Ответ:</h4>

                <textarea className="form-control" rows="5"
                          style={{width: '100%', height: '200px', marginBottom: '10px'}}
                          name="text" value={form.text} onChange={(e) => formHandle(setForm, e)} />



                <input ref={fileInput} className="form-control my-3" name='attachment' type="file"/>
                <div className={'d-flex justify-content-between'}>
                    <button className="btn btn-success" onClick={addData}>
                        Добавить
                    </button>

                </div>
            </div>
        </div>
    )
}
export default AddFAQ;