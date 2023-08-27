from django.urls import path
from .views import home_view, upload_csv, text_input, hl7_to_csv, hl7_to_excel, upload_excel
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("home/", home_view, name='home'),
    path('excel-to-hl7/', upload_excel, name='excel-to-hl7'),
    path('csv-to-hl7/', upload_csv, name='csv-to-hl7'),
    path('text-to-hl7/', text_input, name='text-to-hl7'),
    path('hl7-to-csv/', hl7_to_csv, name='hl7-to-csv'),
    path('hl7-to-excel/', hl7_to_excel, name='hl7-to-excel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)