import csv
import pandas as pd
import math

def octact_identification(mod=5000):
    
    df1=pd.read_csv("octant_input.csv") # reading the input file

    avg_u=df1['U'].mean()     #Calculating average of U,V,W
    avg_v=df1['V'].mean()
    avg_w=df1['W'].mean()
    
    df1["U_Avg"]=''    #Creating average for coloumns U,V,W 
    df1["V_Avg"]=''
    df1["W_Avg"]=''
    df1.iloc[0,4]=avg_u    #assigning the values to respectivley Coloumn
    df1.iloc[0,5]=avg_v
    df1.iloc[0,6]=avg_w

    df1["U'=U - U avg"]=df1["U"]-avg_u   # Creating new columns for U',V',W'
    df1["V'=V - V avg"]=df1["V"]-avg_v
    df1["W'=W - W avg"]=df1["W"]-avg_w

    df1.to_csv('ouput.csv')
    #######          Data PreProcessing     ###########


mod=5000
octact_identification(mod)

