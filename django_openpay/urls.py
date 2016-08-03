from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cards/save/$', views.card_save, name='django_openpay_cardsave'),
]
