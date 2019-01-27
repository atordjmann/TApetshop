from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('petshop/', include('petshop.urls')),
    path('admin/', admin.site.urls),
]