
def factorial(x):
    if(x<2):
        return x
    else:
        return factorial(x-1)*x    

x=int(input("Enter the number whose factorial is to be found :"))
print(factorial(x))

