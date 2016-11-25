from django.conf.urls import url
from .views import make_payment

urlpatterns = [
    url(r'^stripe', make_payment, name='make_payment_stripe'),
]