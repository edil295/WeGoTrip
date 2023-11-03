from django.utils import timezone

from celery import shared_task
from .models import Order

import requests


@shared_task
def confirm_order_task(order_id):
    order = Order.objects.get(id=order_id)
    order.status = 2
    order.confirmation_time = timezone.now()
    order.save()
    order_id = order.id
    amount = order.total_sum
    time = order.confirmation_time
    url = 'https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4'
    data = {'id': order_id, 'amount': amount, 'date': time}
    requests.post(url=url, data=data)
