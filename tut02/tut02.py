try:
 import pandas as pd
 import openpyxl

 def octact_identification(mod=5000):
   try:
    # reading the input file
    df1 = pd.read_excel("input_octant_transition_identify.xlsx")

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

    # df1.to_csv('octant_output.csv')

            ######  Octant Identification  ########

    # creating empty Column without header and assigned "User input" to row 3
    df1[" "] = ""
    df1.iloc[1, 11] = "User Input"

    df1["Octant ID"] = ""  # creating a Coloumn with header as Octant ID
    df1.loc[0, "Octant ID"] = "Overall Octant"
    df1.loc[1, "Octant ID"] = "Mod "+str(mod)

    # oct_count stores a count of unique elements i.e. count of +1,-1,+2,-2,+3,-4,+4
    oct_count = df1['Octant'].value_counts()
    # And assigning a count values to respectively Coloumns
    # sum=[0]*8
    df1.loc[0, "+1"] = oct_count["+1"]
    df1.loc[0, "-1"] = oct_count["-1"]
    df1.loc[0, "+2"] = oct_count["+2"]
    df1.loc[0, "-2"] = oct_count["-2"]
    df1.loc[0, "+3"] = oct_count["+3"]
    df1.loc[0, "-3"] = oct_count["-3"]
    df1.loc[0, "+4"] = oct_count["+4"]
    df1.loc[0, "-4"] = oct_count["-4"]

    # df1.to_csv('octant_output.csv')

    ###########   Added Some Columns And Rows for MOD Count   ##########

    x = 0  # for findind octant values for MOD ranges
    t = 2  # row index
    while (x < l):

        # count values of each octant is stored in varibles for MOD ranges
        c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = 0

        for i in range(x, x+mod, 1):

            if (i >= l):
                break  # bound check
            if (df1.loc[i, "Octant"] == "+1"):
                c1 += 1  # count of +1
            if (df1.loc[i, "Octant"] == "-1"):
                c2 += 1  # count of -1
            if (df1.loc[i, "Octant"] == "+2"):
                c3 += 1  # count of +2
            if (df1.loc[i, "Octant"] == "-2"):
                c4 += 1  # count of -2
            if (df1.loc[i, "Octant"] == "+3"):
                c5 += 1  # count of +3
            if (df1.loc[i, "Octant"] == "-3"):
                c6 += 1  # count of -3
            if (df1.loc[i, "Octant"] == "+4"):
                c7 += 1  # count of -4
            if (df1.loc[i, "Octant"] == "-4"):
                c8 += 1  # count of +4

        # assigning overall count of octants in each interval
        df1.loc[t, "+1"] = c1
        df1.loc[t, "-1"] = c2
        df1.loc[t, "+2"] = c3
        df1.loc[t, "-2"] = c4
        df1.loc[t, "+3"] = c5
        df1.loc[t, "-3"] = c6
        df1.loc[t, "+4"] = c7
        df1.loc[t, "-4"] = c8

        if ((x+mod) > l):  # Writing MOD ranges in Octant ID Coloumn
            df1.loc[t, "Octant ID"] = str(x)+"-"+str(l-1)  # for last index(i.e) 2744
            break
            # h=df1.columns ## h stores column labels
            # y=h.get_loc("+1") ## header name in index format(integer) (here ,y=13)
            # j=0
            # for i in range(y,y+8):
            #     df1.iloc[t+1,i]=sum[j] ##verifing the count of octants
            #     j +=1
        else:
            df1.loc[t, "Octant ID"] = str(x)+"-"+str(x+mod-1)

        x += mod
        t += 1

        ################ Octant Count Based on Mod Values  ######################
    t += 4
    df1.loc[t, "Octant ID"] = "Overall Transition Count"
    df1.loc[t+1, "+1"] = "To"
    t += 2
    arr = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]
    df1.loc[t, "Octant ID"] = "Count"
    df1.iloc[t+1, 11] = "From"
    h = df1.columns  # h stores column labels
    y = h.get_loc("+1")  # header name in index format(integer) (here ,y=13)
    j = 0
    for i in range(y, y+8):
        df1.iloc[t, i] = arr[j]  # verifing the count of octants
        j += 1

    j = 0
    for i in range(t+1, t+9): 
        df1.loc[i, "Octant ID"] = arr[j] #updating Octant ID column 
        j += 1


    t1 = 0
    t2 = 1
    d1 = {"+1": 1, "-1": 2, "+2": 3, "-2": 4,"+3": 5, "-3": 6, "+4": 7, "-4": 8}
    while (1):
        if (t2 == l):
            break
        s1 = df1.at[t1, "Octant"]  # From
        s2 = df1.at[t2, "Octant"]  # To

        if (pd.isnull(df1.loc[t+d1[s1], s2])):## checking if cell is empty/null
            df1.loc[t+d1[s1], s2] = 1 ## adding one
        else:
            df1.loc[t+d1[s1], s2] = int(df1.loc[t+d1[s1], s2]) + 1 ## increamenting the count by one and updating it to coloumn
        t1 += 1
        t2 += 1

    t += 8
    x = 0
    while (x < l): 
        t += 4
        df1.loc[t, "Octant ID"] = "Mod Transition Count"
        if ((x+mod) > l):  # Writing MOD ranges in Octant ID Coloumn
            df1.loc[t+1, "Octant ID"] = str(x)+"-"+str(l-1)  # for last index(i.e) 2744
        else:
            df1.loc[t+1, "Octant ID"] = str(x)+"-"+str(x+mod-1)    
        df1.loc[t+1, "+1"] = "To"
        t += 2
        arr = ["+1", "-1", "+2", "-2", "+3", "-3", "+4", "-4"]
        df1.loc[t, "Octant ID"] = "Count"
        df1.iloc[t+1, 11] = "From"
        h = df1.columns  # h stores column labels
        # header name in index format(integer) (here ,y=13)
        y = h.get_loc("+1")
        j = 0
        for i in range(y, y+8): ## updating a row
            df1.iloc[t, i] = arr[j] 
            j += 1

        j = 0
        for i in range(t+1, t+9): ## updating Coloumn
            df1.loc[i, "Octant ID"] = arr[j]
            j += 1


        for i in range(x, x+mod):## each interval

            if (i == l-1):
                break
            s1 = df1.at[i, "Octant"]  # From
            s2 = df1.at[i+1, "Octant"]  # To

            if (pd.isnull(df1.loc[t+d1[s1], s2])):## checking if cell is empty/null
                df1.loc[t+d1[s1], s2] = 1## adding one
            else:
                df1.loc[t+d1[s1], s2] = int(df1.loc[t+d1[s1], s2]) + 1## increamenting the count by one and updating it to coloumn

        t += 8
        x += mod
    
    # index=flase removes the index coloum

    df1.to_excel('output_octant_transition_identify.xlsx', index=False)  
    # Updating into a output_octant_transition_identify.xlsx file
   except FileNotFoundError:
    print("Error : Input File Not Found") #if Input file is not found / typo in name of the file

   except ZeroDivisionError:
     print("Enter valid mod value") #if mod value is invalid
 


except :
    print("Import pandas/openpyxl libraries ")

try:    
  mod = 5000
  octact_identification(mod)
except:
  print("Error in the code")  