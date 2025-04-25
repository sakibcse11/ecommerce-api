from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_order_status_update_email(order_id, status, customer_email):
    subject = f'Order #{order_id} Status Update'
    message = f'Your order #{order_id} has been updated to: {status}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email]

    send_mail(subject, message, from_email, recipient_list)

    return f"Order status update email sent to {customer_email}"


@shared_task
def notify_vendor_about_new_order(order_id, vendor_email, vendor_items, vendor_subtotal, customer_email):
    subject = f'New Order #{order_id} Received'
    message = f"""
    You have received a new order #{order_id}
    Customer: {customer_email}
    Order total for your products: ${vendor_subtotal}
    Products:
    """

    for item in vendor_items:
        message += f"\n- {item['quantity']} x {item['product_name']} (${item['price']} each)"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [vendor_email]

    send_mail(subject, message, from_email, recipient_list)

    return f"New order notification email sent to vendor {vendor_email}"