try:
    import pandas as pd
    import openpyxl
    import math
    from openpyxl.styles import PatternFill, Border, Side, Alignment, Font, fills
    import glob
    import os

    from datetime import datetime
    start_time = datetime.now()

    def octant_analysis(mod=5000):

        try:
                # path = 'G:\CS384\2001EE19_2022\tut07\output'
                # Check whether the specified
                # path exists or not
            isExist = os.path.isdir(r'G:\CS384\2001EE19_2022\tut07\output')

            if (not (isExist)):#make output dir if it doesnt exist
                os.mkdir(r'G:\CS384\2001EE19_2022\tut07\output')

            os.chdir(r'G:\CS384\2001EE19_2022\tut07\input')
            lst_files = glob.glob('*.xlsx')
            sat = 0
            for file in lst_files:  # iterating thorugh files in input folder

                # again we changing the dir to input from output
                os.chdir(r'G:\CS384\2001EE19_2022\tut07\input')
                df1 = pd.read_excel(file)  # reading the input file
                avg_u = df1['U'].mean()  # Calculating average of U,V,W
                avg_v = df1['V'].mean()
                avg_w = df1['W'].mean()

                df1["U_Avg"] = ''  # Creating average for coloumns U,V,W
                df1["V_Avg"] = ''
                df1["W_Avg"] = ''
                # assigning the values to respectivley Coloumn
                df1.iloc[0, 4] = round(avg_u, 3)
                df1.iloc[0, 5] = round(avg_v, 3)
                df1.iloc[0, 6] = round(avg_w, 3)

                # Creating new coloumns with Header U',V',W'
                df1["U'=U - U avg"] = round(df1["U"]-avg_u, 3)
                df1["V'=V - V avg"] = round(df1["V"]-avg_v, 3)
                df1["W'=W - W avg"] = round(df1["W"]-avg_w, 3)

                # df1.to_csv('octant_output.csv')

                #######          Data PreProcessing     ###########

                df1["Octant"] = ''  # Creatig a empty Column with Header as Octant

                l = len(df1)  # length of DataFrame = 29745

                # creating octant column ,and Identifying the octant value for each triple(U_1,V_1,W_1)
                for i in range(0, l):

                    if (df1.loc[i, "U'=U - U avg"] >= 0 and df1.loc[i, "V'=V - V avg"] >= 0 and df1.loc[i, "W'=W - W avg"] >= 0):
                        df1.loc[i, "Octant"] = "+1"  # for +1

                    if (df1.loc[i, "U'=U - U avg"] >= 0 and df1.loc[i, "V'=V - V avg"] >= 0 and df1.loc[i, "W'=W - W avg"] < 0):
                        df1.loc[i, "Octant"] = "-1"  # for -1

                    if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] >= 0 and df1.loc[i, "W'=W - W avg"] >= 0):
                        df1.loc[i, "Octant"] = "+2"  # for +2

                    if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] >= 0 and df1.loc[i, "W'=W - W avg"] < 0):
                        df1.loc[i, "Octant"] = "-2"  # for -2

                    if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] >= 0):
                        df1.loc[i, "Octant"] = "+3"  # for +3

                    if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
                        df1.loc[i, "Octant"] = "-3"  # for -3

                    if (df1.loc[i, "U'=U - U avg"] >= 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] >= 0):
                        df1.loc[i, "Octant"] = "+4"  # for +4

                    if (df1.loc[i, "U'=U - U avg"] >= 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
                        df1.loc[i, "Octant"] = "-4"  # for -4

                        ######  Octant Identification  ########

                # creating empty Column without header and assigned "User input" to row 3
                df1[""] = "  "
                df1[" "] = " "
                df1.iloc[0, 12] = "Mod "+str(mod)

                # creating a Coloumn with header as Octant ID
                df1["Octant ID"] = " "
                df1.loc[0, "Octant ID"] = "Overall Octant"

                # oct_count stores a count of unique elements i.e. count of +1,-1,+2,-2,+3,-4,+4
                oct_count = df1['Octant'].value_counts()

                arr = ["+1", "-1", "+2", "-2", "+3", "-3",
                    "+4", "-4"]  # cretaed for reference

                oct_cnt = {}  # for storing octant count as key and and coreesponding octant value as value in dict
                for i in range(8):
                    s = arr[i]
                    # appending the overall count of octant and octant value in dict i.e for Ex:("+1",2610)
                    oct_cnt.update({s: oct_count[s]})
                    # And assigning a count values to respectively Coloumns
                    df1.loc[0, s] = oct_count[s]

                # print(oct_cnt) #{2610: '+1', 4603: '-1', 4855: '+2', 2798: '-2', 4548: '+3', 2784: '-3', 2769: '+4', 4778: '-4'}
                # sorting the dict by keys
                # print(sortedbykey) {2610: '+1', 2769: '+4', 2784: '-3', 2798: '-2', 4548: '+3', 4603: '-1', 4778: '-4', 4855: '+2'}
                # storing the sorted values in a list
                # print(sortedbyval_lst)['+1', '+4', '-3', '-2', '+3', '-1', '-4', '+2']

                # sorting the dict by values
                sortedbyval = {k: v for k, v in sorted(
                    oct_cnt.items(), key=lambda item: item[1])}
                # storing the sorted keys in a list
                sortedbyval_lst = list(sortedbyval.keys())

                octant_name_id_mapping = {"1": "Internal outward interaction", "-1": "External outward interaction", "2": "External Ejection",
                                        "-2": "Internal Ejection", "3": "External inward interaction", "-3": "Internal inward interaction", "4": "Internal sweep", "-4": "External sweep"}

                df1["Rank 1"] = ''  # created empty columns
                df1["Rank 2"] = ''
                df1["Rank 3"] = ''
                df1["Rank 4"] = ''
                df1["Rank 5"] = ''
                df1["Rank 6"] = ''
                df1["Rank 7"] = ''
                df1["Rank 8"] = ''
                df1["Rank1 Octant ID"] = " "

                dic_rank = {"+1": "Rank 1", "-1": "Rank 2", "+2": "Rank 3", "-2": "Rank 4",
                            "+3": "Rank 5", "-3": "Rank 6", "+4": "Rank 7", "-4": "Rank 8"}  # for reference

                # i=0
                for i in range(8):
                    df1.loc[0, dic_rank[sortedbyval_lst[i]]] = 8 - \
                        i  # appending the octant ranks of octants
                    if (8-i == 1):
                        # appending the highest rank octant and its corresponding octant name
                        df1.loc[0, "Rank1 Octant ID"] = sortedbyval_lst[i]
                        df1.loc[0, "Rank1 Octant Name"] = octant_name_id_mapping[str(
                            int(df1.loc[0, "Rank1 Octant ID"]))]

                        ###########   Added Some Columns And Rows for MOD Count   ##########

                x = 0  # for findind octant values for MOD ranges
                t = 1  # for row pointer

                count_rank_mod = [0]*8  # Count of rank mod values
                while (x < l):

                    d1 = {"+1": 0, "-1": 1, "+2": 2, "-2": 3, "+3": 4,
                        "-3": 5, "+4": 6, "-4": 7}  # creating a dictionary for reference

                    # count values of each octant is stored for MOD ranges
                    oct_cnt_mod = [0]*8

                    oct_cnt = {}  # for storing octant count as key and and coreesponding octant value as value in dict
                    for i in range(x, x+mod, 1):

                        if (i >= l):
                            break  # bound check
                        s3 = df1.at[i, "Octant"]
                        # incrementing by one of count values of corresponding octants
                        oct_cnt_mod[d1[s3]] += 1

                    i = 0
                    for i in range(8):
                        s = arr[i]
                        # assigning overall count of octants in each interval
                        df1.loc[t, s] = oct_cnt_mod[i]
                        # appending the overall count of octant and octant value in dict
                        oct_cnt.update({s: oct_cnt_mod[i]})

                    # sorting the dict by values
                    sortedbyval = {k: v for k, v in sorted(
                        oct_cnt.items(), key=lambda item: item[1])}
                    # storing the sorted keys in a list
                    sortedbyval_lst = list(sortedbyval.keys())

                    i = 0
                    for i in range(8):
                        df1.loc[t, dic_rank[sortedbyval_lst[i]]] = 8 - \
                            i  # appending the octant ranks of octants
                        if (8-i == 1):
                            # appending the highest rank octant and its corresponding octant name
                            df1.loc[t, "Rank1 Octant ID"] = sortedbyval_lst[i]
                            df1.loc[t, "Rank1 Octant Name"] = octant_name_id_mapping[str(
                                int(df1.loc[t, "Rank1 Octant ID"]))]
                            # incrementing by one of corresponding octant
                            count_rank_mod[d1[sortedbyval_lst[i]]] += 1

                    if ((x+mod) > l):  # Writing MOD ranges in Octant ID Coloumn
                        df1.loc[t, "Octant ID"] = str(
                            x)+"-"+str(l-1)  # for last index(i.e) 2744
                    else:
                        df1.loc[t, "Octant ID"] = str(x)+"-"+str(x+mod-1)

                    x += mod
                    t += 1

                #count of Rank1 of mod values
                t += 3
                df1.loc[t, "+1"] = "Octant ID"
                df1.loc[t, "-1"] = "Octant Name"
                df1.loc[t, "+2"] = "Count of Rank1 of Mod Values"
                t += 1
                i = 0
                for ID, name in octant_name_id_mapping.items():  # iterating through a dict
                    # appending the Octant IDs, Octant Name ,and count of Rank1 of mod values
                    df1.loc[t, "+1"] = int(ID)
                    df1.loc[t, "-1"] = name
                    df1.loc[t, "+2"] = count_rank_mod[i]
                    t += 1
                    i += 1

                                  ############### tut 5 ###############
                 

                # taking 1st name of input file for naming of output
                inp = lst_files[sat].replace(
                    '.xlsx', " cm_vel_octant_analysis_mod_"+str(mod)+".xlsx")
                # changing direc to ouput file to save output files
                os.chdir(r'G:\CS384\2001EE19_2022\tut07\output')
                print(inp)
                df1.to_excel(inp, index=False)  # updating dataframe into excel

                ########################################################################################
                
                sat = sat+1 #iterating to next file in input

        except FileNotFoundError:
            # if Input file is not found / typo in name of the file
            print("Error : Input File Not Found")
        except PermissionError:
             print("Error: Dont have the permission ,Close the output excel file and code the code again")
        except ZeroDivisionError:
            print("Enter valid mod value") #if mod value is invalid 
        except FileExistsError:
            print("File Already Exists, Deleted the existing output file and run again")            

except:
    print("Error:Install Pandas library ")

mod = 5000
octant_analysis(mod)

# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
