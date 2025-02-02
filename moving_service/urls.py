from django.contrib import admin
from django.urls import path, include
from users import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
