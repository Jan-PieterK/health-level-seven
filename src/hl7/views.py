from django.shortcuts import render, redirect
from .models import CSVData
from .forms import TextInputForm
from src.converter import data_to_hl7, convert, hl7_to_csv


def home_view(request):
    return render(request,
                  "home.html")


def textbox_view(request):
    return render(request,
                  'upload.html')


def upload_csv(request):
    return render(request,
                  'upload-csv.html')


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


def hl7_to_csv_view(request):
    if request.method == 'POST':

        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data['text_input']
            if '|' not in submitted_text:
                return render(request,
                              'hl7_to_csv_page.html',
                              {'error_message': 'Please upload the required HL7 format'})
            try:
                csv_data = hl7_to_csv(submitted_text)  # Transform HL7 to CSV-like format
            except:
                pass

            else:
                context = {
                    'csv_data': csv_data,  # Use the transformed CSV data
                }
                return render(request, 'hl7_to_csv_page.html', context)
        else:
            return render(request,
                          'hl7_to_csv_page.html',
                          {'error_message': 'No HL7 message submitted'})

    form = TextInputForm()
    context = {
        'form': form,
    }
    return render(request, 'hl7_to_csv_page.html', context)
