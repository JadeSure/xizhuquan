import pandas as pd
from pandas import DataFrame
from datetime import datetime
from pathlib import Path

pd.set_option('display.max_rows', 3000)

import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

import openpyxl

import os


def load_data(file_name):
    names = ['items', 'unit', 'price']
#     skipDays = datetime.now().day
    
    wb = xlrd.open_workbook(file_name)
    # obtain all the sheet in the workbook
    sheets_name = wb.sheet_names()
    # print(sheets)
    
    # too less info, omit
    if len(sheets_name) <= 5:
        return
 
    # iterator sheets without the total sheet
    df_all = DataFrame()
    for i in range(len(sheets_name)-1):
    # skiprows=2 omit tow
        df = pd.read_excel(file_name, names = names, sheet_name=i, skiprows=2, 
                       skipfooter = 3, usecols= [0,1,3])
        df_all= df_all.append(df)
        
    
    # print(df_all)

    # delete Nan value and reset index
    df_all = df_all.dropna()
    df_all = df_all.reset_index(drop=True)
    
    
    df_all.sort_values(axis=0, ascending=False, inplace=True, kind='quicksort', by=['price'])
    
    # print(df_all)
    
    df_total = pd.read_excel(file_name, 
                             # usecols: use which cols as input
                             # skiprows = 1, jump title and set header to None
                   sheet_name=len(sheets_name)-1,skiprows=1, header = None, names = names, usecols = "A:C")
    # print(df_total)

    # contact active and old database together
    frames = [df_all, df_total]
    results = pd.concat(frames)
    
#     be used for debug
    print(results)
    
    # according to prices, sort value
    results.sort_values(axis=0, ascending=False, inplace=True, 
           kind='quicksort', by=['price'])
    # print(results)
    #based on item and unit to dropout duplicated vlaue
    results.drop_duplicates(['items', 'unit'], keep = 'first', inplace = True)
    
    # reset index
    results = results.reset_index(drop=True)
    
    # print(results)
    
    workbook = openpyxl.load_workbook(file_name)
    
  
#     if len(sheets_name) > skipDays + 2:
#         numPickerList = list(range(len(sheets_name)-12, len(sheets_name)-1))
#         numPickerList.extend([0, 1])
        
    for step, i in enumerate(sheets_name):
        if step == 0 or step == len(sheets_name)-3 or step == 1:
#             if step in numPickerList:
            continue

#         print(i)

        # delete workbook with sheet name
        del workbook[i]

    # print(workbook.get_sheet_names())
    workbook._active_sheet_index = 0
    workbook.save(file_name)

    # save new data into original excel sheet
    with pd.ExcelWriter(file_name, engine="openpyxl", mode = 'a') as writer:
        # write results to that file_name, name this name in: sheet_name
        # without index
        results = results.dropna()
        results.to_excel(writer, sheet_name = sheets_name[len(sheets_name)-1], header = ['品名', '单位', '单价'], index = False)
        writer.save()



if __name__ == '__main__':

    current_folder = Path.cwd()
    static_dir = f"{current_folder}/data/"  

    # Specify the paths for data and output folders
    data_folder = current_folder / 'data'
    output_folder = current_folder / 'output'
    
    # any_unrecorder = True
    # dir = static_dir
    
    # while any_unrecorder:
  
    #     filename_excel = []
    #     folder_name = []
    #     any_unrecorder = False

    #     for root, dirs, files in os.walk(dir):
    #         for file in files:

    #             if not file.endswith('.xlsx'):
    #                 continue
    #             # print(os.path.join(root,file))
    #             filename_excel.append(os.path.join(root,file))

    #     print(filename_excel)

    #     for file in filename_excel:
    #         print("I m processing ", file)
    #         load_data(file)
            
    #     if len(folder_name) != 0:
    #         temp_folder_name = folder_name.pop(0)
    #         dir = static_dir + str(temp_folder_name)
    #         any_unrecorder = True
            
    # print("processing finished")
    # Ensure the output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    any_unrecorder = True
    dir = data_folder

    while any_unrecorder:
        filename_excel = []
        output_file_dict = []

        # List all Excel files in the data folder
        for file_path in dir.glob('*.xlsx'):
            # file_name = str(file_path).split("/")[-1]
            # output_file_dict[str(file_path)] = f"{output_folder}/{file_name}"
            # filename_excel.append(str(file_path))

            filename_excel.append(file_path)

        print(file_path)

        for file_path in filename_excel:
            print("I'm processing", file_path)
            # load_data(file_path, output_file_dict[file_path])
            load_data(file_path)

        any_unrecorder = False  # Assuming you want to process all files once

    print("Processing finished")

