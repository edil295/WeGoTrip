from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .models import Order, Payment, Product
from .serializers import OrderSerializer, PaymentSerializer, ProductSerializer
from .tasks import confirm_order_task

import time


class ProductListView(generics.ListAPIView):
    """
    Эндпоинт получения списка Товаров:
    GET-запрос с выдачей списка Товаров.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(generics.CreateAPIView):
    """
    Эндпоинт создания нового Заказа:
    POST-запрос с указанием списка Товаров.
    Итоговая сумма Заказа складывается из стоимостей всех Товаров.
    Во Время создания записыватся текущий таймстамп.

    param:
     products - список id товаров
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        product_ids = self.request.data.get('products', [])
        products = Product.objects.filter(pk__in=product_ids)
        total_sum = sum(product.price for product in products)
        serializer.save(total_sum=total_sum)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentCreateView(generics.CreateAPIView):
    """
    Эндпоинт создания нового Платежа:
    POST-запрос с указанием Заказа.
    Сумма берется из итоговой суммы Заказа

    param:
     order - id заказа
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        order_id = self.request.data.get('order')
        order = Order.objects.get(pk=order_id)
        amount = order.total_sum
        serializer.save(amount=amount)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ConfirmOrderView(APIView):
    """
    Эндпоинт по подтверждению заказа:

    Которая запускается после подтверждения заказа в админ панели,
    отправляет задачу по изменению статуса заказа и инициирования время подтверждения
    в celery.

    Celery-task: confirm_order_task
    выполняет также отправку POST запроса после изменений в заказа
    на адресс https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4
    с телом {"id": "order_id", "amount": Сумма заказа, "date": Время подтверждения}
    """
    def get(self, request, pk):
        previous_page = request.META.get('HTTP_REFERER')
        confirm_order_task.delay(pk)
        time.sleep(1)
        return HttpResponseRedirect(previous_page)
