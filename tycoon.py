
#Tycoon

import random

#setting global vars

money = 400
product1 = 0
product2 = 0
product3 = 0
prod1Generators = []
prod2Generators = []
prod3Generators = []
possibleActions = []
validAction = False

#subroutines

def getPossibleActions():
    global possibleActions, money
    possibleActions.clear()
    if money >= 50:
        possibleActions.append ("get1")
    if money >= 150:
        possibleActions.append ("get2")
    if money >= 250:
        possibleActions.append ("get3")
    if "lvl1" in prod1Generators:
        if  money >= 300:
            possibleActions.append ("upgrade1")
        


#start game loop

while True :
    print()
    print("-----------------------------------------------")
    print()
    print("Your money is: ", money, ".")
    print()
    print("In this turn you can:")
    print()
    getPossibleActions()
    if "get1" in possibleActions:
        print()
        print(" - Get a generator for product 1 [1]")

    if "get2" in possibleActions:
        print()
        print(" - Get a generator for product 2 [2]")

    if "get3" in possibleActions:
        print()
        print(" - Get a generator for product 3 [3]")

    if "upgrade1" in possibleActions:
        print()
        print(" - Upgrade a level 1 generator for product 1 [4]")

    print()
    print(" - Skip turn. [0]")
    print()

    while validAction == False:
        print("What would you like to do? [1, 2, 3, 4, 0]")
        choice = int(input("> "))

        if "get1" not in possibleActions and choice == 1:
            print("You do not have enough money to get a generator for product 1.")
            print()

        elif "get2" not in possibleActions and choice == 2:
            print("You do not have enough money to get a generator for product 2.")
            print()

        elif "get3" not in possibleActions and choice == 3:
            print("You do not have enough money to get a generator for product 3.")
            print()

        elif "upgrade1" not in possibleActions and choice == 4:
            print("You do not have enough money to upgrade a product 1 generator or you do not have one.")
            print()

        elif choice == 0:
            print("Are you sure you want to skip the turn? Money: ", money, ". [Y, N]")
            skipTurn = input("> ")
            if skipTurn == "Y":
                validAction = True
            else:
                print("Ok.")
                print()
            
        elif choice == 1 or choice == 2 or choice == 3 or choice == 4:
            
            validAction = True

        else:
            print("Please enter either [1, 2, 3, 4].")


    if choice == 0:
        print()

    elif choice == 1:
        prod1Generators.append ("lvl1")
        money = money - 50

    elif choice == 2:
        prod2Generators.append ("lvl1")
        money = money - 150

    elif choice == 3:
        prod3Generators.append ("lvl1")
        money = money - 250
    
    elif choice == 4:
        lvl1Idx = int(prod1Generators.index ("lvl1"))
        prod1Generators[lvl1Idx] = "lvl2"
        money = money - 300
    
    choice = 5
    validAction = False
