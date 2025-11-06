
#Tycoon

#importing packages
import random
import time

#setting global vars

fullturn = 0
subturn = 0
money = 100
product1 = 0
product2 = 0
product3 = 0
product1Generators = []
product2Generators = []
product3Generators = []
possibleActions = []
validAction = False
possibleCustomerWants = []
customers = ["product1", "product1"]



#subroutines

def getPossibleActions():
    global possibleActions, money
    possibleActions.clear()
    if money >= 100:
        possibleActions.append ("get_product1_generator")

    if money >= 200:
        possibleActions.append ("get_product2_generator")

    if money >= 300:
        possibleActions.append ("get_product3_generator")

    if len(product1Generators) >= 1:
        possibleActions.append ("make_product1")

    if len(product2Generators) >= 1:
        possibleActions.append ("make_product2")

    if len(product3Generators) >= 1:
        possibleActions.append ("make_product3")


def replaceCustomer():

    if "lvl1" in product1Generators:
        possibleCustomerWants.append("product1")
    
    if "lvl1" in product2Generators:
        possibleCustomerWants.append("product2")
    
    if "lvl1" in product3Generators:
        possibleCustomerWants.append("product3")
    
    if not "lvl1" in product1Generators or product2Generators or product3Generators:
        possibleCustomerWants.append("product1")


#start game loop

print()
print("Tycoon game v1.05.2")
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
        print("-Tutorial-")
        print("Before a turn you will be notified of how many customers are waiting and what they want.")
        print("These ones both want a product1.")
        print()
    
    print("Customers waiting: ", len(customers), ".")

    for c in range(len(customers)):
        print()
        print("One wants ", customers[c], ".")

    print()
    print("Currently, you have:" )
    print()
    print(product1, " product1")
    print(product2, " product2")
    print(product3, " product3")
    print()
          

    time.sleep(2)
    print()
    print("----------------------turn begin-----------------------")
    print()
    subturn = 1

    for d in range(len(product1Generators)):
        product1 = product1 + 1
    for e in range(len(product2Generators)):
        product2 = product2 + 1
    for f in range(len(product3Generators)):
        product3 = product3 + 1

    while subturn <= 3:

        time.sleep(1)
        print()
        print("----------------------subturn ", subturn, "------------------------")
        print()

        if fullturn == 1:
            if subturn == 1:
                print()
                print("-Tutorial-")
                print("Once your turn starts, you will then be asked what you want to do.")
                print("In each turn you will have three 'subturns'. In a subturn, if you wish,")
                print("you can end your turn even if you have not used all three subturns.")
                print("This time, buy a product1 generator with your 100 coins.")
                print()
            elif subturn == 2:
                print()
                print("-Tutorial-")
                print("Now make a product by hand.")
                print()
            elif subturn == 3:
                print()
                print("-Tutorial-")
                print("Once again make a product by hand.")
                print()

        print("Your money is: ", money, ".")
        print()
        print("In this turn you can:")
        print()
        getPossibleActions()
        if "get_product1_generator" in possibleActions:
            print()
            print(" - Get a product1 generator [1]")

        if "get_product2_generator" in possibleActions:
            print()
            print(" - Get a product2 generator [2]")

        if "get_product3_generator" in possibleActions:
            print()
            print(" - Get a product3 generator [3]")

        if "make_product1" or "make_product2" or "make_product3" in possibleActions:
            print()
            print(" - make a product by hand [4]")


        print()
        print(" - End turn. [0]")
        print()
        while validAction == False:
            print("What would you like to do? [0, 1, 2, 3, 4]")
            choice = int(input("> "))

            if "get_product1_generator" not in possibleActions and choice == 1:
                print("You do not have enough money to get a product1 generator.")
                print()

            elif "get_product2_generator" not in possibleActions and choice == 2:
                print("You do not have enough money to get a product2 generator.")
                print()

            elif "get_product3_generator" not in possibleActions and choice == 3:
                print("You do not have enough money to get a product3 generator.")
                print()

            elif choice == 0:
                validAction = True
                subturn = 4
                
            elif choice == 1 or 2 or 3 or 4:
                
                validAction = True

            else:
                print("Please enter either [0, 1, 2, 3, 4].")


        if choice == 0:
            print()
            choice = 9
            validAction = False

        elif choice == 1:
            product1Generators.append ("lvl1")
            money = money - 100
            choice = 9
            validAction = False

        elif choice == 2:
            product2Generators.append ("lvl1")
            money = money - 200
            choice = 9
            validAction = False

        elif choice == 3:
            product3Generators.append ("lvl1")
            money = money - 300
            choice = 9
            validAction = False

        elif choice == 4:

            if fullturn == 1:
                print()
                print("-Tutorial-")
                print("Make a product1.")
                print()

            print("You can make:")
            if "make_product1" in possibleActions:
                print(" - One of product1 [1]")

            if "make_product2" in possibleActions:
                print(" - One of product2 [2]")

            if "make_product3" in possibleActions:
                print(" - One of product3 [3]")

            validChoice = False

            while validChoice == False:
                print()
                print("Which would you like to make [1, 2, 3]")
                productchoice = int(input("> "))

                if productchoice == 1 and "make_product1" in possibleActions:
                    print("making product...")
                    time.sleep(3)
                    print("You now have one more of product1.")
                    product1 = product1 + 1
                    validChoice = True

                elif productchoice == 2 and "make_product2" in possibleActions:
                    print("making product...")
                    time.sleep(3)
                    print("You now have one more of product2.")
                    product2 = product2 + 1
                    validChoice = True

                elif productchoice == 3 and "make_product3" in possibleActions:
                    print("making product...")
                    time.sleep(3)
                    print("You now have one more of product3.")
                    product3 = product3 + 1
                    validChoice = True

                elif productchoice > 3:
                    print("Invalid. please enter [1, 2, 3]")

                else:
                    print("You do not have a generator for this product yet so therefore cannot create one yourself.")
                    print("Please enter a product you can make.")
            choice = 9
            validAction = False
        subturn = subturn + 1

            
    print()
    time.sleep(1)
    print("-----------------------turn end------------------------")
    time.sleep(2)

    if fullturn == 1:
        print()
        print("-Tutorial-")
        print("After a turn you can then sell your made products to waiting customers.")
        print("Sell both of your product1 to these customers.")
        print()

    print()
    print("Time to sell products:")
    print()
    print("You have: ")
    print()
    print(" - ", product1, " of product1")
    print(" - ", product2, " of product2")
    print(" - ", product3, " of product3")

    for g in range(len(customers)):
        print()
        print("One customer wants a ", customers[c])
        print("What would you like to do?")
        print()
        print(" - sell a ", customers[c], " to them [1]")
        print(" - do not sell to them yet [2]")
        print(" - dismiss them from the shop without serving them [3]")
        validSellChoice = False

        while validSellChoice == False:
            sellchoice = int(input("> "))
            # TODO: Handle incorrect input, e.g.:
            # try / except / exception ValueError etc.

            if sellchoice == 1:

                if customers[c] == "product1":
                    
                    if product1 >= 1:
                        product1 = product1 - 1
                        money = money + 50
                        print("Money now: ", money)
                        print()
                        validSellChoice = True

                    else:
                        print("sorry, you do not have enough product1.")
                        print()
                        print("Please enter [2, 3]")
                        print()

                elif customers[c] == "product2":

                    if product2 >= 1:
                        product2 = product2 - 1
                        money = money + 100
                        print("Money now: ", money)
                        print()
                        validSellChoice = True

                    else:
                        print("sorry, you do not have enough product2.")
                        print()
                        print("Please enter [2, 3]")
                        print()

                elif customers[c] == "product3":

                    if product3 >= 1:
                        product3 = product3 - 1
                        money = money + 150
                        print("Money now: ", money)
                        print()
                        validSellChoice = True

                    else:
                        print("sorry, you do not have enough product3.")
                        print()
                        print("Please enter [2, 3]")
                        print()

            elif sellchoice == 2:
                print()
                validSellChoice = True

            elif sellchoice == 3:
                print()
                customers.remove(c)
                validSellChoice = True

            else:
                print("Invalid. Please enter [1, 2, 3]")

    if fullturn == 1:
        print()
        print("-Tutorial-")
        print("Congratulations! you have now completed the tutorial!")
        print("Enjoy my game! :)")
        print()

    print()
    print()
    print("-------------------------------------------------------")
    time.sleep(4)
    print()
    print()