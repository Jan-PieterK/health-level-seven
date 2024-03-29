from django.http import HttpResponse
from django.shortcuts import render

from hl7 import csv_to_hl7, excel_to_hl7, hl7_to_csv, hl7_to_excel
from src.converter import is_valid_csv_format

from .forms import TextInputForm


def home_view(request):
    return render(request, "home.html")


def _excel_to_hl7(request):
    if request.method == "POST":
        if "excel_file" in request.FILES:
            excel_file = request.FILES["excel_file"]
            if excel_file.name.endswith(".xlsx"):
                try:
                    excel_file_path = excel_file
                    hl7_message = excel_to_hl7(excel_file_path)
                    return render(
                        request,
                        "excel_to_hl7.html",
                        {"hl7_message": hl7_message},
                    )
                except Exception as e:
                    return render(
                        request,
                        "excel_to_hl7.html",
                        {"error_message": f"Error: {e}"},
                    )
            else:
                return render(
                    request,
                    "excel_to_hl7.html",
                    {
                        "error_message": "Invalid file format. Please upload an Excel file."
                    },
                )
        else:
            return render(
                request,
                "excel_to_hl7.html",
                {
                    "error_message": "No file uploaded. Please select an Excel file to upload."
                },
            )
    return render(request, "excel_to_hl7.html")


def _csv_to_hl7(request):
    if request.method == "POST":
        if "csv_file" in request.FILES:
            csv_file = request.FILES["csv_file"]
            if csv_file.name.endswith(".csv"):
                data = csv_file.read().decode("utf-8")
                if not is_valid_csv_format(data):
                    return render(
                        request,
                        "csv_to_hl7.html",
                        {"error_message": "Please upload the required CSV format"},
                    )
                hl7_message = csv_to_hl7(data)
                return render(request, "csv_to_hl7.html", {"hl7_message": hl7_message})
            else:
                return render(
                    request,
                    "csv_to_hl7.html",
                    {"error_message": "Invalid file format. Please upload a CSV file."},
                )
        else:
            return render(
                request,
                "csv_to_hl7.html",
                {
                    "error_message": "No file uploaded. Please select a CSV file to upload."
                },
            )
    return render(request, "csv_to_hl7.html")


def _text_to_hl7(request):
    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data["text_input"]
            try:
                return render(
                    request,
                    "text_to_hl7.html",
                    {"hl7_message": csv_to_hl7(submitted_text)},
                )
            except Exception as e:
                return render(
                    request,
                    "text_to_hl7.html",
                    {"error_message": f"Error: {e}"},
                )
        else:
            return render(
                request,
                "text_to_hl7.html",
                {"error_message": "No text submitted"},
            )
    else:
        form = TextInputForm()

    return render(request, "text_to_hl7.html", {"form": form})


def _hl7_to_csv(request):
    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data["text_input"]
            if "|" not in submitted_text:
                return render(
                    request,
                    "hl7_to_csv.html",
                    {"error_message": "Please upload the required HL7 format"},
                )
            try:
                csv_data = hl7_to_csv(submitted_text)
            except:
                pass

            else:
                context = {
                    "csv_data": csv_data,
                }
                return render(request, "hl7_to_csv.html", context)
        else:
            return render(
                request,
                "hl7_to_csv.html",
                {"error_message": "No HL7 message submitted"},
            )

    form = TextInputForm()
    context = {
        "form": form,
    }
    return render(request, "hl7_to_csv.html", context)


def _hl7_to_excel(request):
    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data["text_input"]
            if "|" not in submitted_text:
                return render(
                    request,
                    "hl7_to_excel.html",
                    {"error_message": "Please upload the required HL7 format"},
                )
            excel_data = hl7_to_excel(submitted_text)
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response[
                "Content-Disposition"
            ] = 'attachment; filename="converted_data.xlsx"'
            response.write(excel_data)
            return response
        else:
            return render(
                request,
                "hl7_to_excel.html",
                {"error_message": "No HL7 message submitted"},
            )

    return render(request, "hl7_to_excel.html", {"form": TextInputForm()})
