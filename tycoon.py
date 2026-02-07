
#Tycoon

#importing packages
import random
import time

# ---------------- Customer names ----------------

COMMON_NAMES = [
    "Alex", "Jamie", "Sam", "Taylor", "Jago",
    "Chris", "Morgan", "Riley", "Casey", "Avery",
    "Bob", "Timothy", "Jerry", "Tom", "Polly",
    "Anthony", "Thomas", "Amelia", "Olive", "Liam",
    "Alex", "Steve", "Mia", "Summer", "Daniel", "Guy"
    
]

VIP_NAMES = [
    "Victoria", "Sebastian", "Alexander", "Isabella",
    "Theodore", "Charlotte", "Charles", "Royal Reubus", "King Jordus",
    "Lord Jensus", "Admiral Atticus", "Duke Deacus", "Reverend Rupert"
]

IMPATIENT_NAMES = [
    "Brad", "Kyle", "Derek", "Tina", "Sharon", "Eden",
    "Dolly", "Darren"
]

BULK_NAMES = [
    "Warehouse Inc.", "BigBuy Ltd.", "MegaMart Rep",
    "Wholesale Co.", "BulkBuyer LLC"
]

# ---------------- Colours ----------------
RESET = "\033[0m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
DEFAULT = "\033[39m"
BRONZE = "\033[38;5;130m"
SILVER = "\033[90m"
GOLD = "\033[38;5;178m"
PLATINUM = "\033[38;5;178m"


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

possibleActions = []
validAction = False

possibleCustomerWants = []
customers_this_turn = 2
vip_served = 0
non_vip_served = 0

switch_price = 50
xbox_price = 100
playstation_price = 150

switchGenerators = []
xboxGenerators = []
playstationGenerators = []
genProduction = 1
switch_maintainance = 10
xbox_maintainance = 15
playstation_maintainance = 20

generators_active = True
active_event = None
event_turns_left = 0

shop_staff = 2
staff_base_cost = 50
manufacturing_staff = 0
staff = shop_staff
manufacturing_base_cost = 50
marketing_staff = 0
marketing_base_cost = 75

switch_min = 20
switch_max = 90
xbox_min = 50
xbox_max = 160
playstation_min = 100
playstation_max = 215

GOAL_COST = 1800
GOAL_NAME = "Platinum Superstore Trophy"
game_won = False
awards = {
    "bronze": False,
    "silver": False,
    "gold": False,
    "platinum": False
}

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


def createCustomer(force_type=None):
    getCustomerWants()

    #normal chances based off rep.
    vip_weight = max(5, reputation // 5)
    impatient_weight = max(5, (100 - reputation) // 4)
    bulk_weight = 10

    # marketing affects it though!
    vip_weight += marketing_staff * 4
    bulk_weight += marketing_staff * 2

    #cap on chance(We don't want it to go TOO high!!!)
    vip_weight = min(vip_weight, 60)
    bulk_weight = min(bulk_weight, 35)

    if force_type == "normal":
        customer_type = "normal"

    elif force_type == "impatient":
        customer_type = "impatient"

    else:
        customer_type = random.choices(
            ["normal", "impatient", "vip", "bulk"],
            weights=[
                60,
                impatient_weight,
                vip_weight,
                bulk_weight
                ]
        )[0]
    
    if customer_type == "impatient":
        patience = random.randint(1,2)

    elif customer_type == "vip":
        patience = random.randint(3,5)
    
    elif customer_type == "bulk":
        patience = random.randint(2, 3)
    
    elif customer_type == "normal":
        if fullturn == 0:
            patience = random.randint(3,5)
        else:
            patience = random.randint(2,4)

    bulk_amount = 1
    if customer_type == "bulk":
        bulk_amount = random.randint(2, 3)

    name = getCustomerName(customer_type)


    return{
        "name": name,
        "want": possibleCustomerWants[random.randint(0, len(possibleCustomerWants) - 1)],
        "patience": patience,
        "type": customer_type,
        "amount": bulk_amount
    }


def addCustomer():
    global customers, active_event

    if active_event == "sale" and random.random() < 0.8:
        customer = createCustomer("impatient")
        customers.append(customer)
    else:
        customers.append(createCustomer())

def getCustomerName(customer_type):
    pool = COMMON_NAMES.copy()

    if customer_type == "vip":
        pool += VIP_NAMES
    elif customer_type == "impatient":
        pool += IMPATIENT_NAMES
    elif customer_type == "bulk":
        pool += BULK_NAMES

    return random.choice(pool)


def prependPlusSign(number):
    if number >=0:
        newnum = str(number)
        return "+" + newnum

    else:
        return str(number)


def clampReputation():
    global reputation
    if awards["platinum"] == True:
        if reputation > 125:
            reputation = 125
        elif reputation < 5:
            reputation = 5
    else:
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
        return 100 * manufacturing_staff

def getShopStaffCost():
    #price: 1st: 50, 2nd: 100, 3rd: 200, 4th: 300, 5th: 400.
    if shop_staff == 2:
        return 50
    
    elif shop_staff == 3:
        return 100
    
    else:
        return 100 * (shop_staff - 2)

def getCraftTime():
    base_craft_time = 6
    return max(1, base_craft_time - manufacturing_staff)

def getMarketingStaffCost():
    #price: 1st: 75, 2nd: 150, 3rd: 300, 4th: 450...
    if marketing_staff == 0:
        return 75
    elif marketing_staff == 1:
        return 150
    else:
        return 150 * marketing_staff



def canBuyGoal():
    return (
        money >= GOAL_COST and
        vip_served >= 5 and
        non_vip_served >= 20 and
        len(switchGenerators) >= 1 and
        len(xboxGenerators) >= 1 and
        len(playstationGenerators) >= 1 and
        shop_staff >= 4 and
        manufacturing_staff >= 1 and
        marketing_staff >= 1 and
        reputation >= 80
    )

def canBuyBronze():
    if money >= 300 and reputation >= 50 and vip_served >= 1 and non_vip_served >= 5:

        return True

def canBuySilver():
    if money >= 800 and reputation >= 60 and vip_served >= 2 and staff >= 1 and non_vip_served >= 10:
        return True

def canBuyGold():
    if money >= 1200 and reputation >= 70 and vip_served >= 3 and shop_staff >= 3 and manufacturing_staff >= 1 and marketing_staff >= 1 and  non_vip_served >= 15:
        return True

def canBuyPlatinum():
    if canBuyGoal():
        return True

def canBuyAward():
    if canBuyBronze == True:
        return True
    elif canBuySilver == True:
        return True
    elif canBuyGold == True:
        return True
    elif canBuyPlatinum == True:
        return True
    else:
        return False

def applyAwardBuff(tier):
    global reputation, shop_staff

    if tier == "bronze":
        reputation += 10
        shop_staff += 1

    elif tier == "silver":
        reputation += 15
        if not getCraftTime() == 1:
            manufacturing_staff += 1

    elif tier == "gold":
        reputation += 20
        marketing_staff += 1
        genProduction = 2
    
    elif tier == "platinum":
        reputation+= 30
        marketing_staff += 2
        shop_staff += 2
        if not getCraftTime() in (1, 2):
            manufacturing_staff += 2
        genProduction = 3

    clampReputation()




#other vars

customers = [createCustomer("normal"), createCustomer("normal")]



#---------------------------------------start game loop--------------------------------------------------

print()
print(CYAN+"Tycoon game V26.08.07"+RESET)
print()
print()
print(BLUE+"-Tutorial-"+RESET)
print(BLUE+"Welcome to my tycoon game!"+RESET)
print(BLUE+"I'll be teaching you how to play for your first turn!"+RESET)
print(BLUE+"Now, without further ado lets get going! :)"+RESET)
print()

while not game_won:
    #before turn setup:

    fullturn += 1
    for customer in customers[:]:
        customer["patience"] -= 1

        if customer["patience"] <= 0:
            print(RED+" 🌩️ ", customer['name'], "(", customer['type'], ") stormed out of the shop! 🌩️"+RESET)

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
    if active_event is None and fullturn > 1:
        roll = random.randint(1, 30)

        if roll == 1:
            active_event = "shortage"
            event_turns_left = random.randint(3, 4)
            print(RED+"⚠ Supply shortage! Production halved. ⚠"+RESET)

        elif roll == 2:
            active_event = "sale"
            event_turns_left = random.randint(3, 4)
            print(GREEN+"🔥 Sale day! Crowds flood the shop! 🔥"+RESET)
        
        elif roll == 3:
            active_event = "journalist"
            event_turns_left = random.randint(3, 4)
            print(YELLOW+" 🗞️ A jouralist enters the shop. They will interview your customers. 🗞️"+RESET)
        
        print()

    orig_switches = switch
    orig_xboxes = xbox
    orig_playstations = playstation
    orig_money = money

    #-------------maintenenance & generator related stuff--------------

    if fullturn % 3 == 2:
        print()
        if generators_active:
            print(YELLOW+"⚠ Maintenance is due tomorrow. Make sure you have enough money! ⚠"+RESET)
            
        else:
            print(RED+"⚠ Maintenance is due tomorrow, and your generators are already offline! ⚠"+RESET)

    print()

    if fullturn % 3 == 1 and not fullturn == 1:
        switch_price = switch_price + random.randint(-10,10)
        xbox_price = xbox_price + random.randint(-10,10)
        playstation_price = playstation_price + random.randint(-10,10)
        switch_price = round(switch_price / 5) * 5
        xbox_price = round(xbox_price / 5) * 5
        playstation_price = round(playstation_price / 5) * 5
        customers_this_turn = customers_this_turn + 1

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
            print(GREEN+"You managed to pay overdue maintenance!")
            print("Generators are back online."+RESET)

    if fullturn % 3 == 0:
        base_maintenance = (
        len(switchGenerators) * switch_maintainance +
        len(xboxGenerators) * xbox_maintainance +
        len(playstationGenerators) * playstation_maintainance
        )

        modifier = getMaintenanceModifier()
        maintenance = int(base_maintenance * modifier)

        print()
        print(YELLOW+"Maintenance day!"+RESET)
        print(YELLOW+"Cost of maintenance: ", maintenance, "c."+RESET)

        if money >= maintenance:
            money -= maintenance
            generators_active = True
            print(GREEN+"Maintenance paid. Generators operational"+RESET)
        
        else:
            generators_active = False
            print(RED+"⚠You cannot afford to pay the maintenance fee!⚠"+RESET)
            print(RED+"⚠Generators will shut down until the payment is made.⚠"+RESET)
            print()

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
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"Before a turn you will be notified of how many customers are waiting and what they want."+RESET)
        print(BLUE+"These ones both want a switch."+RESET)
        print()
    
    print(YELLOW+"Customers waiting", len(customers), ":" +RESET)

    for i, customer in enumerate(customers):
        row_color = DEFAULT if i % 2 == 0 else CYAN

        amount = customer.get("amount", 1)
        print()
        print(
            row_color+" [", i, "] ", customer['name'], " (",
            customer['type'], ") wants",
            amount, customer['want'], "((e)s).",
            "They will wait ", customer['patience'], " more turns."+RESET)

    print()
    print(DEFAULT+"Currently, you have:"+RESET)
    print()
    print(DEFAULT+" - ",  switch, " switch(es)"+RESET)
    print(CYAN+" - ", xbox, " xbox(es)"+RESET)
    print(DEFAULT+" - ", playstation, " playstation(s)"+RESET)
    print()
    print(DEFAULT+"Currently, the generators you have are:"+RESET)
    print(DEFAULT+" - ", len(switchGenerators), " switch generator(s)"+RESET)
    print(CYAN+" - ", len(xboxGenerators), " xbox generator(s)"+RESET)
    print(DEFAULT+" - ", len(playstationGenerators), " playstation generator(s)"+RESET)

    status = "ONLINE" if generators_active else "OFFLINE"
    color = GREEN if generators_active else RED

    print(color + "Generators status:", status +RESET)
    print()
    print(DEFAULT+"Shopkeeping staff:", shop_staff, "employees"+RESET)
    print(CYAN+"Customers you can serve per turn:", shop_staff, "."+RESET)
    print(DEFAULT+"Manufacturing staff:", manufacturing_staff, "."+RESET)
    print(CYAN+"Hand-craft time:",
        getCraftTime(), "seconds"+RESET)
    print(DEFAULT+"Marketing staff:", marketing_staff, "."+RESET)
    print(CYAN+"Effectiveness:", (marketing_staff + 1), "."+RESET)


          

    time.sleep(2)
    print()
    print(CYAN+"----------------------turn", fullturn, "begin-----------------------"+RESET)
    print()
    subturn = 1

    while subturn <= 3:

        time.sleep(1)
        print()
        print(CYAN+"----------------------subturn ", subturn, "------------------------"+RESET)
        print()

        if fullturn == 1:
            if subturn == 1:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Once your turn starts, you will then be asked what you want to do."+RESET)
                print(BLUE+"In each turn you will have three 'subturns'. In a subturn, if you wish,"+RESET)
                print(BLUE+"you can end your turn even if you have not used all three subturns."+RESET)
                print(BLUE+"This time, select 'buy generators'. Let's get a switch generator."+RESET)
                print()
            elif subturn == 2:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Now make a product by hand."+RESET)
                print()
            elif subturn == 3:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Once again make a product by hand."+RESET)
                print()

        #-----------------------------------------suturn------------------------------------------------
        getPossibleActions()
        print(DEFAULT+"Your money is: ", money, "c."+RESET)
        print()
        print(CYAN+"Choose an action category:"+RESET)
        print()
        if fullturn == 1:
            if subturn == 1:
                print(BLUE+" [1] Buy generators"+RESET)
                print(MAGENTA+" [2] Hand crafting"+RESET)
            else:
                print(MAGENTA+" [1] Buy generators"+RESET)
                print(BLUE+" [2] Hand crafting"+RESET)
        else:
            print(MAGENTA+" [1] Buy generators"+RESET)
            print(MAGENTA+" [2] Hand crafting"+RESET)
        if canBuyBronze() and not awards["bronze"]:
            print(BRONZE+" [3] Staff management"+RESET)
        elif canBuySilver() and not awards["silver"]:
            print(SILVER+" [3] Staff management"+RESET)
        elif canBuyGold() and not awards["gold"]:
            print(GOLD+" [3] Staff management"+RESET)
        elif canBuyPlatinum() and not awards["platinum"]:
            print(PLATINUM+" [3] Staff management"+RESET)
        else:
            print(MAGENTA+" [3] Staff management"+RESET)
        print()
        print(MAGENTA+" [0] End turn"+RESET)
        print()

        while True:
            try:
                print(MAGENTA+"What would you like to do? [0-3]"+RESET)
                choice = int(input(MAGENTA+"> "))
                if choice in (0, 1, 2, 3):
                    break
                else:
                    print(RED+"Please enter either [0, 1, 2, 3]."+RESET)

            except:
                print(RED+"Invalid. Please try again."+RESET)

        turnUsed = False
        if choice == 0:
            print()
            choice = 9
            validAction = False
            subturn = 4
            turnUsed = True

        if choice == 1:

                print()
                print(CYAN+"--- Buy Generators ---"+RESET)
                print()

                if fullturn == 1:
                    print(BLUE+"-Tutorial-"+RESET)
                    print(BLUE+"Buy a switch generator with your 100 coins."+RESET)
                    print(BLUE+"However, do note: every generator you buy equates to"+RESET)
                    print(BLUE+"more money added to the maintenance fee (in 3 turns)"+RESET)
                    print()

                if "get_switch_generator" in possibleActions:
                    if fullturn == 1:
                        print(BLUE+" [1] Switch generator - 100c"+RESET)
                    else:
                        print(GREEN+" [1] Switch generator - 100c"+RESET)
                else:
                    print(RED+" [1] Switch generator - 100c (too expensive)"+RESET)

                if "get_xbox_generator" in possibleActions:
                    print(GREEN+" [2] Xbox generator - 200c"+RESET)
                else:
                    print(RED+" [2] Xbox generator - 200c (too expensive)"+RESET)
                
                if "get_playstation_generator" in possibleActions:
                    print(GREEN+" [3] Playstation generator - 300c"+RESET)
                else:
                    print(RED+" [3] Playstation generator - 300c (too expensive)"+RESET)
                
                print()
                print(MAGENTA+" [0] Back"+RESET)
                print()

                while True:
                    try:
                        sub = int(input(MAGENTA+"> "))

                        if sub == 0:
                            break

                        if sub == 1:
                            if money >= 100:
                                switchGenerators.append("1")
                                money -= 100
                                print(GREEN+"Bought a switch generator."+RESET)
                                turnUsed = True
                                break
                            else:
                                print(RED+"You can't afford that."+RESET)
                        
                        elif sub == 2:
                            if money >= 200:
                                xboxGenerators.append("1")
                                money -= 200
                                print(GREEN+"Bought an xbox generator."+RESET)
                                turnUsed = True
                                break
                            else:
                                print(RED+"You can't afford that."+RESET)
                        
                        elif sub == 3:
                            if money >= 300:
                                playstationGenerators.append("1")
                                money -= 300
                                print(GREEN+"Bought a playstation generator."+RESET)
                                turnUsed = True
                                break
                            else:
                                print(RED+"You can't afford that."+RESET)
                    except:
                        print(RED+"Invalid. Please try again."+RESET)


        elif choice == 2:
            print()
            print(CYAN+"--- Hand Crafting ---"+RESET)
            print()

            if fullturn == 1:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Make a switch."+RESET)
                print()

            if "make_switch" in possibleActions:
                if fullturn == 1:
                    print(BLUE+" [1] One switch"+RESET)
                else:
                    print(GREEN+" [1] One switch"+RESET)
            
            else:
                print(RED+" [1] switch (requires generators)"+RESET)

            if "make_xbox" in possibleActions:
                print(GREEN+" [2] One xbox"+RESET)

            else:
                print(RED+" [2] xbox (requires generators)"+RESET)

            if "make_playstation" in possibleActions:
                print(GREEN+" [3] One playstation"+RESET)
            
            else:
                print(RED+" [3] playstation (requires generators)"+RESET)
            print()
            print(MAGENTA+" [0] Back"+RESET)
            print()

            while True:
                try:
                    productchoice = int(input(MAGENTA+"> "))
                    
                    if productchoice == 0:
                        break

                    elif productchoice not in (1, 2, 3):
                        print(RED+"Invalid. Please enter [0-3]"+RESET)
                        continue

                    craft_time = getCraftTime()
                    if active_event == "shortage":
                        craft_time += 3

                    if productchoice == 1 and "make_switch" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        switch += 1
                        print(GREEN+"You now have one more switch"+RESET)
                        turnUsed = True
                        break

                    elif productchoice == 2 and "make_xbox" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        xbox += 1
                        print(GREEN+"You now have one more xbox."+RESET)
                        turnUsed = True
                        break

                    elif productchoice == 3 and "make_playstation" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        playstation += 1
                        print(GREEN+"You now have one more playstation."+RESET)
                        turnUsed = True
                        break
                    
                    else:
                        print(RED+"You do not have the required generator yet."+RESET)
                        
                except:
                    print(RED+"Invalid. Please try again."+RESET)

            choice = 9
            validAction = False

        elif choice == 3:
            print()
            print(CYAN+"--- Staff Management ---"+RESET)
            print()

            shop_cost = getShopStaffCost()
            manu_cost = getManufacturingStaffCost()
            market_cost = getMarketingStaffCost()

            print(DEFAULT+"Shopkeeping staff:", shop_staff, "."+RESET)
            print(CYAN+"Manufacturing staff:", manufacturing_staff, "." +RESET)
            print(DEFAULT+"Marketing staff:", marketing_staff, "." +RESET)
            print()
            if money >= shop_cost:
                print(GREEN+" [1] Hire shopkeeping staff -", shop_cost, "c"+RESET)
            else:
                print(RED+" [1] Hire shopkeeping staff -", shop_cost, "c (too expensive)"+RESET)

            if getCraftTime() == 1:
                print(YELLOW+" [2] Hire manufacturing staff - MAXED OUT (craft time 1s)"+RESET)

            elif money >= manu_cost:
                print(GREEN+" [2] Hire manufacturing staff -", manu_cost, "c"+RESET)
            else:
                print(RED+" [2] Hire manufacturing staff -", manu_cost, "c (too expensive)"+RESET)
            
            if money >= market_cost:
                print(GREEN+" [3] Hire marketing staff -", market_cost, "c"+RESET)
            else:
                print(RED+" [3] Hire marketing staff -", market_cost, "c (too expensive)"+RESET)
            
            print()
            print(CYAN+"--- Trophies ---"+RESET)
            print()

            if not awards["bronze"] and canBuyBronze():
                print(BRONZE+" [6] Claim Bronze Shop Trophy"+RESET)           

            elif awards["bronze"] and not awards["silver"] and canBuySilver():
                    print(SILVER+" [7] Claim Silver Shop Trophy"+RESET)                

            elif awards["silver"] and not awards["gold"] and canBuyGold():
                        print(GOLD+" [8] Claim Gold Superstore Trophy"+RESET)             

            elif awards["gold"] and not awards["platinum"] and canBuyPlatinum():
                            print(PLATINUM+" [9] Claim Platinum Superstore Trophy"+RESET)
            
            else:
                print(RED+" No trophies to claim. :("+RESET)

            print()
            print(MAGENTA+" [0] Back"+RESET)
            print()
            
            while True:
                try:
                    sub = int(input(MAGENTA+"> "))

                    if sub == 0:
                        break

                    elif sub == 1:
                        if money >= shop_cost:
                            money -= shop_cost
                            shop_staff += 1
                            print(GREEN+"You hired a shopkeeping staff member!"+RESET)
                            turnUsed = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 2:
                        if getCraftTime() == 1:
                            print(YELLOW+"Your manufacturing process is already fully optimised."+RESET)
                        elif money >= manu_cost:
                            money -= manu_cost
                            manufacturing_staff += 1
                            print(GREEN+"You hired manufacturing staff!"+RESET)
                            turnUsed = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 3:
                        if money >= market_cost:
                            money -= market_cost
                            marketing_staff += 1
                            print(GREEN+"You hired marketing staff! More VIPs may shop here."+RESET)
                            turnUsed = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 6 and canBuyBronze() and not awards["bronze"]:
                        awards["bronze"] = True
                        applyAwardBuff("bronze")
                        print(BRONZE+"🏆 Bronze Shop Trophy earned!"+RESET)
                        print(BRONZE+"Reputation increased!"+RESET)
                        turnUsed = True
                        break

                    elif sub == 7 and canBuySilver() and awards["bronze"]:
                        awards["silver"] = True
                        applyAwardBuff("silver")
                        print(SILVER+"🏆 Silver Shop Trophy earned!"+RESET)
                        print(SILVER+"Extra shop staff hired for free!"+RESET)
                        turnUsed = True
                        break

                    elif sub == 8 and canBuyGold() and awards["silver"]:
                        awards["gold"] = True
                        applyAwardBuff("gold")
                        print(GOLD+"🏆 Gold Superstore Trophy earned!"+RESET)
                        print(GOLD+"Your shop is now famous!"+RESET)
                        turnUsed = True
                        break

                    elif sub == 9 and canBuyGoal():
                        awards["platinum"] = True
                        print()
                        print(PLATINUM+"🏆 CONGRATULATIONS! 🏆"+RESET)
                        print(PLATINUM+"You earned the " + GOAL_NAME + "!"+RESET)
                        print(PLATINUM+"Your shop is legendary!"+RESET)
                        print(PLATINUM+"Would you like to keep playing [1] or end the game? [0]"+RESET)
                        while True:
                            try:
                                endGame = int(input(PLATINUM+"> "))
                                if endGame == 0:
                                    print()
                                    print(PLATINUM+"WELL DONE!"+RESET)
                                    print(PLATINUM+"YOU HAVE BEATEN THE GAME!!!"+RESET)
                                    print(PLATINUM+"Farewell, master of business!"+RESET)
                                    print(PLATINUM+"I hope you have a nice time here!")
                                    print(PLATINUM+"Thanks for playing!"+RESET)
                                    print()
                                    game_won = True
                                    break
                                else:
                                    applyAwardBuff("platinum")
                                    print(PLATINUM+"I knew you'd stay, master of business!"+RESET)
                                    print(PLATINUM+"With this award you will receive many buffs!"+RESET)
                                    print(PLATINUM+"Enjoy your free play now!"+RESET)
                                    break
                            except:
                                print(RED+"That is invalid, master of business. Please try again")

                        print()
                        turnUsed = True
                        break

                    
                    else:
                        if canBuyAward:
                            print(RED+"Invalid. Please enter [0-3] or [6-9]."+RESET)
                        else:
                            print(RED+"Invalid. Please enter [0-3].")
                
                except:
                    print(RED+"Invalid. Please try again.")

        if turnUsed == True:
            subturn += 1
        if game_won == True:
            break

        staff = shop_staff + manufacturing_staff + marketing_staff

    if game_won == True:
        break


    #----------------------------------selling here------------------------------------------------------------------------------
    print()
    time.sleep(1)
    print(CYAN+"-----------------------turn end------------------------"+RESET)
    time.sleep(2)

    production_multiplier = 1

    if active_event == "shortage":
        production_multiplier = 0.5

    if generators_active:
        switch += (int(len(switchGenerators)* genProduction) * production_multiplier)
        xbox += (int(len(xboxGenerators)* genProduction) * production_multiplier)
        playstation += (int(len(playstationGenerators) * genProduction) * production_multiplier)
    
    else:
        print(RED+"⚠Your generators are inactive so could not produce products this turn.⚠"+RESET)

    if fullturn == 1:
        print()
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"After a turn you can then sell your made products to waiting customers."+RESET)
        print(BLUE+"Sell two of your switches to these normal customers."+RESET)
        print(BLUE+"Some customers will occasionally have a different type such as vips who pay more."+RESET)
        print()

    print()
    print(DEFAULT+"Time to sell products:"+RESET)
    print()
    print(DEFAULT+"You have:"+RESET)
    print()
    print(CYAN+" - ", switch, " switch(es)"+RESET)
    print(DEFAULT+" - ", xbox, " xbox(es)"+RESET)
    print(CYAN+" - ", playstation, " playstation(s)"+RESET)

    customers.sort(
    key=lambda c: (
        c["type"] != "vip",     # VIPs first
        c["patience"]           # low patience first
    )
)

    if marketing_staff > 0:
        print(MAGENTA+"📣 Marketing campaign active (+",marketing_staff, " influence)📣"+RESET)

    print(DEFAULT+"Customers in shop:"+RESET)
    for i, customer in enumerate(customers):
        if fullturn == 1:
            row_color = BLUE if i % 2 == 0 else CYAN
        else:
            row_color = DEFAULT if i % 2 == 0 else CYAN

        amount = customer.get("amount", 1)
        print(
            row_color+" [", i, "] ", customer ['name'],
            "(" + customer['type'].capitalize() + ")", " wants: ",
            amount, customer['want'],
            "((e)s) they will wait ", customer['patience'], "turns."+RESET
        )
        if customer["patience"] == 1:
                print(RED+"⚠ This customer is about to leave! ⚠"+RESET)
        print()

    orig_sale_money = money

    customers_served = 0
    max_servesPerTurn = shop_staff
    if active_event == "sale":
        max_servesPerTurn = shop_staff + 3

    while customers_served < max_servesPerTurn and len(customers) > 0:
        print()
        print(MAGENTA+"You can serve ", max_servesPerTurn - customers_served, " more customer(s)."+RESET)
        print(MAGENTA+"Enter customer number to serve or -1 to stop serving."+RESET)

        try:
            choice = int(input(MAGENTA+">"))

            if choice == -1:
                break
            if not 0 <= choice < len(customers):
                print(RED+"Invalid customer number."+RESET)
                continue
            
            customer = customers[choice]
            want = customer["want"]
            amount = customer.get("amount", 1)

            #find base prices
            if want == "switch":
                if switch < amount:
                    print(RED+"You don't have enough switches!"+RESET)
                    continue
                base_price = switch_price
                switch -= amount
            
            elif want == "xbox":
                if xbox < amount:
                    print(RED+"You don't have enough xboxes!"+RESET)
                    continue
                base_price = xbox_price
                xbox -= amount

            elif want == "playstation":
                if playstation < amount:
                    print(RED+"You don't have enough playstations!"+RESET)
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

            if customer["type"] == "vip":
                vip_served += 1
            else:
                non_vip_served += 1


            print(
                GREEN+"Sold", amount, want, "((e)s) to",
                customer['name'], "(" + customer['type'] + ") for",
                total_price, "c."+RESET
            )


            customers.pop(choice)
            customers_served += 1

            # re display updated customer list
            if len(customers) > 0:
                print()
                print(DEFAULT+"Updated customers:"+RESET)
                for i, customer in enumerate(customers):
                    if fullturn == 1:
                        row_color = BLUE if i % 2 == 0 else CYAN
                    else:
                        row_color = DEFAULT if i % 2 == 0 else CYAN
                    amount = customer.get("amount", 1)
                    print(
                        row_color+" [", i, "] ", customer['name'],
                        "(" + customer['type'].capitalize() + ") wants:",
                        amount, customer['want'],
                        ". They will wait", customer['patience'], "turns."+RESET
                    )
                    if customer["patience"] == 1:
                        print(RED+"⚠ This customer is about to leave! ⚠"+RESET)
                    print()

        except:
            print(RED+"Error!"+RESET)

    #-----------------------------------summary--------------------------------------------------------------------
    print()
    print()
    print(CYAN+"-------------------------------------------------------"+RESET)
    time.sleep(2)
    print()
    print()
    if fullturn == 1:
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"After a turn you will receive a summary of that turn!"+RESET)
        print()
    print(DEFAULT+"Turn ", fullturn, " summary:"+RESET)
    print(CYAN+ prependPlusSign(int(switch - orig_switches)), " switch(es)"+RESET)
    print(DEFAULT+ prependPlusSign(int(xbox - orig_xboxes)), " xbox(es)"+RESET)
    print(CYAN+ prependPlusSign(int(playstation - orig_playstations)), " playstation(s)"+RESET)
    print(DEFAULT+"-", orig_money - orig_sale_money, " spent"+RESET)
    print(CYAN+"+", money - orig_sale_money, " sales"+RESET)

    print(DEFAULT+ prependPlusSign(int(money - orig_money)), " overall profit"+RESET)
    print()
    if awards["platinum"] == True:
        print(DEFAULT+"Shop reputation:", reputation, "/ 125"+RESET)
    else:
        print(DEFAULT+"Shop reputation:", reputation, "/ 100"+RESET)
    if reputation >= 100:
        print(PLATINUM+"Customers talk about your shop across the city!"+RESET)

    elif reputation >= 80 and reputation < 100:
        print(GREEN+"Your shop is well respected! VIPs love it here."+RESET)

    elif reputation <= 20:
        print(RED+"Your shop has a bad reputation… customers are more impatient."+RESET)
    
        
    
    print()
    print(DEFAULT+"Shop award rank:"+RESET)

    if awards["platinum"]:
        print(PLATINUM+"💎 Platinum Superstore Trophy — LEGENDARY SHOP 💎"+RESET)
        print(PLATINUM+"💎Well done on your big achievement!!!💎"+RESET)

    elif awards["gold"]:
        print(GOLD+"🥇 Gold Superstore Trophy — Elite business 🥇"+RESET)
        print(GOLD+"Platinum trophy requirements:"+RESET)
        print(GOLD+" -",GOAL_COST, "c")
        print(GOLD+" - Rep: 80 or more")

    elif awards["silver"]:
        print(SILVER+"🥈 Silver Shop Trophy — Growing success 🥈"+RESET)
        print(SILVER+"Gold trophy requirements:"+RESET)
        print(SILVER+" - 1200c")
        print(SILVER+" - Rep: 70 or more")

    elif awards["bronze"]:
        print(BRONZE+"🥉 Bronze Shop Trophy — On the rise 🥉"+RESET)
        print(BRONZE+"Silver trophy requirements:"+RESET)
        print(BRONZE+" - 800c")
        print(BRONZE+" - 60 rep")

    else:
        print(DEFAULT+"No trophies yet — keep building your shop!"+RESET)
        print(DEFAULT+"First trophy requirements:"+RESET)
        print(DEFAULT+" - 300 or more coins")
        print(DEFAULT+" - reputation of 50 or above"+RESET)
    



    if active_event is not None:
        event_turns_left -= 1

        if event_turns_left <= 0:
            if active_event == "sale":
                print(RED+"The sale has ended. Things return to normal."+RESET)
            elif active_event == "shortage":
                print(GREEN+"Supply lines restored. Production normalised."+RESET)
            elif active_event == "journalist":
                print(YELLOW+"The journalist has left your shop now."+RESET)

            active_event = None
    
    if fullturn == 1:
        print()
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"Well, I think thats about it. You know all you need to know."+RESET)
        print(BLUE+"It was nice teaching you but it's time you continue on your own!"+RESET)
        print(BLUE+"Enjoy my game! :)"+RESET)
        print()

    print()
    print()
    print(CYAN+"-------------------------------------------------------"+RESET)
    time.sleep(7)
    print()
    print()
