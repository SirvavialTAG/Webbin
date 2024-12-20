"""
URL configuration for webbin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
#from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'brands', views.BrandViewSet)

urlpatterns = [
    # HTML
    path('', views.main, name='main'),
    path('japan/', views.cars_catalog, name='japan'),








    #path('korea/', , name='korea'),

    # API
    #path('', include(router.urls)),
    #path('cars/', views.CarsCatalog.as_view(), name='cars'),
    #path('brands/<int:brand__id>/models/', views.CarsModel.as_view(), name='car_models')
]
