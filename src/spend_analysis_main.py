"""
@author: Akul
"""

from src.utils.sheet_utils import get_category
from src.utils.excel_utils import convert_xls_to_dataframe
from src.utils.config_utils import read_category_config
category_dict = read_category_config()

#this is the delimiter which sandwiches a generic balancesheet
sheet_delimiter = "----------------------"
raw_root_path = "..\\input_files"

spend_df = convert_xls_to_dataframe(raw_root_path, sheet_delimiter=sheet_delimiter)
spend_df.reset_index(inplace=True,drop = True)
spend_df['category']=spend_df['PARTICULARS'].apply(lambda x : get_category(x,category_map=category_dict))
spend_df.to_excel("..\\reports\\spend.xlsx")