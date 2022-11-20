
check=1
def add (a,b):
    return a+b
def sub (a,b):
    return a-b
def mul (a,b):
    return a*b
def div (a,b):
    return a/b
c=0
while check==1:
    num1=int(input("num1--->"))
    num2=int(input("num2--->"))
    ope=input("operation--->")
    if ope=="+":
        c=add(num1,num2)
    elif ope=="-":
        c=sub(num1,num2)
    elif ope=="*":
        c=mul(num1,num2)
    elif ope=="/":
        c=div(num1,num2)
    else:
        print("You pick the wrong house, sucka mama!")
        break
    print("\noutput-->",c)
    print("You're bad at math so you want to cheat on here, huh?")
    print("\nenter 0 or 1")
    check=int(input("Wanna continue? Sucka mama?"))                

    
    
