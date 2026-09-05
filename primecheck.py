import math

while True:
    num = int(input("enter ur number: "))
    if num <= 1 or num % 2 == 0:
         print("not prime")

    elif num == 2 or num == 3:

         print("prime")

    else:


        n1 = num + 1
        n2 = num - 1

        if (n1 % 2 == 0 and n1 % 3 == 0) or (n2 % 2 == 0 and n2 % 3 == 0):
            print("your number can be prime")
        else:

            print("your number is definitely not prime")

