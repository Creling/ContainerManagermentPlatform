from django.urls import path
from . import views

urlpatterns = [
    path('nation', views.NationView.as_view()),
    path('city', views.CityView.as_view()),
    path('datacenter', views.DatacenterView.as_view()),
    path('provider', views.ProviderView.as_view()),
    path('container', views.Container.as_view()),
    path('service', views.Service.as_view()),
    path('servicecontainer', views.ContainerService.as_view())
]