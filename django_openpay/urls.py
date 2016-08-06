from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cards/save/$', views.cardSave,
        name='django_openpay_cardsave'),
    url(r'^charges/save/$', views.chargeSave,
        name='django_openpay_chargesave'),
]
