"""the_taz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts import views as accounts_views
from taz.views import get_index, get_menu,get_reservation,get_voucher,get_contact,get_opening,get_location
from products import urls as products_urls
from payment import urls as payment_urls


urlpatterns = [
    url(r'^', include("blog.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_index, name='index'),
    url(r'menu/', get_menu, name='menu'),
    url(r'reservation/',accounts_views.get_reservation, name='reservation'),
    url(r'voucher/', get_voucher, name='voucher'),
    url(r'contact/', accounts_views.get_contact, name='contact'),
    url(r'opening/', get_opening, name='opening'),
    url(r'location/', get_location, name='location'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^cancel_subscription/$', accounts_views.cancel_subscription, name='cancel_subscription'),
    url(r'^products/', include(products_urls)),
    url(r'^payments/', include(payment_urls)),
    url(r'^thanks/', accounts_views.thanks, name='thanks'),
    url(r'^booking/', accounts_views.booking, name='booking'),

]
