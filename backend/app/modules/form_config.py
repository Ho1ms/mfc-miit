titles = {
        'ru': {
            '1': 'Справка с места учёбы',
            '2': 'Справка о размере стипендии',
        },
        'en': {
            '1': 'Certificate from the place of study',
            '2': 'Certificate of the amount of the scholarship',
        }
    }

type_settings = {
        'name': {'required': True, 'type': 'text','pattern': '[А-ЯA-Z]{1}[а-яa-z]{0,32}'},
        'last_name': {'required': True, 'type': 'text','pattern': '[А-ЯA-Z]{1}[а-яa-z]{0,32}'},
        'father_name': {'type': 'text','pattern': '[А-ЯA-Z]{0,1}[а-яa-z]{0,32}'},
        'birthday': {'required': True, 'type': 'date'},
        'email': {'required': True, 'type': 'text',
                  'pattern': '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'},
        'target': {'required': True, 'type': 'text','pattern':'.{0,256}'},
        'group_name': {'required': True, 'type': 'text', 'pattern': '[А-Яа-я]{3,5}-\d\d\d'},
        'count': {'required': True, 'type': 'number', 'min': 1, 'max': 10, 'value': 1},
        'date_start': {'required': True, 'type': 'date'},
        'date_end': {'required': True, 'type': 'date'},
    }

config = {
        'ru': {
            'name': 'Имя',
            'last_name': 'Фамилия',
            'father_name': 'Отчество',
            'group_name': 'Номер группы',
            'birthday': 'Дата рождения',
            'date_start': 'Начало периода',
            'date_end': 'Конец периода',
            'email': 'Электронная почта',
            'target': 'Место предоставления',
            'count': 'Количество',
        },
        'en': {
            'name': 'Name',
            'last_name': 'Surname',
            'father_name': 'Middle name',
            'group_name': 'Group number',
            'birthday': 'Date of birth',
            'date_start': 'Beginning of the Period',
            'date_end': 'End of the period',
            'email': 'Email',
            'target': 'Place of provision',
            'count': 'Count',
        }
    }
btn_name = {
    'en': 'Send a request',
    'ru': 'Отправить заявку',
}
params = {
        '1': ['name', 'last_name', 'father_name', 'email', 'birthday', 'group_name','target', 'count'],
        '2': ['name', 'last_name', 'father_name', 'email', 'birthday', 'date_start','target', 'date_end', 'group_name', 'count']
    }