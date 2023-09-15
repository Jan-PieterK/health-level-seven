import pandas as pd
from io import BytesIO
import openpyxl
from hl7 import csv_to_hl7


def excel_to_hl7(file_path: str) -> str:
    wb = openpyxl.load_workbook(file_path)
    rows = list(wb.active.iter_rows(values_only=True))
    return csv_to_hl7(
        "\n".join(";".join(str(cell) for cell in row) for row in rows)
    )


def hl7_to_excel(hl7_message):
    csv_data = []
    segments = hl7_message.split('\n')

    for segment in segments:
        if segment:
            fields = segment.split('|')
            segment_name = fields[0]
            for index, field in enumerate(fields[1:], start=1):
                if field:
                    subfields = field.split('^')
                    for sub_index, subfield in enumerate(subfields, start=1):
                        if subfield:
                            if '&&' in subfield:
                                subsubfields = subfield.split('&&')
                                for subsub_index, subsubfield in enumerate(subsubfields, start=1):
                                    csv_data.append(
                                        [segment_name, f'{index}.{sub_index}.{subsub_index}', subsubfield])
                            else:
                                csv_data.append(
                                    [segment_name, f'{index}.{sub_index}', subfield])

    df = pd.DataFrame(csv_data, columns=['Segment',
                                         'Index',
                                         'Value'])
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer,
                                  engine='xlsxwriter')
    df.to_excel(excel_writer,
                index=False)
    excel_writer.close()
    excel_buffer.seek(0)
    excel_data = excel_buffer.read()
    return excel_data
