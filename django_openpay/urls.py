from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^save/$', views.cardSave,
        name='django_openpay_cardsave'),
    url(r'^webhook/$', views.webhook,
        name='django_openpay_webhook'),
]
