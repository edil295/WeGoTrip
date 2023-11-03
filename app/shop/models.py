from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

STATUS = (
    (1, 'Оформлен'),
    (2, 'Подтвержден'),
    (3, 'Отменен')
)

PAYMENT_STATUS = (
    (1, 'В обработке'),
    (2, 'Оплачен'),
    (3, 'Не оплачен')
)

TYPE_OF_PAYMENT = (
    (1, 'Наличные'),
    (2, 'Безналичные')
)


class Product(models.Model):
    """
    Модель описывающая продукт/товар.

    Поля:
    - name (CharField): Название продукта.
    - text (TextField): Описание или контент, описывающий продукт. Может быть пустым.
    - price (PositiveIntegerField): Стоимость продукта, представленная в целых числах.
    - image (ImageField): Изображение продукта. Может быть пустым.

    Примечания:
    - Поле "name" используется для задания названия продукта, не должно превышать 255 символов.
    - Поле "text" предоставляет возможность добавления описания или контента для продукта, и оно может быть пустым.
    - Поле "price" представляет стоимость продукта в целых числах.
    - Поле "image" позволяет загрузить изображение продукта и может быть пустым.

    """
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Описание/Контент',
        null=True, blank=True
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость'
    )
    image = models.ImageField(
        upload_to='products_images',
        verbose_name='Изображение',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Список товаров'

    def __str__(self):
        return f"{self.name} -{self.price}"


class Order(models.Model):
    """
    Модель описывающая заказ товара(списка товаров).

    Поля:
    - products (ManyToManyField): Список продуктов, которые нужно заказать.
    - total_sum (PositiveIntegerField): Итоговая сумма заказа.
    - status (PositiveSmallIntegerField): Статус заказа.
    - created_at (DateTimeField): Дата создания заказа.
    - confirmation_time (DateTimeField): Время подтверждения заказа.

    Примечания:
    - Поле "products" используется для задания списка продуктов, которые нужно заказать.
    - Поле "total_sum" представляет стоимость заказа в целых числах.
    - Поле "status" представляет статус заказа.
    - Поле "created_at" представляет дату создания заказа.
    - Поле "confirmation_time" представляет время подтверждения заказа.

    """
    products = models.ManyToManyField(
        Product,
        verbose_name='Продукты',
        related_name='orders'
    )
    total_sum = models.PositiveIntegerField(
        verbose_name='Итоговая сумма'
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=1,
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    confirmation_time = models.DateTimeField(
        verbose_name='Время подтверждения',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'

    def get_status_display(self):
        return dict(STATUS).get(self.status, '')

    def __str__(self):
        return f"{self.total_sum} -{self.get_status_display()}"


class Payment(models.Model):
    """
    Модель описывающая оплату заказа.

    Поля:
    - order (ForeignKey): Заказ, который нужно оплатить.
    - amount (PositiveIntegerField): Сумма оплаты.
    - type_of_payment (CharField): Тип оплаты.

    Примечания:
    - Поле "order" используется для указания заказа, который нужно оплатить.
    - Поле "amount" представляет сумму оплаты в целых числах.
    - Поле "type_of_payment" представляет тип оплаты.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты'
    )
    status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS,
        verbose_name='Статус',
        default=1
    )
    type_of_payment = models.PositiveSmallIntegerField(
        choices=TYPE_OF_PAYMENT,
        verbose_name='Тип оплаты',
        default=1
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Список платежей'

    def get_status_display(self):
        return dict(STATUS).get(self.status, '')

    def __str__(self):
        return f"Заказ №: {self.order.id} Сумма: {self.amount} Тип оплаты: {self.type_of_payment}"
