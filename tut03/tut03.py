
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
            # assigning the values to respectivley Coloumn
            df1.iloc[0, 4] = avg_u
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
            for i in range(8):  # Updating a Octant Column
                df1.loc[i, "Octant "] = arr[i]

            df1["Longest Subsequence Length"] = " "  # Empty Column
            df1["Count"] = " "  # Empty Column

            l = len(df1)  # 29745
            x = 0

            # Longest subsequence length for respectively octant values #initlizing a max_count with all zeroes
            max_count = [0]*8

            # for count of LSL for respectively octant values # initlizing a max_count with all zeroes
            max_count1 = [0]*8
            d1 = {"+1": 0, "-1": 1, "+2": 2, "-2": 3,
                  "+3": 4, "-3": 5, "+4": 6, "-4": 7}# creating a dictionary

            while (x < l):
                s1 = df1.at[x, "Octant"]
                count = 0
                j = x
                while (1):  # counting length of sequence
                    # breaking if next element is not equal to s1
                    if (j >= l or df1.at[j, "Octant"] != s1):
                        break
                    count += 1
                    j += 1

                x += count
                temp = max_count[d1[s1]]

                # updating a maximum count of value if current count is greater
                max_count[d1[s1]] = max(max_count[d1[s1]], count)

                if (count > temp):
                    max_count1[d1[s1]] = 1 ##Reassigning the values of LSL count to one

                if (count == temp):
                    max_count1[d1[s1]] += 1 ##incremneting the count of LSL by one

            for i in range(8):  # updating Longest subsequence length for respectively octant values
                df1.loc[i, "Longest Subsequence Length"] = max_count[i]

            for j in range(8):  # updating count of LSL for respectively octant values
                df1.loc[j, "Count"] = max_count1[j]

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
