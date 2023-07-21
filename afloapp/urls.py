from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),

    path('formations/', formations, name="formations"),
    path('formations/create/', create_formation, name="create-formation"),
    path('formations/<int:pk>/', formation, name="formation"),
    path('formations/update/<int:pk>/', update_formation, name="update-formation"),
    path('formations/delete/<int:pk>/', delete_formation, name="delete-formation"),

    path('formateurs/', formateurs, name="formateurs"),
    path('formateurs/create/', create_formateur, name="create-formateur"),
    path('formateurs/<int:pk>/', formateur, name="formateur"),
    path('formateurs/update/<int:pk>/', update_formateur, name="update-formateur"),
    path('formateurs/delete/<int:pk>/', delete_formateur, name="delete-formateur"),
    path('formateurs/remove-responsability/<int:pk>/', remove_responsability, name="remove-responsability"),
    
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),

    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    # path('about/<str:name>/', about, name="about"),
    # path('contact/<str:email>/<int:age>/', contact, name="contact"),
]