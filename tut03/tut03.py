
try:
 import pandas as pd

 from datetime import datetime
 start_time = datetime.now()


 def octant_longest_subsequence_count():
    # reading the input file
    try:
        df1 = pd.read_excel("input_octant_longest_subsequence.xlsx")

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

        df1[" "] = " "
        df1["Octant "] = " "
        arr = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]
        for i in range(8): # Updating a Octant Column 
            df1.loc[i, "Octant "] = arr[i]


        df1["Longest Subsequence Length"] = " " #Empty Column
        df1["Count"] = " " #Empty Column

        df1.to_excel('output_octant_longest_subsequence.xlsx', index=False)
        # Updating into a output_octant_transition_identify.xlsx file
    except FileNotFoundError: 
        print("error in a new file")

except:
    print("Install pandas library ")

octant_longest_subsequence_count()
# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))

