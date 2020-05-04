from django.urls import path, include
from . import views

urlpatterns = [
    path('hamburguesa', views.Hamburguesa_list),
    path('hamburguesa/<numero>', views.Hamburguesa_detail),
    path('ingrediente', views.Ingrediente_list),
    path('ingrediente/<numero>', views.Ingrediente_detail),
    path('hamburguesa/<int:pk>/ingrediente/<int:pk2>', views.modify_hamburguesa_ingrediente),
]