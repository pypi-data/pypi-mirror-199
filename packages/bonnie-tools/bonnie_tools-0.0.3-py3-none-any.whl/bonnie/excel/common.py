# coding: utf-8

import openpyxl


def select_sheet(workbook: openpyxl.Workbook):
    sheet_names = workbook.sheetnames

    # 输出工作表的名称
    for idx, sheet_name in enumerate(sheet_names):
        print(f'{idx + 1}. {sheet_name}')

    sheet_index = input('Please select worksheet: ')
    return int(sheet_index) - 1
