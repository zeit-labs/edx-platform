"""Learner dashboard URL routing configuration"""

from django.urls import path, re_path

from . import views

urlpatterns = [
    # Used the eCommerce deprecated URL for backward compatibility
    path('basket/add', views.start_order, name='payments_start_order'),
    path('payment/webhook', views.webhook, name='payments_webhook'),
    path('payment/callback', views.callback, name='payments_callback'),
    path('payment/invoice', views.invoice, name='payments_invoice'),
    path(r'payment/pay/<slug:provider>', views.payment_form, name='payments_form_payfort'),
]
