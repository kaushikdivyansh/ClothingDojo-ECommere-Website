from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.products),
    url(r'admin$', views.admin),
    url(r'checkout$', views.checkout),
    url(r'cart/(?P<num>\d+)$', views.cart),
    url(r'update/(?P<num>\d+)$', views.update),
    url(r'remove/(?P<num>\d+)$', views.remove),
    url(r'purchase$', views.purchase),
    url(r'free$', views.free),
    url(r'cancel/(?P<num>\d+)$', views.cancel),
    url(r'locking$', views.lock),
    url(r'unlock$', views.unlock),
    url(r'viewproduct$', views.viewproduct),
    url(r'update_product/(?P<num>\d+)$', views.update_product),
    url(r'add_product$', views.add_product),
    url(r'remove_product/(?P<num>\d+)$', views.remove_product),
    url(r'faq$', views.faq),
    url(r'tos$', views.tos)
]
