from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('client_login/', views.client_login_view, name="client_login_view"),
    path('client_signup/', views.client_signup_view, name="client_signup_view"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('product/', views.product_view, name="product_view"),
    path("admin/", admin.site.urls),

]
