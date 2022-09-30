import json

import requests
from django.conf import settings

from advertisement.utils import Redis
from config.celery import app


@app.task
def check_payment(ads_subsriber_pk):
    url = 'https://api.paybox.money/get_status2.php'

    redis = Redis()
    conn = redis.conn
    data = conn.get(f'payment-{ads_subsriber_pk}')

    if not data:
        print('Error')

    decode_data = data.decode('utf-8')
    data = json.loads(decode_data)
    data['pg_salt'] = settings.PAYBOX_SALT
    print(data)
    response = requests.post(url, data=data)
    print(response.status_code)
    print(response.text)
    print(response.ok)
    print(response.request)
    print(dir(response))
