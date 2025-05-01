import pandas as pd
import os

def slice_xls(file_path, sheet_delimiter):
    xlsObject = pd.ExcelFile(r"{file_path}".format(file_path=file_path))
    sheet0_df = xlsObject.parse(0)
    index_list = list(sheet0_df[sheet0_df[sheet_delimiter]=='\t'].index)
    slice_start = index_list[0]+1
    slice_end = index_list[1]
    sliced_df = sheet0_df.iloc[slice_start:slice_end]
    sliced_df.columns = sliced_df.iloc[0]
    sliced_df = sliced_df[1:]
    return sliced_df


def convert_xls_to_dataframe(raw_root_path, sheet_delimiter):
    df_list = []
    for xls_file in os.listdir(raw_root_path):
        file_path = raw_root_path + "\\" + xls_file
        raw_df = slice_xls(file_path, sheet_delimiter)
        df_list.append(raw_df)

    xls_df = pd.concat(df_list)
    return xls_df