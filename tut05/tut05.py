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
