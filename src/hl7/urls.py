from django.urls import path
from . import views
from .views import text_input_view
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("home/", home_view, name='home'),
    path('upload-excel/', views.upload_excel, name='upload-excel'),
    path('text-input/', text_input_view, name='text_input_view'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)