import csv
from io import StringIO
from typing import Dict, List, Tuple
import pandas as pd
from io import BytesIO


def data_to_hl7(hl7_data: Dict[str, List[List[str]]]) -> str:
    message = ''
    for segment_name, segment_data in hl7_data.items():
        segment_value = "|".join(
            ["^".join(
                ["&".join(
                    [l3 or '' for l3 in l2 or []]
                ) for l2 in l1 or []]
            ) for l1 in segment_data]
        )
        message += f'{segment_name}|{segment_value}\n'
    return message


def hl7_index_split(index: str) -> Tuple[int, int, int]:
    index = index.split('.')
    try:
        index_pipes = int(index[0]) - 1
    except IndexError:
        raise ValueError("Error")
    try:
        index_roofs = int(index[1]) - 1
    except IndexError:
        index_roofs = 0
    try:
        index_ands = int(index[2]) - 1
    except IndexError:
        index_ands = 0
    return index_pipes, index_roofs, index_ands


def convert(content: str) -> Dict[str, List[List[str]]]:
    hl7_data = {}
    data = list(csv.reader(StringIO(content), delimiter=';'))
    for segment_name, index, value in data:
        index_l1, _, _ = hl7_index_split(index)
        if segment_name in hl7_data:
            hl7_data[segment_name] = hl7_data[segment_name] + (
                [None] * (index_l1 + 1 - len(hl7_data[segment_name]))
            )
        else:
            hl7_data[segment_name] = [None] * (index_l1 + 1)

    for segment_name, index, value in data:
        index_l1, index_l2, _ = hl7_index_split(index)

        l2_list: List | None = hl7_data[segment_name][index_l1]
        if l2_list is not None:
            hl7_data[segment_name][index_l1] = l2_list + (
                [None] * (index_l2 + 1 - len(l2_list))
            )
        else:
            hl7_data[segment_name][index_l1] = [None] * (index_l2 + 1)

    for segment_name, index, value in data:
        index_l1, index_l2, index_l3 = hl7_index_split(index)
        l3_list: List | None = hl7_data[segment_name][index_l1][index_l2]
        if l3_list is not None:
            hl7_data[segment_name][index_l1][index_l2] = l3_list + (
                [None] * (index_l3 + 1 - len(l3_list))
            )
        else:
            hl7_data[segment_name][index_l1][index_l2] = [None] * (index_l3 + 1)

    for segment_name, index, value in data:
        index_l1, index_l2, index_l3 = hl7_index_split(index)
        hl7_data[segment_name][index_l1][index_l2][index_l3] = value

    return hl7_data


def hl7_to_csv(hl7_message):
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
                                        f'{segment_name};{index}.{sub_index}.{subsub_index};{subsubfield}')
                            else:
                                csv_data.append(
                                    f'{segment_name};{index}.{sub_index};{subfield}')

    return '\n'.join(csv_data)


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
