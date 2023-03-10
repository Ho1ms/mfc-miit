from json import dumps
from .modules.form_config import *
from flask import Blueprint, request
from .modules.database import create_connect
from .modules.access_handler import access_handler

dashboard_router = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def get_avg_cnt(cnt):
    avg_active = cnt['active'] + cnt['ready'] + cnt['closed']
    avg_ready = cnt['ready'] + cnt['closed']
    avg_closed = cnt['closed']

    return avg_active or 1, avg_ready or 1, avg_closed or 1


@dashboard_router.get('/', endpoint='dashboard_handle')
@access_handler((1, 2, 3))
def dashboard_handle(user):
    db, sql = create_connect()
    data = request.args

    date = datetime.datetime.now()
    start = data.get('start') or (date - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    stop = data.get('stop') or date.strftime('%Y-%m-%d')

    sql.execute("""with dates as (
    SELECT i , COUNT(b.timestamp_registration) cnt_bot_uses
    FROM generate_series(date %s, %s, '1 day'::interval) i
        LEFT JOIN bot_users b ON i = CAST(b.timestamp_registration as date)
    GROUP BY i
    )
SELECT to_char(i, 'DD.MM') date, cnt_bot_uses, cnt_certifications, COUNT(t.create_at) cnt_certificates_of_payment
FROM
         (SELECT i , dates.cnt_bot_uses, COUNT(f.create_at) cnt_certifications
          FROM dates
                   LEFT JOIN certificates f ON CAST(f.create_at as date) = i
          GROUP BY i, dates.cnt_bot_uses
          ORDER BY i) d
             LEFT JOIN certificates_of_payment t
         ON CAST(t.create_at as date) = i

GROUP BY i, d.cnt_bot_uses, cnt_certifications
ORDER BY i""", (start, stop))
    rows_by_dates = sql.fetchall()

    sql.execute("""SELECT status,
       create_at,
       date_active,
       date_ready,
       date_closed,
       0 as type
FROM certificates
UNION ALL
SELECT status,
       create_at,
       date_active,
       date_ready,
       date_closed,
       1 as type
FROM certificates_of_payment""")
    rows = sql.fetchall()
    db.close()

    response = {
        'labels': (titles['ru']['1'], titles['ru']['2']),
        'colors': ('#FF0000', '#FF7400'),
        'rows': [{
            'total': 0,
            'new': 0,
            'active': 0,
            'ready': 0,
            'closed': 0,
            'avg_active': datetime.timedelta(),
            'avg_ready': datetime.timedelta(),
            'avg_closed': datetime.timedelta(),
            'avg_total': datetime.timedelta()
        },
        {
            'total': 0,
            'new': 0,
            'active': 0,
            'ready': 0,
            'closed': 0,
            'avg_active': datetime.timedelta(),
            'avg_ready': datetime.timedelta(),
            'avg_closed': datetime.timedelta(),
            'avg_total': datetime.timedelta()
        }],
        'dates':{
            'cnt_bot_uses':{
                'label':'Новые пользователи',
                'data': [],
                'borderColor': '#FF6384FF',
                'backgroundColor': '#FF63847F',
            },
            'date':{
                'data':[]
            },
            'cnt_certifications':{
                'label':'Справки об учёбе',
                'data': [],
                'borderColor': '#35A2EBFF',
                'backgroundColor': '#35A2EB7F',
            },
            'cnt_certificates_of_payment':{
                'label':'Справки о стипендии',
                'data': [],
                'borderColor': '#ff8f0f',
                'backgroundColor': '#f29429',
            },
        },
    }

    for row in rows_by_dates:
        print(row)
        for i in ('date','cnt_bot_uses','cnt_certifications','cnt_certificates_of_payment'):
            response['dates'][i]['data'].append(row[i])

    statuses = ('new', 'active', 'ready', 'closed')
    for row in rows:
        response['rows'][row['type']]['total'] += 1
        response['rows'][row['type']][row['status']] += 1

        if statuses.index(row['status']) >= 1:
            response['rows'][row['type']]['avg_active'] += (row['date_active'] - row['create_at'])
        if statuses.index(row['status']) >= 2:
            response['rows'][row['type']]['avg_ready'] += (row['date_ready'] - row['date_active'])
        if statuses.index(row['status']) >= 3:
            response['rows'][row['type']]['avg_closed'] += (row['date_closed'] - row['date_ready'])
            response['rows'][row['type']]['avg_total'] += (row['date_closed'] - row['create_at'])

    for i in range(2):
        avg_active, avg_ready, avg_closed = get_avg_cnt(response['rows'][i])

        response['rows'][i]['avg_active'] /= avg_active
        response['rows'][i]['avg_ready'] /= avg_ready
        response['rows'][i]['avg_closed'] /= avg_closed
        response['rows'][i]['avg_total'] /= avg_closed

    return dumps(response, ensure_ascii=False, default=str), 200
