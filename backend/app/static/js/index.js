const tg = window.Telegram.WebApp

tg.expand()

user = tg.initDataUnsafe.user

const config = {
    'name': 'Имя',
    'last_name': 'Фамилия',
    'father_name': 'Отчество',
    'group': 'Номер группы',
    'birthday': 'Дата рождения',
    'email': 'Электронная почта',
    'target': 'Для предоставления в',
    'count': 'Количество',
    'btn': 'Отправить заявку'
}

function invalidHandler(name) {
    console.log(name)
    alert(`Поле ${config[name]} заполнено не корректно!`)
}

function handleForm() {
    let form = {}

    Object.keys(config).forEach(name => {
        if (name === 'btn') return

        let elem = document.getElementById(name)
        form[name] = elem.value
    })

    form.user = user

    fetch('/add', {
        'method': 'POST',
        'body': JSON.stringify(form),
        'headers': {'Content-Type': 'application/json'}
    })
        .then(resp => tg.close())

}

window.onload = () => {

    Object.keys(config).forEach(name => {

        let elem = document.querySelector(`label[for=${name}]`)

        if (!elem) return

        document.getElementById(name).addEventListener(oninvalid, invalidHandler, name)
        elem.innerText = config[name]
    })

}
