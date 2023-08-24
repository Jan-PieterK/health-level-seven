from django.urls import path
from . import views
from .views import text_input_view
from .views import home_view
from .views import upload_csv
from .views import hl7_to_csv_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("home/", home_view, name='home'),
    path('upload-excel/', views.upload_excel, name='upload-excel'),
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('text-input/', text_input_view, name='text_input_view'),
    path('hl7_to_csv/', hl7_to_csv_view, name='hl7_to_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)