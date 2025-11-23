
#Tycoon

#importing packages
import random
import time

#setting global vars

fullturn = 0
subturn = 0
money = 100
switch = 0
xbox = 0
playstation = 0
switchGenerators = []
xboxGenerators = []
playstationGenerators = []
possibleActions = []
validAction = False
possibleCustomerWants = []
customers = ["switch", "switch"]



#subroutines

def getPossibleActions():
    global possibleActions, money
    possibleActions.clear()
    if money >= 100:
        possibleActions.append ("get_switch_generator")

    if money >= 200:
        possibleActions.append ("get_xbox_generator")

    if money >= 300:
        possibleActions.append ("get_playstation_generator")

    if len(switchGenerators) >= 1:
        possibleActions.append ("make_switch")

    if len(xboxGenerators) >= 1:
        possibleActions.append ("make_xbox")

    if len(playstationGenerators) >= 1:
        possibleActions.append ("make_playstation")



def replaceCustomer():

    if "lvl1" in switchGenerators:
        possibleCustomerWants.append("switch")
    
    if "lvl1" in xboxGenerators:
        possibleCustomerWants.append("xbox")
    
    if "lvl1" in playstationGenerators:
        possibleCustomerWants.append("playstation")
    
    if not "lvl1" in switchGenerators or xboxGenerators or playstationGenerators:
        possibleCustomerWants.append("switch")


#start game loop

print()
print("Tycoon game v1.06.1")
print()
print()

while True :
    fullturn = fullturn + 1
    subturn = 0
    if len(customers) <2:
        for b in range(2 - len(customers)):
            replaceCustomer()

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mBefore a turn you will be notified of how many customers are waiting and what they want.\033[0m")
        print("\033[35mThese ones both want a switch.\033[0m")
        print()
    
    print("\033[31mCustomers waiting: ", len(customers), ".\033[0m")

    for c in range(len(customers)):
        print()
        print("\033[33mOne wants one ", customers[c], ".\033[0m")

    print()
    print("\033[34mCurrently, you have:\033[0m")
    print()
    print("\033[34m", switch, " switch\033[0m")
    print("\033[34m", xbox, " xbox\033[0m")
    print("\033[34m", playstation, " playstation\033[0m")
    print()
          

    time.sleep(2)
    print()
    print("\033[32m----------------------turn begin-----------------------\033[0m")
    print()
    subturn = 1

    for d in range(len(switchGenerators)):
        switch = switch + 1
    for e in range(len(xboxGenerators)):
        xbox = xbox + 1
    for f in range(len(playstationGenerators)):
        playstation = playstation + 1

    while subturn <= 3:

        time.sleep(1)
        print()
        print("\033[33m----------------------subturn ", subturn, "------------------------\033[0m")
        print()

        if fullturn == 1:
            if subturn == 1:
                print()
                print("\033[35m-Tutorial-\033[0m")
                print("\033[35mOnce your turn starts, you will then be asked what you want to do.\033[0m")
                print("\033[35mIn each turn you will have three 'subturns'. In a subturn, if you wish,\033[0m")
                print("\033[35myou can end your turn even if you have not used all three subturns.\033[0m")
                print("\033[35mThis time, buy a switch generator with your 100 coins\033[0m")
                print()
            elif subturn == 2:
                print()
                print("\033[35m-Tutorial-\033[0m")
                print("\033[35mNow make a product by hand.\033[0m")
                print()
            elif subturn == 3:
                print()
                print("\033[35m-Tutorial-\033[0m")
                print("\033[35mOnce again make a product by hand.\033[0m")
                print()

        print("\033[34mYour money is: ", money, ".\033[0m")
        print()
        print("\033[34mIn this turn you can:\033[0m")
        print()
        getPossibleActions()
        if "get_switch_generator" in possibleActions:
            print()
            print("\033[32m - Get a switch generator [1]\033[0m")
        
        else:
            print()
            print("\033[31m - Get a switch generator [too expensive]\033[0m")

        if "get_xbox_generator" in possibleActions:
            print()
            print("\033[32m - Get an xbox generator [2]\033[0m")
        
        else:
            print()
            print("\033[31m - Get an xbox generator [too expensive]\033[0m")

        if "get_playstation_generator" in possibleActions:
            print()
            print("\033[32m - Get a playstation generator [3]\033[0m")
        
        else:
            print()
            print("\033[31m - Get a playstation generator [too expensive]\033[0m")

        if ("make_switch" or "make_xbox" or "make_playstation") in possibleActions:
            print()
            print("\033[32m - Make a product by hand [4]\033[0m")
        
        else:
            print()
            print("\033[31m - Make a product by hand [requires generators]\033[0m")


        print()
        print("\033[33m - End turn. [0]\033[0m")
        print()
        while validAction == False:

            try:
                print("\033[36mWhat would you like to do? [0, 1, 2, 3, 4]\033[0m")
                choice = int(input("\033[36m> "))

                if "get_switch_generator" not in possibleActions and choice == 1:
                    print("\033[31mYou do not have enough money to get a switch generator.\033[0m")
                    print()

                elif "get_xbox_generator" not in possibleActions and choice == 2:
                    print("\033[31mYou do not have enough money to get an xbox generator.\033[0m")
                    print()

                elif "get_playstation_generator" not in possibleActions and choice == 3:
                    print("\033[31mYou do not have enough money to get a playstation generator.\033[0m")
                    print()

                elif choice == 0:
                    validAction = True
                    subturn = 4
                    
                elif choice == 1 or 2 or 3 or 4:
                    
                    validAction = True

                else:
                    print("\033[31mPlease enter either [0, 1, 2, 3, 4].\033[0m")

            except:
                print("\033[31mInvalid. Please try again.\033[0m")


        if choice == 0:
            print()
            choice = 9
            validAction = False

        elif choice == 1:
            switchGenerators.append ("lvl1")
            money = money - 100
            choice = 9
            validAction = False

        elif choice == 2:
            xboxGenerators.append ("lvl1")
            money = money - 200
            choice = 9
            validAction = False

        elif choice == 3:
            playstationGenerators.append ("lvl1")
            money = money - 300
            choice = 9
            validAction = False

        elif choice == 4:

            if fullturn == 1:
                print()
                print("\033[35m-Tutorial-\033[0m")
                print("\033[35mMake a switch.\033[0m")
                print()

            print("\033[34mYou can make:\033[0m")
            if "make_switch" in possibleActions:
                print("\033[32m - One switch [1]\033[0m")
            
            else:
                print("\033[31m - switch [requires generators]\033[0m")

            if "make_xbox" in possibleActions:
                print("\033[32m - One xbox [2]\033[0m")

            else:
                print("\033[31m - xbox [requires generators]\033[0m")

            if "make_playstation" in possibleActions:
                print("\033[32m - One playstation [3]\033[0m")
            
            else:
                print("\033[31m - playstation [requires generators]\033[0m")

            validChoice = False

            while validChoice == False:
                print()

                try:
                    print("\033[36mWhich would you like to make [1, 2, 3]\033[0m")
                    productchoice = int(input("\033[36m> "))

                    if productchoice == 1 and "make_switch" in possibleActions:
                        print("\033[33mmaking product...\033[0m")
                        time.sleep(3)
                        print("\033[32mYou now have one more switch\033[0m")
                        switch = switch + 1
                        validChoice = True

                    elif productchoice == 2 and "make_xbox" in possibleActions:
                        print("\033[33mmaking product...\033[0m")
                        time.sleep(3)
                        print("\033[32mYou now have one more xbox.\033[0m")
                        xbox = xbox + 1
                        validChoice = True

                    elif productchoice == 3 and "make_playstation" in possibleActions:
                        print("\033[33mmaking product...\033[0m")
                        time.sleep(3)
                        print("\033[32mYou now have one more playstation.\033[0m")
                        playstation = playstation + 1
                        validChoice = True

                    elif productchoice > 3:
                        print("\033[31mInvalid. please enter [1, 2, 3]\033[0m")

                    else:
                        print("\033[31mYou do not have a generator for this product yet so therefore cannot create one yourself.\033[0m")
                        print("Please enter a product you can make.")
                except:
                    print("\033[31mInvalid. Please try again.\033[0m")

            choice = 9
            validAction = False
        subturn = subturn + 1

            
    print()
    time.sleep(1)
    print("\033[31m-----------------------turn end------------------------\033[0m")
    time.sleep(2)

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mAfter a turn you can then sell your made products to waiting customers.\033[0m")
        print("\033[35mSell both of your switches to these customers.\033[0m")
        print()

    print()
    print("\033[34mTime to sell products:\033[0m")
    print()
    print("\033[34mYou have:\033[0m")
    print()
    print("\033[34m - ", switch, " switch(es)\033[0m")
    print("\033[34m - ", xbox, " xbox(es)\033[0m")
    print("\033[34m - ", playstation, " playstation(s)\033[0m")

    for g in range(len(customers)):
        print()
        print("\033[34mOne customer wants one ", customers[c], "\033[0m")
        print("\033[36mWhat would you like to do?\033[0m")
        print()

        if len(switchGenerators) >=1:
            print("\033[32m - sell one ", customers[c], " to them [1]\033[0m")
        
        else:
            print("\033[31m - sell one ", customers[c], " to them\033[0m")
        print("\033[33m - do not sell to them yet [2]\033[0m")
        print("\033[33m - dismiss them from the shop without serving them [3]\033[0m")
        validSellChoice = False

        while validSellChoice == False:
            print()

            try:
                sellchoice = int(input("\033[36m> "))

                if sellchoice == 1:

                    if customers[c] == "switch":
                        
                        if switch >= 1:
                            switch = switch - 1
                            money = money + 50
                            print("\033[33mMoney now: ", money, "\033[0m")
                            print()
                            validSellChoice = True

                        else:
                            print("\033[31mSorry, you do not have enough switches.\033[0m")
                            print()
                            print("\033[31mPlease enter [2, 3]\033[0m")
                            print()

                    elif customers[c] == "xbox":

                        if xbox >= 1:
                            xbox = xbox - 1
                            money = money + 100
                            print("\033[33mMoney now: ", money, "\033[0m")
                            print()
                            validSellChoice = True

                        else:
                            print("\033[31mSorry, you do not have enough xboxes.\033[0m")
                            print()
                            print("\033[31mPlease enter [2, 3]\033[0m")
                            print()

                    elif customers[c] == "playstation":

                        if playstation >= 1:
                            playstation = playstation - 1
                            money = money + 150
                            print("\033[33mMoney now: ", money, "\033[0m")
                            print()
                            validSellChoice = True

                        else:
                            print("\033[31mSorry, you do not have enough playstations.\033[0m")
                            print()
                            print("\033[31mPlease enter [2, 3\033[0m")
                            print()
                elif sellchoice == 2:
                    print()
                    validSellChoice = True

                elif sellchoice == 3:
                    print()
                    customers.remove(c)
                    validSellChoice = True

                else:
                    print("\033[31mInvalid. Please enter [1, 2, 3]\033[0m")

            except:
                print("\033[31mInvalid. Please try again.\033[0m")

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mCongratulations! You have now completed the tutorial!\033[0m")
        print("\033[35mEnjoy my game! :)\033[0m")
        print()

    print()
    print()
    print("\033[33m-------------------------------------------------------\033[0m")
    time.sleep(4)
    print()
    print()