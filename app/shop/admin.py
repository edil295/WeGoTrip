from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Payment, Product, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'get_product_names',
        'total_sum',
        'status',
        'created_at',
        'confirmation_time',
        'confirm_order_button'
    )
    readonly_fields = (
        'created_at',
        'confirmation_time'
    )
    fields = (
        'total_sum',
        'status',
        'products',
        'created_at',
        'confirmation_time'
    )

    def get_product_names(self, obj):
        return ', '.join([product.name for product in obj.products.all()])

    get_product_names.short_description = 'Продукты'

    def confirm_order_button(self, obj):
        if obj.get_status_display() == "Подтвержден":
            return 'Заказ подтвержден'
        elif obj.payment.status == 2:
            url = reverse('confirm_order', args=[obj.id])
            return format_html('<a class="button" href="{}">Подтвердить заказ</a>', url)
        else:
            return 'В ожидании оплаты'

    confirm_order_button.short_description = 'Подтверждение заказа'

    confirm_order_button.allow_tags = True


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'get_order_id',
        'amount',
        'status',
        'type_of_payment'
    )
    list_editable = ('status', )

    def get_order_id(self, obj):
        return f"Заказ №{obj.order.id}"

    get_order_id.short_description = 'Номер заказа'


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'get_html_image',
    )

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=50>')
        return '---'

    get_html_image.short_description = 'Изображение'


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
