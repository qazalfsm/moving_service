from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('register_mover/', views.register_mover, name='register_mover'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_order/', views.create_order, name='create_order'),
    path('mover_dashboard/', views.mover_dashboard, name='mover_dashboard'),
    path('nearest_movers/<int:order_id>/', views.nearest_movers, name='nearest_movers'),  # اضافه کردن URL نمایش نزدیک‌ترین موورها
]
