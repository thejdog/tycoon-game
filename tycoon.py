
#Tycoon

#importing packages
import random
import time

#some vars:

reputation = 50
fullturn = 0
subturn = 0
money = 100
orig_money = 0
orig_sale_money = 0
switch = 0
xbox = 0
playstation = 0
orig_playstations = 0
orig_switches = 0
orig_xboxes = 0
switchGenerators = []
xboxGenerators = []
playstationGenerators = []
possibleActions = []
validAction = False
possibleCustomerWants = []
customers_this_turn = 2
switch_price = 50
xbox_price = 100
playstation_price = 150
switch_maintainance = 5
xbox_maintainance = 10
playstation_maintainance = 15
generators_active = True
active_event = None
event_turns_left = 0
shop_staff = 2
staff_base_cost = 50
manufacturing_staff = 0
manufacturing_base_cost = 50
switch_min = 20
switch_max = 90
xbox_min = 50
xbox_max = 160
playstation_min = 100
playstation_max = 215

#------------------------------------------------subroutines----------------------------------------------

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
    
    if money >= getShopStaffCost():
        possibleActions.append("hire_staff")


def getCustomerWants():
    global possibleCustomerWants, switchGenerators, xboxGenerators, playstationGenerators

    possibleCustomerWants.clear()

    if "1" in switchGenerators:
        possibleCustomerWants.append("switch")
    
    if "1" in xboxGenerators:
        possibleCustomerWants.append("xbox")
    
    if "1" in playstationGenerators:
        possibleCustomerWants.append("playstation")
    
    if not "1" in switchGenerators and not "1" in xboxGenerators and not "1" in playstationGenerators:
        possibleCustomerWants.append("switch")

def createCustomer(type):
    getCustomerWants()

    vip_weight = max(5, reputation // 5)
    impatient_weight = max(5, (100 - reputation) // 4)

    if type == 1:
        customer_type = "normal"

    elif type == 2:
        customer_type = "impatient"

    else:
        customer_type = random.choices(
            ["normal", "impatient", "vip", "bulk"],
            weights=[
                60,
                impatient_weight,
                vip_weight,
                10
                ]
        )[0]
    
    if customer_type == "impatient":
        patience = random.randint(1,2)

    elif customer_type == "vip":
        patience = random.randint(3,5)
    
    elif customer_type == "bulk":
        patience = random.randint(2, 3)
    
    else:
        patience = random.randint(2,4)

    bulk_amount = 1
    if customer_type == "bulk":
        bulk_amount = random.randint(2, 3)

    return{
        "want": possibleCustomerWants[random.randint(0, len(possibleCustomerWants) - 1)],
        "patience": patience,
        "type": customer_type,
        "amount": bulk_amount
    }


def addCustomer():
    global customers, active_event

    if active_event == "sale" and random.random() < 0.8:
        customer = createCustomer(2)
        customers.append(customer)
    else:
        customers.append(createCustomer(0))

def prependPlusSign(number):
    if number >=0:
        newnum = str(number)
        return "+" + newnum

    else:
        return str(number)

def clampReputation():
    global reputation
    if reputation > 100:
        reputation = 100
    elif reputation < 0:
        reputation = 0
    
def clampPrice(price, min_price, max_price):
    return max(min_price, min(price, max_price))

    
def getMaintenanceModifier():
    # returns a maintainance cost payment multiplier
    # rep 0ish → 1.3x cost 🙁
    # rep 50 → 1.0x cost 😐
    # rep 100 → 0.7x cost 🙂
    return 1.3 - (reputation / 100) * 0.6

def getManufacturingStaffCost():
    #price of staff: 1st: 50, 2nd: 100, 3rd: 200, 4th: 300, 5th: 400.
    if manufacturing_staff == 0:
        return 50
    
    elif manufacturing_staff == 1:
        return 100
    
    else:
        return 100 * (manufacturing_staff)

def getShopStaffCost():
    #price of staff: 1st: 50, 2nd: 100, 3rd: 200, 4th: 300, 5th: 400.
    if shop_staff == 2:
        return 50
    
    elif shop_staff == 3:
        return 100
    
    else:
        return 100 * (shop_staff - 2)

def getCraftTime():
    base_craft_time = 6
    return max(1, base_craft_time - manufacturing_staff)



#other vars

customers = [createCustomer(1), createCustomer(1)]



#---------------------------------------start game loop--------------------------------------------------

print()
print("Tycoon game v1.06.1")
print()
print()

while True :
    #before turn setup:
    if fullturn % 5 == 3:
        customers_this_turn = customers_this_turn + 1

    fullturn += 1
    for customer in customers[:]:
        customer["patience"] -= 1

        if customer["patience"] <= 0:
            print("\033[31mA customer stormed out of the shop!\033[0m")

            orig_reputation = reputation
            if customer["type"] == "vip":
                reputation -= 10

            elif customer["type"] == "impatient":
                reputation -= 3

            else:
                reputation -= 5
            
            if active_event == "journalist":
                reputation-= orig_reputation - reputation
            clampReputation()
            customers.remove(customer)
    
        # roll 'dice' for new event ONLY if no events are already active
    if active_event is None:
        roll = random.randint(1, 30)

        if roll == 1:
            active_event = "shortage"
            event_turns_left = random.randint(3, 4)
            print("\033[31m⚠ Supply shortage! Production halved. ⚠\033[0m")

        elif roll == 2:
            active_event = "sale"
            event_turns_left = random.randint(3, 4)
            print("\033[32m🔥 Sale day! Crowds flood the shop! 🔥\033[0m")
        
        elif roll == 3:
            active_event = "journalist"
            event_turns_left = random.randint(3, 4)
            print("\033[33mA jouralist enters the shop. They will interview your customers.\033[0m")

    orig_switches = switch
    orig_xboxes = xbox
    orig_playstations = playstation
    orig_money = money

    #-------------maintenenance & generator related stuff--------------

    if fullturn % 3 == 2:
        print()
        if generators_active:
            print("\033[33m⚠ Maintenance is due tomorrow. Make sure you have enough money! ⚠\033[0m")
        else:
            print("\033[31m⚠ Maintenance is due tomorrow, and your generators are already offline! ⚠\033[0m")


    if fullturn % 3 == 1:
        switch_price = switch_price + random.randint(-10,10)
        xbox_price = xbox_price + random.randint(-10,10)
        playstation_price = playstation_price + random.randint(-10,10)

        switch_price = clampPrice(switch_price, switch_min, switch_max)
        xbox_price = clampPrice(xbox_price, xbox_min, xbox_max)
        playstation_price = clampPrice(playstation_price, playstation_min, playstation_max)

    if not generators_active:
        base_maintenance = (
            len(switchGenerators) * switch_maintainance +
            len(xboxGenerators) * xbox_maintainance +
            len(playstationGenerators) * playstation_maintainance
        )

        maintenance = int(base_maintenance * getMaintenanceModifier())

        if money >= maintenance:
            money -= maintenance
            generators_active = True
            print("\033[32mYou managed to pay overdue maintenance!")
            print("Generators are back online.\033[0m")

    if fullturn % 3 == 0:
        base_maintenance = (
        len(switchGenerators) * switch_maintainance +
        len(xboxGenerators) * xbox_maintainance +
        len(playstationGenerators) * playstation_maintainance
        )

        modifier = getMaintenanceModifier()
        maintenance = int(base_maintenance * modifier)

        print()
        print("\033[31mMaintenance day!")
        print("\033[34mCost of maintenance: ", maintenance, "c.\033[0m")

        if money >= maintenance:
            money -= maintenance
            generators_active = True
            print("\033[32mMaintenance paid. Generators operational\033[0m")
        
        else:
            generators_active = False
            print("\033[31m⚠You cannot afford to pay the maintenance fee!⚠")
            print("\033[31m⚠Generators will shut down until the payment is made.⚠\033[0m")

    #----------------------before turn stuff------------------------

    subturn = 0
    if active_event == "sale":
        if len(customers) < (customers_this_turn + 3):
            for b in range((customers_this_turn + 3) - len(customers)):
                addCustomer()
    else:
        if len(customers) < customers_this_turn:
            for b in range(customers_this_turn - len(customers)):
                addCustomer()

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mBefore a turn you will be notified of how many customers are waiting and what they want.\033[0m")
        print("\033[35mThese ones both want a switch.\033[0m")
        print()
    
    print("\033[31mCustomers waiting: ", len(customers), "\033[0m")

    for customer in customers:
        amount = customer.get("amount", 1)
        print()
        print(
            "\033[34m", customer['type'], " customer wants ",
            amount, customer['want'], "((e)s).",
            "They will wait ", customer['patience']," more turn(s).\033[0m")

    print()
    print("\033[34mCurrently, you have:\033[0m")
    print()
    print("\033[34m", switch, " switch(es)\033[0m")
    print("\033[34m", xbox, " xbox(es)\033[0m")
    print("\033[34m", playstation, " playstation(s)\033[0m")
    print()
    print("\033[34mCurrently, the generators you have are:")
    print(len(switchGenerators), " switch generator(s)")
    print(len(xboxGenerators), " xbox generator(s)")
    print(len(playstationGenerators), " playstation generator(s)")

    status = "ONLINE" if generators_active else "OFFLINE"
    color = "\033[32m" if generators_active else "\033[31m"

    print(color + "Generators status:", status + "\033[0m")
    print("\033[0m")
    print("\033[34mShop staff:", shop_staff, "employees\033[0m")
    print("\033[34mCustomers you can serve per turn:", shop_staff, "\033[0m")
    print("\033[34mManufacturing staff:", manufacturing_staff, "\033[0m")
    print("\033[34mHand-craft time:",
        getCraftTime(), "seconds\033[0m")


          

    time.sleep(2)
    print()
    print("\033[32m----------------------turn begin-----------------------\033[0m")
    print()
    subturn = 1

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

        #-----------------------------------------suturn------------------------------------------------
        getPossibleActions()
        print("\033[34mYour money is: ", money, ".\033[0m")
        print()
        print("\033[34mChoose an action category:\033[0m")
        print()
        print("\033[32m[1] Buy generators\033[0m")
        print("\033[32m[2] Hand crafting\033[0m")
        print("\033[32m[3] Staff management\033[0m")
        print()
        print("\033[33m[0] End turn\033[0m")

        try:
            print("\033[36mWhat would you like to do? [0-3]\033[0m")
            choice = int(input("\033[36m> "))
            if choice in (0, 1, 2, 3):
                print()
            else:
                print("\033[31mPlease enter either [0, 1, 2, 3].\033[0m")

        except:
            print("\033[31mInvalid. Please try again.\033[0m")


        if choice == 0:
            print()
            choice = 9
            validAction = False
            subturn = 4

        if choice == 1:
                print()
                print("\033[34m--- Buy Generators ---\033[0m")
                print()

                if "get_switch_generator" in possibleActions:
                    print("\033[32m[1] Switch generator - 100c\033[0m")
                else:
                    print("\033[31m[1] Switch generator - 100c (too expensive)\033[0m")

                if "get_xbox_generator" in possibleActions:
                    print("\033[32m[2] Xbox generator - 200c\033[0m")
                else:
                    print("\033[31m[2] Xbox generator - 200c (too expensive)\033[0m")
                
                if "get_playstation_generator" in possibleActions:
                    print("\033[32m[3] Playstation generator - 300c\033[0m")
                else:
                    print("\033[31m[3] Playstation generator - 300c (too expensive)\033[0m")
                
                print("\033[33m[0] Back\033[0m")

                sub = int(input("\033[36m> "))

                if sub == 1 and money >= 100:
                    switchGenerators.append("1")
                    money -= 100
                
                elif sub == 2 and money >= 200:
                    xboxGenerators.append("1")
                    money -= 200
                
                elif sub == 3 and money >= 300:
                    playstationGenerators.append("1")
                    money -= 300

        elif choice == 2:
            print()
            print("\033[34m--- Hand Crafting ---\033[0m")

            if fullturn == 1:
                print()
                print("\033[35m-Tutorial-\033[0m")
                print("\033[35mMake a switch.\033[0m")
                print()

            print("\033[34mYou can make:\033[0m")
            if "make_switch" in possibleActions:
                print("\033[32m [1] One switch [1]\033[0m")
            
            else:
                print("\033[31m [1] switch (requires generators)\033[0m")

            if "make_xbox" in possibleActions:
                print("\033[32m [2] One xbox [2]\033[0m")

            else:
                print("\033[31m [2] xbox (requires generators)\033[0m")

            if "make_playstation" in possibleActions:
                print("\033[32m [3] One playstation [3]\033[0m")
            
            else:
                print("\033[31m [3] playstation (requires generators)\033[0m")
            print()
            print("\033[33[33m [0] Back\033[0m")

            try:
                productchoice = int(input("\033[36m> "))

                craft_time = getCraftTime()

                if active_event == "shortage":
                    craft_time += 3

                if productchoice == 1 and "make_switch" in possibleActions:
                    print("\033[33mmaking product...\033[0m")
                    time.sleep(craft_time)
                    print("\033[32mYou now have one more switch\033[0m")
                    switch = switch + 1

                elif productchoice == 2 and "make_xbox" in possibleActions:
                    print("\033[33mmaking product...\033[0m")
                    time.sleep(craft_time)
                    print("\033[32mYou now have one more xbox.\033[0m")
                    xbox = xbox + 1

                elif productchoice == 3 and "make_playstation" in possibleActions:
                    print("\033[33mmaking product...\033[0m")
                    time.sleep(craft_time)
                    print("\033[32mYou now have one more playstation.\033[0m")
                    playstation = playstation + 1

                elif productchoice > 3:
                    print("\033[31mInvalid. please enter [0-3]\033[0m")

                elif choice == (1 or 2 or 3) and not ("make_playstation" or "make_xbox" or "make_switch") in possibleActions:
                    print("\033[31mYou do not have a generator for this product yet so therefore cannot create one yourself.\033[0m")
                    print("Please enter a product you can make.")
            except:
                print("\033[31mInvalid. Please try again.\033[0m")

            choice = 9
            validAction = False

        elif choice == 3:
            print()
            print("\033[34m--- Staff Management ---\033[0m")
            print()

            shop_cost = getShopStaffCost()
            manu_cost = getManufacturingStaffCost()

            print("\033[34mShopkeeping staff:", shop_staff, "\033[0m")
            print("\033[34mManufacturing staff:", manufacturing_staff, "\033[0m")
            print()
            if money >= shop_cost:
                print("\033[32m[1] Hire shopkeeping staff -", shop_cost, "c\033[0m")
            else:
                print("\033[31m[1] Hire shopkeeping staff -", shop_cost, "c (too expensive)\033[0m")

            if getCraftTime() == 1:
                print("\033[32m[2] Hire manufacturing staff - MAXED OUT (craft time 1s)\033[0m")

            elif money >= manu_cost:
                print("\033[32m[2] Hire manufacturing staff -", manu_cost, "c\033[0m")
            else:
                print("\033[31m[2] Hire manufacturing staff -", manu_cost, "c (too expensive)\033[0m")
            
            print("\033[33m[0] Back\033[0m")
                
            sub = int(input("\033[36m> "))
            if sub == 1 and money >= shop_cost:
                money -= shop_cost
                shop_staff += 1
                print("\033[32mYou hired a shopkeeping staff member!\033[0m")
            
            elif sub == 2:
                if getCraftTime() == 1:
                    print("\033[31mYour manufacturing process is already fully optimised.\033[0m")
                elif money >= manu_cost:
                    money -= manu_cost
                    manufacturing_staff += 1
                    print("\033[32mYou hired manufacturing staff!\033[0m")
                else:
                    print("\033[31mYou can't afford that.\033[0m")


    #----------------------------------selling here------------------------------------------------------------------------------
    print()
    time.sleep(1)
    print("\033[31m-----------------------turn end------------------------\033[0m")
    time.sleep(2)

    production_multiplier = 1

    if active_event == "shortage":
        production_multiplier = 0.5

    if generators_active:
        switch += int(len(switchGenerators) * production_multiplier)
        xbox += int(len(xboxGenerators) * production_multiplier)
        playstation += int(len(playstationGenerators) * production_multiplier)
    
    else:
        print("⚠Your generators are inactive so could not produce products this turn.⚠")

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mAfter a turn you can then sell your made products to waiting customers.\033[0m")
        print("\033[35mSell both of your switches to these customers.\033[0m")
        print("\033[35mSome customers will occasionally have a different type such as vips who pay more.")
        print()

    print()
    print("\033[34mTime to sell products:\033[0m")
    print()
    print("\033[34mYou have:\033[0m")
    print()
    print("\033[34m - ", switch, " switch(es)\033[0m")
    print("\033[34m - ", xbox, " xbox(es)\033[0m")
    print("\033[34m - ", playstation, " playstation(s)\033[0m")

    customers.sort(
    key=lambda c: (
        c["type"] != "vip",     # VIPs first
        c["patience"]           # low patience first
    )
)

    print("\033[34mCustomers in shop:")
    for i, customer in enumerate(customers):
        amount = customer.get("amount", 1)
        print(
            "\033[34m", customer ['type'].capitalize(), " customer No", i, " wants: ",
            amount, customer['want'],
            "((e)s) they will wait ", customer['patience'], "turns.\033[0m"
        )
        if customer["patience"] == 1:
                print("\033[31m⚠ This customer is about to leave! ⚠\033[0m")

    orig_sale_money = money

    customers_served = 0
    max_servesPerTurn = shop_staff
    if active_event == "sale":
        max_servesPerTurn = shop_staff + 3

    while customers_served < max_servesPerTurn and len(customers) > 0:
        print()
        print("\033[34mYou can serve ", max_servesPerTurn - customers_served, " more customer(s).")
        print("\033[36mEnter customer number to serve or -1 to stop serving.\033[0m")

        try:
            choice = int(input("\033[36m>"))

            if choice == -1:
                break
            if choice < 0 or choice >= len(customers):
                print("Invalid customer number.")
                continue
            
            customer = customers[choice]
            want = customer["want"]
            amount = customer.get("amount", 1)

            #find base prices
            if want == "switch":
                if switch < amount:
                    print("\033[31mYou don't have enough switches!")
                    continue
                base_price = switch_price
                switch -= amount
            
            elif want == "xbox":
                if xbox < amount:
                    print("\033[31mYou don't have enough xboxes!")
                    continue
                base_price = xbox_price
                xbox -= amount

            elif want == "playstation":
                if playstation < amount:
                    print("\033[31mYou don't have enough playstations!")
                    continue
                base_price = playstation_price
                playstation -= amount
            
            #here is the base total price, code!
            total_price = base_price * amount

            #don't forget to add type multipliers
            if customer["type"] == "vip":
                total_price = int(total_price * 1.4)

            elif customer["type"] == "impatient":
                total_price = int(total_price * 0.9)
            
            elif customer['type'] == "bulk":
                #you get a ten percent discount, bulky guys!!!
                total_price = int(total_price * 0.9)

            elif customer['type'] == "normal":
                #reputation affects price!!!
                total_price = int(total_price * (0.8 + (reputation / 100) * 0.4))

            money += total_price
            orig_reputation = reputation
            if customer['type'] == "normal":
                reputation += random.randint(1,3)
            
            elif customer['type'] == "impatient":
                reputation += random.randint(0,1)

            elif customer['type'] == "vip":
                reputation += random.randint(3,6)
            
            elif customer['type'] == "bulk":
                reputation += random.randint(1,3)

            if active_event == "journalist":
                reputation += reputation - orig_reputation
            clampReputation()

            print("Sold ", amount, want, "((e)s) to ", customer['type'], " customer for ", total_price, "c.")

            customers.pop(choice)
            customers_served += 1

        except:
            print("\033[31mError!\033[0m")

    if fullturn == 1:
        print()
        print("\033[35m-Tutorial-\033[0m")
        print("\033[35mCongratulations! You have now completed the tutorial!\033[0m")
        print("\033[35mEnjoy my game! :)\033[0m")
        print()

    #-----------------------------------summary--------------------------------------------------------------------
    print()
    print()
    print("\033[33m-------------------------------------------------------\033[0m")
    time.sleep(2)
    print()
    print()
    print("Turn ", fullturn, " summary:")
    print("+", switch - orig_switches, " switch(es)")
    print("+", xbox - orig_xboxes, " xbox(es)")
    print("+", playstation - orig_playstations, " playstation(s)")
    print("-", orig_money - orig_sale_money, " spent")
    print("+", money - orig_sale_money, " sales")

    print(prependPlusSign(int(money - orig_money)), " overall profit")
    print()
    print("\033[35mShop reputation:", reputation, "/ 100\033[0m")
    if reputation >= 80:
        print("\033[32mYour shop is well respected! VIPs love it here.\033[0m")
    elif reputation <= 20:
        print("\033[31mYour shop has a bad reputation… customers are more impatient.\033[0m")


    if active_event is not None:
        event_turns_left -= 1

        if event_turns_left <= 0:
            if active_event == "sale":
                print("\033[33mThe sale has ended. Things return to normal.\033[0m")
            elif active_event == "shortage":
                print("\033[32mSupply lines restored. Production normalised.\033[0m")

            active_event = None


    print()
    print()
    print("\033[33m-------------------------------------------------------\033[0m")
    time.sleep(7)
    print()
    print()