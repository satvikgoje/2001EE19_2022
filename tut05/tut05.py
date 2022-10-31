try:
    import pandas as pd

    from datetime import datetime
    start_time = datetime.now()


    def octant_range_names(mod=5000):

        try:
            df1 = pd.read_excel("octant_input.xlsx")  # reading the input file

            avg_u = df1['U'].mean()  # Calculating average of U,V,W
            avg_v = df1['V'].mean()
            avg_w = df1['W'].mean()

            df1["U_Avg"] = ''  # Creating average for coloumns U,V,W
            df1["V_Avg"] = ''
            df1["W_Avg"] = ''
            df1.iloc[0, 4] = avg_u  # assigning the values to respectivley Coloumn
            df1.iloc[0, 5] = avg_v
            df1.iloc[0, 6] = avg_w

            # Creating new coloumns with Header U',V',W'
            df1["U'=U - U avg"] = df1["U"]-avg_u
            df1["V'=V - V avg"] = df1["V"]-avg_v
            df1["W'=W - W avg"] = df1["W"]-avg_w

            # df1.to_csv('octant_output.csv')

            #######          Data PreProcessing     ###########

            df1["Octant"] = ''  # Creatig a empty Column with Header as Octant

            l = len(df1)  # length of DataFrame = 29745

            # creating octant column ,and Identifying the octant value for each triple(U_1,V_1,W_1)
            for i in range(0, l):

                if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] > 0):
                    df1.loc[i, "Octant"] = "+1"  # for +1

                if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] < 0):
                    df1.loc[i, "Octant"] = "-1"  # for -1

                if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] > 0):
                    df1.loc[i, "Octant"] = "+2"  # for +2

                if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] < 0):
                    df1.loc[i, "Octant"] = "-2"  # for -2

                if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] > 0):
                    df1.loc[i, "Octant"] = "+3"  # for +3

                if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
                    df1.loc[i, "Octant"] = "-3"  # for -3

                if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] > 0):
                    df1.loc[i, "Octant"] = "+4"  # for +4

                if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
                    df1.loc[i, "Octant"] = "-4"  # for -4

                    ######  Octant Identification  ########

            # creating empty Column without header and assigned "User input" to row 3
            df1[" "] = ""
            df1.iloc[1, 11] = "User Input"

            df1["Octant ID"] = " "  # creating a Coloumn with header as Octant ID
            df1.loc[0, "Octant ID"] = "Overall Octant"
            df1.loc[1, "Octant ID"] = "Mod "+str(mod)

            # oct_count stores a count of unique elements i.e. count of +1,-1,+2,-2,+3,-4,+4
            oct_count = df1['Octant'].value_counts()
            
            arr = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"] #cretaed for reference

            oct_cnt = {} #for storing octant count as key and and coreesponding octant value as value in dict 
            for i in range(8):
                s = arr[i] 
                oct_cnt.update({oct_count[s]: s})# appending the overall count of octant and octant value in dict i.e for Ex:(2610,"+1")
                df1.loc[0, s] = oct_count[s]# And assigning a count values to respectively Coloumns

            # print(oct_cnt) #{2610: '+1', 4603: '-1', 4855: '+2', 2798: '-2', 4548: '+3', 2784: '-3', 2769: '+4', 4778: '-4'}
            sortedbykey = {k: v for k, v in sorted(oct_cnt.items())} #sorting the dict by keys
            # print(sortedbykey) {2610: '+1', 2769: '+4', 2784: '-3', 2798: '-2', 4548: '+3', 4603: '-1', 4778: '-4', 4855: '+2'}
            sortedbykey_lst = list(sortedbykey.values()) #storing the sorted values in a list
            # print(sortedbykey_lst)['+1', '+4', '-3', '-2', '+3', '-1', '-4', '+2']

            octant_name_id_mapping = {"1": "Internal outward interaction", "-1": "External outward interaction", "2": "External Ejection",
                                    "-2": "Internal Ejection", "3": "External inward interaction", "-3": "Internal inward interaction", "4": "Internal sweep", "-4": "External sweep"}

            df1["Rank 1"] = ''#created empty columns
            df1["Rank 2"] = ''
            df1["Rank 3"] = ''
            df1["Rank 4"] = ''
            df1["Rank 5"] = ''
            df1["Rank 6"] = ''
            df1["Rank 7"] = ''
            df1["Rank 8"] = ''

            dic_rank = {"+1": "Rank 1", "-1": "Rank 2", "+2": "Rank 3", "-2": "Rank 4",
                        "+3": "Rank 5", "-3": "Rank 6", "+4": "Rank 7", "-4": "Rank 8"}#for reference

            for i in range(8):
                df1.loc[0, dic_rank[sortedbykey_lst[i]]] = 8-i #appending the octant ranks of octants

                    ###########   Added Some Columns And Rows for MOD Count   ##########

            x = 0  # for findind octant values for MOD ranges
            t = 2  # for row pointer

            while (x < l):

                d1 = {"+1": 0, "-1": 1, "+2": 2, "-2": 3, "+3": 4,
                    "-3": 5, "+4": 6, "-4": 7}  # creating a dictionary for reference

                oct_cnt_mod = [0]*8 # count values of each octant is stored for MOD ranges

                oct_cnt = {} #for storing octant count as key and and coreesponding octant value as value in dict
                for i in range(x, x+mod, 1):

                    if (i >= l):
                        break  # bound check
                    s3 = df1.at[i, "Octant"]
                    oct_cnt_mod[d1[s3]] += 1 #incrementing by one of count values of corresponding octants 

                for i in range(8):
                    s = arr[i]
                    # assigning overall count of octants in each interval
                    df1.loc[t, s] = oct_cnt_mod[i]
                    oct_cnt.update({oct_cnt_mod[i]: s})#appending the overall count of octant and octant value in dict

                sortedbykey = {k: v for k, v in sorted(oct_cnt.items())}#sorting the dict by keys
                sortedbykey_lst = list(sortedbykey.values())#storing the sorted values in a list

                for i in range(8):
                    df1.loc[t, dic_rank[sortedbykey_lst[i]]] = 8-i #appending the octant ranks of octants

                if ((x+mod) > l):  # Writing MOD ranges in Octant ID Coloumn
                    df1.loc[t, "Octant ID"] = str(x)+"-"+str(l-1)  # for last index(i.e) 2744
                else:
                    df1.loc[t, "Octant ID"] = str(x)+"-"+str(x+mod-1)

                x += mod
                t += 1


            df1.to_excel('octant_output_ranking_excel.xlsx', index=False)

        except FileNotFoundError:
            # if Input file is not found / typo in name of the file
            print("Error : Input File Not Found")
        except PermissionError:
             print("Error: Dont have the permission ,Close the output excel file and code the code again")
        except ZeroDivisionError:
            print("Enter valid mod value") #if mod value is invalid   


except:
    print("Error:Install Pandas library ")

mod = 5000
octant_range_names(mod)

# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
