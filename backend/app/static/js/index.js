const tg = window.Telegram.WebApp

tg.expand()

const type = new URL(location.href).searchParams.get('type') || 1

let config = {}


function renderForm() {
    const form = document.getElementsByTagName('form')[0]
    console.log(form)
    config.names.forEach(name => {

        const div = document.createElement('div')
        div.classList.add('mb-4')

        const label = document.createElement('label')
        label.for = name
        label.innerText = config.data[name].name
        label.classList.add('form-label')

        const input = document.createElement('input')

        input.type = config.data[name].data.type
        input.style.fontSize = '2.5vh'
        input.classList.add('form-control-lg')
        input.classList.add('form-control')
        input.id = name
        input.required = config.data[name].data.required

        if (config.data[name].data.pattern) {
            input.pattern = config.data[name].data.pattern
        }
        if (config.data[name].data.value) {
            input.value = config.data[name].data.value
        }

        form.appendChild(div)
        div.appendChild(label)
        div.appendChild(input)
    })

    let btn = document.createElement('button')
    btn.type = 'submit'
    btn.id = 'btn'
    btn.style.width = '100%'
    btn.style.fontSize = '2.5vh'
    btn.classList.add('btn')
    btn.classList.add('btn-primary')
    btn.classList.add('mt-5')
    btn.innerText = config.button
    form.appendChild(btn)

    document.getElementsByTagName('h1')[0].innerText = config.title

}

function showNotify(data){
    const class_types = ['success','warning','danger']

    const alert = document.getElementById('alert')
    const title = document.getElementById('h1_title')

    title.innerText = data.message
    alert.classList.add(`alert-${class_types[data.resultCode]}`)
    alert.style.display = 'block'
}

function handleForm() {
    let form = {}

    config.names.forEach(name => {
        if (name === 'btn') return

        let elem = document.getElementById(name)
        form[name] = elem.value
    })

    form.type = type
    form.sign = decodeURIComponent(tg.initData)

    fetch('/form/add', {
        'method': 'POST',
        'body': JSON.stringify(form),
        'headers': {'Content-Type': 'application/json'}
    })
        .then(resp => resp.json())
        .then(data => {
            if (data.resultCode === 0) {
                tg.close()
            } else {
                showNotify(data)
            }
        })
}


window.onload = () => {
    fetch(`/form/get-form?type=${type}&lang=${tg?.initDataUnsafe?.user?.language_code || 'ru'}`)
        .then(resp => resp.json())
        .then(resp => {
            config = resp

            renderForm()
        })
        .catch(e => console.log(e))

}
