import csv
import pandas as pd
import math


def octact_identification(mod=5000):

    df1 = pd.read_csv("octant_input.csv")  # reading the input file

    avg_u = df1['U'].mean()  # Calculating average of U,V,W
    avg_v = df1['V'].mean()
    avg_w = df1['W'].mean()

    df1["U_Avg"] = ''  # Creating average for coloumns U,V,W
    df1["V_Avg"] = ''
    df1["W_Avg"] = ''
    df1.iloc[0, 4] = avg_u  # assigning the values to respectivley Coloumn
    df1.iloc[0, 5] = avg_v
    df1.iloc[0, 6] = avg_w

    df1["U'=U - U avg"] = df1["U"]-avg_u   # Creating new coloumns with Header U',V',W'
    df1["V'=V - V avg"] = df1["V"]-avg_v
    df1["W'=W - W avg"] = df1["W"]-avg_w

    # df1.to_csv('octant_output.csv')

                  #######          Data PreProcessing     ###########


    df1["Octant"] = '' ## Creatig a empty Column with Header as Octant

    l = len(df1)  # length of DataFrame = 29745

    #creating octant column ,and Identifying the octant value for each triple(U_1,V_1,W_1)
    for i in range(0, l):

        if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] > 0):
            df1.loc[i, "Octant"] = "+1"  ## for +1 

        if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] < 0):
            df1.loc[i, "Octant"] = "-1"  ## for -1 

        if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] > 0):
            df1.loc[i, "Octant"] = "+2"   ## for +2 

        if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] > 0 and df1.loc[i, "W'=W - W avg"] < 0):
            df1.loc[i, "Octant"] = "-2"    ## for -2 

        if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] > 0):
            df1.loc[i, "Octant"] = "+3"    ## for +3 

        if (df1.loc[i, "U'=U - U avg"] < 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
            df1.loc[i, "Octant"] = "-3"     ## for -3 

        if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] > 0):
            df1.loc[i, "Octant"] = "+4"     ## for +4

        if (df1.loc[i, "U'=U - U avg"] > 0 and df1.loc[i, "V'=V - V avg"] < 0 and df1.loc[i, "W'=W - W avg"] < 0):
            df1.loc[i, "Octant"] = "-4"      ## for -4 

    # df1.to_csv('octant_output.csv')

                         ######  Octant Identification  ########

    df1[" "] = ""  ## creating empty Column without header and assigned "User input" to row 3
    df1.iloc[1, 11] = "User Input"  

    df1["Octant ID"] = "" ## creating a Coloumn with header as Octant ID 
    df1.loc[0, "Octant ID"] = "Overall Octant"
    df1.loc[1, "Octant ID"] = "Mod "+str(mod)

    oct_count = df1['Octant'].value_counts()# oct_count stores a count of unique elements i.e. count of +1,-1,+2,-2,+3,-4,+4 
    #And assigning a count values to respectively Coloumns
    df1.loc[0, "+1"] = oct_count["+1"]
    df1.loc[0, "-1"] = oct_count["-1"]
    df1.loc[0, "+2"] = oct_count["+2"]
    df1.loc[0, "-2"] = oct_count["-2"]
    df1.loc[0, "+3"] = oct_count["+3"]
    df1.loc[0, "-3"] = oct_count["-3"]
    df1.loc[0, "+4"] = oct_count["+4"]
    df1.loc[0, "-4"] = oct_count["-4"]   

    #df1.to_csv('octant_output.csv')

                  ###########   Added Some Columns And Rows for MOD Count   ##########                

    x = 0 # for findind octant values for MOD ranges
    t = 2 #for 
    while (x < l): ##

        c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = 0 ## count values of each octant is stored in varibles for MOD ranges 

        for i in range(x,x+mod,1):

            if(i>=l):
                break ## bound check 
            if (df1.loc[i, "Octant"] == "+1"):
                c1+=1 ## count of +1
            if (df1.loc[i, "Octant"] == "-1"):
                c2+=1 ## count of -1
            if (df1.loc[i, "Octant"] == "+2"):
                c3+=1 ## count of +2
            if (df1.loc[i, "Octant"] == "-2"):
                c4+=1 ## count of -2
            if (df1.loc[i, "Octant"] == "+3"):
                c5+=1 ## count of +3
            if (df1.loc[i, "Octant"] == "-3"):
                c6+=1 ## count of -3
            if (df1.loc[i, "Octant"] == "+4"):
                c7+=1 ## count of -4
            if (df1.loc[i, "Octant"] == "-4"):
                c8+=1 ## count of +4

        # assigning overall count of octants in each interval
        df1.loc[t, "+1"] = c1
        df1.loc[t, "-1"] = c2
        df1.loc[t, "+2"] = c3
        df1.loc[t, "-2"] = c4
        df1.loc[t, "+3"] = c5
        df1.loc[t, "-3"] = c6
        df1.loc[t, "+4"] = c7
        df1.loc[t, "-4"] = c8


        if((x+mod)>l): # Writing MOD ranges in Octant ID Coloumn
            df1.loc[t,"Octant ID"]=str(x)+"-"+str(l-1)## for last index(i.e) 2744
        else:
            df1.loc[t,"Octant ID"]=str(x)+"-"+str(x+mod-1)

        x+=mod
        t+=1 
    
               ################ Octant Count Based on Mod Values  ######################
    df1.to_csv('octant_output.csv') ## Updating into a octant_output.csv file


mod = 5000
octact_identification(mod)
