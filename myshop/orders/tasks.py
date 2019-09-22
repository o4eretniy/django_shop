from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def OrderCreated(order_id):
    # Sending a purchase creation email
    order = Order.objects.get(id=order_id)
    subject = 'Order number {}'.format(order.id)
    message = 'Dear, {}, Dear, you have successfully done an order.\
               Your order number {}'.format(order.first_name, order.id)
    mail_send = send_mail(subject, message, 'admin@myshop.ua', [order.email])
    return mail_send