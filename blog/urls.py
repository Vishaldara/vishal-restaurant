from django.conf.urls import url
import views
from django.views.static import serve
from the_taz.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^blog/$', views.post_list),
    url(r'^blog/(?P<id>\d+)/$', views.post_detail),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]