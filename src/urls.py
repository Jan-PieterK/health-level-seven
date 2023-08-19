from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('hl7/',include('src.hl7.urls')),
    path('admin/', admin.site.urls),
]
