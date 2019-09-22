from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order
import xhtml2pdf.pisa as pisa

def PaymentNotification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()
        
        # Email sending
        subject = 'Online-shop - Order: {}'.format(order.id)
        message = 'A PDF file with information about your order is attached to the email message.'
        email = EmailMessage(subject, message, 'admin@mayshop.com', [order.email])

        # PDF generation
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        response = HttpResponse(content_type='application/pdf')
        pdf = pisa.pisaDocument( out, response)

        # Attach PDF
        email.attach('order_{}'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()

        
valid_ipn_received.connect(PaymentNotification)