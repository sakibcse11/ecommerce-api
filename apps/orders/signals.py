from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, OrderItem
from .tasks import send_order_status_update_email, notify_vendor_about_new_order


@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    print('signal 1')

    if not created and instance.status in ['processing', 'shipped', 'delivered', 'cancelled']:
        print('order status change')

        send_order_status_update_email.delay(
            order_id=instance.id,
            status=instance.get_status_display(),
            customer_email=instance.customer.email
        )


@receiver(post_save, sender=Order)
def notify_vendors_new_order(sender, instance, created, **kwargs):
    if created:
        #send notifications only when order is completely placed
        transaction.on_commit(lambda: send_vendor_notifications(instance.id))

def send_vendor_notifications(order_id):
    instance = Order.objects.get(id=order_id)

    vendors = instance.get_vendors()

    for vendor in vendors:
        vendor_items = OrderItem.objects.filter(
            order=instance,
            product__vendor=vendor
        ).select_related('product')

        vendor_subtotal = sum(item.subtotal for item in vendor_items)

        items_data = [
            {
                'quantity': item.quantity,
                'product_name': item.product.name,
                'price': str(item.price)
            }
            for item in vendor_items
        ]

        notify_vendor_about_new_order.delay(
            order_id=instance.id,
            vendor_email=vendor.user.email,
            vendor_items=items_data,
            vendor_subtotal=str(vendor_subtotal),
            customer_email=instance.customer.email
        )