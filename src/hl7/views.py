from django.shortcuts import render, redirect
from .models import CSVData
from .forms import TextInputForm
from src.converter import data_to_hl7, convert


def home_view(request):
    return render(request, "home.html")


def textbox_view(request):
    return render(request, 'upload.html')


def upload_excel(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            if csv_file.name.endswith('.csv'):
                data = csv_file.read().decode('utf-8')
                hl7_message = data_to_hl7(hl7_data=convert(data))
                return render(request,
                              'upload-excel.html',
                              {'hl7_message': hl7_message})
            else:
                return render(request,
                              'upload-excel.html',
                              {'error_message': 'Invalid file format. Please upload a Excel file.'})
        else:
            return render(request,
                          'upload-excel.html',
                          {'error_message': 'No file uploaded. Please select a Excel file to upload.'})
    return render(request,
                  'upload-excel.html')


def text_input_view(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data['text_input']
            try:
                hl7_message = data_to_hl7(hl7_data=convert(submitted_text))
            except:
                return render(request,
                              'text_input_page.html',
                              {'error_message': 'Please enter text in the required csv format'})
            return render(request,
                          'text_input_page.html',
                          {'hl7_message': hl7_message})
        else:
            return render(request,
                          'text_input_page.html',
                          {'error_message': 'No text submitted'})
    else:
        form = TextInputForm()

    return render(request,
                  'text_input_page.html',
                  {'form': form})


