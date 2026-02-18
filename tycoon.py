
#Tycoon

#importing packages
import random
import time

# ---------------- Customer names ----------------

COMMON_NAMES = [
    "Alex", "Jamie", "Sam", "Taylor", "Jago",
    "Chris", "Morgan", "Riley", "Casey",
    "Bob", "Timothy", "Jerry", "Tom", "Avery",
    "Anthony", "Thomas", "Liam", "Polly",
    "Alex", "Steve", "Mia", "Summer", "Guy"    
]

VIP_NAMES = [
     "Emperor Edus", "Lord Jensus", "Dictator Daniel",
     "Charles", "Royal Reubus", "King Jordus", "Officer Oliver",
     "Admiral Atticus", "Duke Deacus", "Reverend Rupert"
]

IMPATIENT_NAMES = [
    "Brad", "Kyle", "Derek", "Tina", "Sharon",
    "Dolly", "Darren", "Amelia"
]

BULK_NAMES = [
    "Warehouse Inc.", "BigBuy Ltd.", "MegaMart Rep",
    "Wholesale Co.", "BulkBuyer LLC"
]

GRAND_CUSTOMER_NAMES = [
    "The Console Collector",
    "The Grand Gamer",
    "The Hardware Hunter",
    "The Serious Speedrunner"
]

BARGAINER_NAMES = [
    "The negotiator",
    "Deal Hunter",
    "The bargainer",
    "The haggler"
]

SCAMMER_NAMES = [
    "michael",
    "daniel",
    "steve",
    "alex",
    "martin",
    "james",
    "robert"
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

# ------------------ Game State ------------------
game_state = {
    "money": 100,
    "Switch": 0,
    "Xbox": 0,
    "Playstation": 0,
    "SwitchGenerators": [],
    "XboxGenerators": [],
    "PlaystationGenerators": [],
    "Shop_staff": 2,
    "manufacturing_staff": 0,
    "marketing_staff": 0,
    "security_staff": 0,
    "reputation": 50,
    "customers": [],
    "awards": {"bronze": False, "silver": False, "gold": False, "platinum": False},
    "active_event": None,
    "event_turns_left": 0,
    "turnUsed": False,
    "game_won": False,
    "tutorial": False,
    "fullturn": 0,
    "vip_served": 0,
    "non_vip_served": 0
}

#some vars:

subturn = 0

orig_money = 0
orig_sale_money = 0

orig_Playstations = 0
orig_Switches = 0
orig_Xboxes = 0

possibleActions = []
validAction = False

possibleCustomerWants = []
customers_this_turn = 2

Switch_price = 50
Xbox_price = 100
Playstation_price = 150

genProduction = 1
Switch_maintainance = 10
Xbox_maintainance = 15
Playstation_maintainance = 20

generators_active = True

staff_base_cost = 50
staff = game_state["Shop_staff"]
manufacturing_base_cost = 50
marketing_base_cost = 75
effective_shop_staff = game_state["Shop_staff"]
effective_manufacturing_staff = game_state["manufacturing_staff"]
effective_marketing_staff = game_state["marketing_staff"]
effective_security_staff = game_state["security_staff"]

Switch_min = 20
Switch_max = 90
Xbox_min = 50
Xbox_max = 160
Playstation_min = 100
Playstation_max = 215

GOAL_COST = 2000
GOAL_NAME = "Platinum Superstore Trophy"
game_state["game_won"] = False


#------------------------------------------------subroutines----------------------------------------------

def getPossibleActions():
    global possibleActions, game_state
    possibleActions.clear()
    if game_state["money"] >= 100:
        possibleActions.append ("get_Switch_generator")

    if game_state["money"] >= 200 and len(game_state["SwitchGenerators"]) >=1:
        possibleActions.append ("get_Xbox_generator")

    if game_state["money"] >= 300 and len(game_state["XboxGenerators"]) >=1:
        possibleActions.append ("get_Playstation_generator")

    if len(game_state["SwitchGenerators"]) >= 1:
        possibleActions.append ("make_Switch")

    if len(game_state["XboxGenerators"]) >= 1:
        possibleActions.append ("make_Xbox")

    if len(game_state["PlaystationGenerators"]) >= 1:
        possibleActions.append ("make_Playstation")
    
    if game_state["money"] >= getShopStaffCost():
        possibleActions.append("hire_staff")

    if game_state["money"] >= getSecurityStaffCost():
        possibleActions.append("hire_security")




def getCustomerWants():
    global possibleCustomerWants, game_state

    possibleCustomerWants.clear()

    if len(game_state["SwitchGenerators"]) > 0:
        possibleCustomerWants.append("Switch")
    
    if len(game_state["XboxGenerators"]) > 0:
        possibleCustomerWants.append("Xbox")
    
    if len(game_state["PlaystationGenerators"]) > 0:
        possibleCustomerWants.append("Playstation")
    
    if len(possibleCustomerWants) == 0:
        possibleCustomerWants.append("Switch")


def createCustomer(force_type=None):
    getCustomerWants()

    #normal chances based off rep.
    vip_weight = max(5, game_state["reputation"] // 5)
    impatient_weight = max(5, (100 - game_state["reputation"]) // 4)
    bulk_weight = 10
    if game_state["fullturn"] >= 10 and game_state["reputation"] >=75:
        grand_weight = 5
    else:
        grand_weight = 0

    bargainer_weight = 15
    
    if game_state["fullturn"] >= 7 and not any(c["type"] == "scammer" for c in game_state["customers"]):
        base_scammer_weight = 7
    else:
        base_scammer_weight = 0

    #security staff - "Haha! I see you scammer!!! GET OUT OF THE SHOP!!!"
    scammer_weight = max(0, base_scammer_weight - (effective_security_staff * 2))

    # marketing affects it though!
    vip_weight += effective_marketing_staff * 5
    bulk_weight += effective_marketing_staff * 2
    if not grand_weight == 0:
        grand_weight += effective_marketing_staff
    bargainer_weight -= effective_marketing_staff

    #cap on chance (We don't want it to go TOO high!!!)
    vip_weight = min(vip_weight, 60)
    bulk_weight = min(bulk_weight, 30)
    grand_weight = min(grand_weight, 30)

    if force_type == "normal":
        customer_type = "normal"

    elif force_type == "impatient":
        customer_type = "impatient"

    else:
        customer_type = random.choices(
            ["normal", "impatient", "vip", "bulk", "grand", "bargainer", "scammer"],
            weights=[
                60,
                impatient_weight,
                vip_weight,
                bulk_weight,
                grand_weight,
                bargainer_weight,
                scammer_weight
                ]
        )[0]
    
    if customer_type == "impatient":
        patience = 1
        if game_state["fullturn"] == 0:
            patience += 1

    elif customer_type == "vip":
        patience = random.randint(3,4)
        if game_state["fullturn"] == 0:
            patience += 1
    
    elif customer_type == "bulk":
        patience = random.randint(2, 3)
        if game_state["fullturn"] == 0:
            patience += 1
    
    elif customer_type == "normal":  
        patience = random.randint(2,4)
        if game_state["fullturn"] == 0:
            patience += 1
    
    elif customer_type == "scammer":
        patience = random.randint(2,4)
    
    elif customer_type == "grand":
        patience = random.randint(3,5)
        if game_state["fullturn"] == 0:
            patience += 1
        bulk_amount = 1
    
    elif customer_type == "bargainer":
        patience = random.randint(8, 11)


    bulk_amount = 1
    if customer_type == "bulk":
        bulk_amount = random.randint(2, 4)
    
    offer_multiplier = 1
    if customer_type == "bargainer":
        offer_multiplier = (random.randint(6, 8) / 10)
    direction = 0
    if customer_type == "bargainer":
        direction = 1
    offer_cap = 1
    if customer_type == "bargainer":
        offer_cap = (1 + (random.randint(2,4) / 10)) + int(game_state["reputation"] / 80)

    name = getCustomerName(customer_type)

    if game_state["fullturn"] == 0:
        patience += 1


    if customer_type == "grand":
        want = "all"
        print(GOLD+"✨ ", name, " has entered the shop! ✨"+RESET)
    else:
        want = possibleCustomerWants[random.randint(0, len(possibleCustomerWants) - 1)]

    return{
        "name": name,
        "want": want,
        "patience": patience,
        "type": customer_type,
        "amount": bulk_amount,
        "multiplier": offer_multiplier,
        "direction": direction,
        "offer_cap": offer_cap
    }


def addCustomer():
    global game_state

    if game_state["active_event"] == "sale" and random.random() < 0.8:
        customer = createCustomer("impatient")
        game_state["customers"].append(customer)
    else:
        game_state["customers"].append(createCustomer())

def getCustomerName(customer_type):
    pool = COMMON_NAMES.copy()

    if customer_type == "vip":
        pool.clear()
        pool += VIP_NAMES
    elif customer_type == "impatient":
        pool.clear()
        pool += IMPATIENT_NAMES
    elif customer_type == "bulk":
        pool.clear()
        pool += BULK_NAMES
    elif customer_type == "grand":
        pool.clear()
        pool += GRAND_CUSTOMER_NAMES
    elif customer_type == "bargainer":
        pool.clear()
        pool += IMPATIENT_NAMES
        pool += BARGAINER_NAMES

    return random.choice(pool)


def prependPlusSign(number):
    if number >=0:
        newnum = str(number)
        return "+" + newnum

    else:
        return str(number)


def clampReputation():
    global game_state
    if game_state["awards"]["platinum"] == True:
        if game_state["reputation"] > 125:
            game_state["reputation"] = 125
        elif game_state["reputation"] < 5:
            game_state["reputation"] = 5
    else:
        if game_state["reputation"] > 100:
            game_state["reputation"] = 100
        elif game_state["reputation"] < 0:
            game_state["reputation"] = 0
    
def clampPrice(price, min_price, max_price):
    return max(min_price, min(price, max_price))

    
def getMaintenanceModifier():
    # returns a maintainance cost payment multiplier
    # rep 0ish → 1.3x cost 🙁
    # rep 50 → 1.0x cost 😐
    # rep 100 → 0.7x cost 🙂
    return 1.3 - (game_state["reputation"] / 100) * 0.6


def getManufacturingStaffCost():
    #price of staff: 1st: 50, 2nd: 100, 3rd: 250, 4th: 400, 5th: 550.
    if game_state["manufacturing_staff"] == 0:
        return 50
    
    elif game_state["manufacturing_staff"] == 1:
        return 100
    
    else:
        return (150 * game_state["manufacturing_staff"]) - 50

def getShopStaffCost():
    #price: 1st: 50, 2nd: 100, 3rd: 200, 4th: 300, 5th: 400...
    if game_state["Shop_staff"] == 2:
        return 50
    
    elif game_state["Shop_staff"] == 3:
        return 100
    
    else:
        temp =  100 * (game_state["Shop_staff"] - 2)
        if temp >= 500:
            temp = 500
        return temp

def getCraftTime():
    base_craft_time = 6
    return max(1, base_craft_time - effective_manufacturing_staff)

def getMarketingStaffCost():
    #price: 1st: 75, 2nd: 150, 3rd: 300, 4th: 450...
    if game_state["marketing_staff"] == 0:
        return 75
    elif game_state["marketing_staff"] == 1:
        return 150
    else:
        temp2 = 150 * game_state["marketing_staff"]
        if temp2 >= 600:
            temp2 = 600
        return temp2

def getSecurityStaffCost():
    # 1st: 80, 2nd: 160, 3rd: 300, 4th+: 500 cap
    if game_state["security_staff"] == 0:
        return 80
    elif game_state["security_staff"] == 1:
        return 160
    else:
        cost = 140 * game_state["security_staff"]
        if cost >= 500:
            cost = 500
        return cost




def canClaimGoal():
    return (
        game_state["money"] >= GOAL_COST and
        game_state["vip_served"] >= 5 and
        game_state["non_vip_served"] >= 20 and
        len(game_state["SwitchGenerators"]) >= 1 and
        len(game_state["XboxGenerators"]) >= 1 and
        len(game_state["PlaystationGenerators"]) >= 1 and
        game_state["Shop_staff"] >= 4 and
        game_state["manufacturing_staff"] >= 1 and
        game_state["marketing_staff"] >= 1 and
        game_state["reputation"] >= 100
    )

def canClaimBronze():
    if game_state["money"] >= 300 and game_state["reputation"] >= 50 and game_state["vip_served"] >= 1 and game_state["non_vip_served"] >= 5:

        return True

def canClaimSilver():
    if game_state["money"] >= 800 and game_state["reputation"] >= 65 and game_state["vip_served"] >= 2 and staff >= 3 and game_state["non_vip_served"] >= 10:
        return True

def canClaimGold():
    if game_state["money"] >= 1300 and game_state["reputation"] >= 80 and game_state["vip_served"] >= 3 and game_state["Shop_staff"] >= 3 and game_state["manufacturing_staff"] >= 1 and game_state["marketing_staff"] >= 1 and  game_state["non_vip_served"] >= 15:
        return True

def canClaimPlatinum():
    if canClaimGoal():
        return True

def canClaimAward():
    if canClaimBronze():
        return True
    elif canClaimSilver():
        return True
    elif canClaimGold():
        return True
    elif canClaimPlatinum():
        return True
    else:
        return False

def applyAwardBuff(tier):
    global game_state

    if tier == "bronze":
        game_state["reputation"] += 10
        game_state["Shop_staff"] += 1

    elif tier == "silver":
        game_state["reputation"] += 15
        if not getCraftTime() == 1:
            game_state["manufacturing_staff"] += 1

    elif tier == "gold":
        game_state["reputation"] += 20
        game_state["marketing_staff"] += 1
        genProduction = 2
    
    elif tier == "platinum":
        game_state["reputation"]+= 30
        game_state["marketing_staff"] += 2
        game_state["Shop_staff"] += 2
        if not getCraftTime() in (1, 2):
            game_state["manufacturing_staff"] += 2
        genProduction = 3

    clampReputation()

#----------
#---------------------------------------game loop--------------------------------------------------
#----------

print()
print(CYAN+"Tycoon game V26.12.00"+RESET)
print()
print(MAGENTA+"Would you like to have the tutorial for your first turn? [Yes - 1] [No - 2]"+RESET)
print()
while True:
    try:
        tutorialOnOff = int(input(MAGENTA+"> "))
        if tutorialOnOff == 1:
            game_state["tutorial"] = True
            break
        elif tutorialOnOff == 2:
            game_state["tutorial"] = False
            break
        else:
            print(RED+"Invalid. Please enter [1-2]."+RESET)
    except:
        print(RED+"Invalid. Please try again."+RESET)

if game_state["tutorial"] == True:
    print()
    print(BLUE+"-Tutorial active-"+RESET)
    print(BLUE+"💡 Tip: Professional customers usually write their names properly."+RESET)
    print()
    game_state["customers"] = [createCustomer("normal"), createCustomer("normal")]
else:
    print()
    print(BLUE+"-Tutorial inactive-"+RESET)
    print()
    game_state["customers"] = [createCustomer(), createCustomer()]

print()
print(CYAN+"-------------------------------------------------------"+RESET)
time.sleep(1)

while not game_state["game_won"]:
    #before turn setup:

    game_state["fullturn"] += 1
    for customer in game_state["customers"][:]:
        customer["patience"] -= 1

        if customer["patience"] <= 0:
            if customer["type"] == "scammer":
                cType = "normal"
            else:
                cType = customer["type"]
            print(RED+" 🌩️ ", customer['name'], "(", cType, ") stormed out of the shop! 🌩️"+RESET)

            orig_reputation = game_state["reputation"]
            if customer["type"] == "vip":
                game_state["reputation"] -= random.randint(6, 9)

            elif customer["type"] == "impatient":
                game_state["reputation"] -= random.randint(1,3)
            
            elif customer["type"] == "bargainer":
                game_state["reputation"] -= random.randint(1,2)

            else:
                game_state["reputation"] -= random.randint(4,6)
            
            if game_state["active_event"] == "journalist":
                game_state["reputation"]-= int((orig_reputation - game_state["reputation"]) * 0.5)
            clampReputation()
            game_state["customers"].remove(customer)
    
        if customer["type"] == "bargainer":
            step = 0.1
            customer["multiplier"] += step * customer["direction"]
            if customer["multiplier"] >= customer["offer_cap"]:
                customer["direction"] = -1
            
            elif customer["multiplier"] <= 0.5:
                customer["direction"] = 0
    
        # roll 'dice' for new event ONLY if no events are already active
    if game_state["active_event"] is None and not game_state["tutorial"] == True:
        roll = random.randint(1, 20)

        if roll == 1:
            game_state["active_event"] = "shortage"
            game_state["event_turns_left"] = random.randint(2, 4)
            print(RED+"⚠ Supply shortage! Production halved. ⚠"+RESET)

        elif roll == 2:
            game_state["active_event"] = "sale"
            game_state["event_turns_left"] = random.randint(2, 4)
            print(GREEN+"🔥 Sale day! Crowds flood the shop! 🔥"+RESET)
        
        elif roll == 3:
            game_state["active_event"] = "journalist"
            game_state["event_turns_left"] = random.randint(2, 4)
            print(YELLOW+" 🗞️  A jouralist enters the shop. They will interview your customers. 🗞️"+RESET)
        
        # ---- Cyber Attack Event Trigger (a bit different)----
        if game_state["fullturn"] > 4:
            base_chance = 0.10  # 10% base chance

            # security reduces risk
            reduced_chance = base_chance - (effective_security_staff * 0.015)

            # clamp so it never goes negative
            if reduced_chance < 0.02:
                reduced_chance = 0.02

            if random.random() < reduced_chance:
                game_state["active_event"] = "cyber_attack"
                if game_state["active_event"] == "cyber_attack":
                    print(RED + "⚠ CYBER ATTACK DETECTED! ⚠" + RESET)
                    print(RED + "Your generators have been hacked and shut down!" + RESET)
                    print(RED + "Encrypted files detected..." + RESET)
                    generators_active = False
                    product_down = random.randint(1,3)
                    fraction_lost = random.randint(15,30) / 100
                    if product_down == 1:
                        lost = int(game_state["Switch"] * fraction_lost)
                        game_state["Switch"] -= lost
                        product_name = "Switches"
                    elif product_down == 2:
                        lost = int(game_state["Xbox"] * fraction_lost)
                        game_state["Xbox"] -= lost
                        product_name = "Xboxes"
                    elif product_down == 3:
                        lost = int(game_state["Playstation"] * fraction_lost)
                        game_state["Playstation"] -= lost
                        product_name = "Playstations"
                    
                    print(RED + f"{lost} {product_down} corrupted and unsellable!" + RESET)
                    
                    ransom_cost = random.randint(250, 650)
                    print()
                    print(RED+f"Hackers demand {ransom_cost}c to restore your generators."+RESET)
                    print(RED+"Pay ransom? [Yes - 1] [No - 2]")
                    while True:
                        try:
                            pay = int(input(MAGENTA+"> "))
                            if pay == 1:
                                if game_state["money"] >= ransom_cost:
                                    game_state["money"] -= ransom_cost
                                    generators_active = True
                                    game_state["active_event"] = None
                                    print(GREEN + "Generators restored! Systems rebooting..." + RESET)
                                else:
                                    print(RED+ "You cannot afford the ransom!"+RESET)
                                    game_state["event_turns_left"] = random.randint(4,6)
                                break
                            elif pay == 2:
                                game_state["event_turns_left"] = random.randint(6,8)
                                print(RED+"You refuse to pay. Systems will restore in", game_state["event_turns_left"], "turns."+RESET)
                                break
                            else:
                                print(RED+"Invalid. Please enter [1 - 2]"+RESET)
                        except:
                            print(RED+"Invalid. Please try again"+RESET)
        if game_state["fullturn"] > 5:
            strike_chance = max(0, ((staff - 2) * 0.05))
            if random.random() < strike_chance:
                game_state["active_event"] = "strike"
                game_state["event_turns_left"] = random.randint(4,6)
                striking_staff = random.sample(["shop", "manufacturing", "marketing", "security"], k=random.randint(1,3))
                print(RED+"💢 Staff are going on strike! 💢"+RESET)
                print(RED+"Striking departments:", ", ".join(striking_staff)+RESET)
                print()
                print(RED+"You can pay them to end it immediately."+RESET)
                effective_shop_staff = game_state["Shop_staff"]
                effective_manufacturing_staff = game_state["manufacturing_staff"]
                effective_marketing_staff = game_state["marketing_staff"]
                effective_security_staff = game_state["security_staff"]

                if game_state["active_event"] == "strike":
                    if "shop" in striking_staff:
                        effective_shop_staff = 1
                    if "manufacturing" in striking_staff:
                        effective_manufacturing_staff = 0
                    if "marketing" in striking_staff:
                        effective_marketing_staff = 0
                    if "security" in striking_staff:
                        effective_security_staff = 0

                    while True:
                        try:
                            print(MAGENTA+"Pay staff to end strike? Cost: 150c. [Yes - 1] [No - 2]"+RESET)
                            choice = int(input(MAGENTA+"> "))
                            if choice == 1 and game_state["money"] >= 150:
                                game_state["money"] -= 150
                                game_state["active_event"] = None
                                print(GREEN+"Strike ended! Staff return to work."+RESET)
                            elif choice == 1 and game_state["money"] < 150:
                                print(RED+"You cannot afford to pay them. Strike continues."+RESET)
                            elif choice == 2:
                                print(RED+"You refuse to pay them. Strike will end in", game_state["event_turns_left"], "turns."+RESET)
                            else:
                                print(RED+"Invalid. Please enter [1 - 2].")
                        except:
                            print(RED+"Invalid. Please try again.")

        print()

    orig_Switches = game_state["Switch"]
    orig_Xboxes = game_state["Xbox"]
    orig_Playstations = game_state["Playstation"]
    orig_money = game_state["money"]
    time.sleep(3)

    #-------------maintenenance & generator related stuff--------------

    if game_state["fullturn"] % 3 == 2:
        if generators_active:
            print(YELLOW+"⚠ Maintenance is due tomorrow. Make sure you have enough money! ⚠"+RESET)
            time.sleep(1)
            
        else:
            print(RED+"⚠ Maintenance is due tomorrow, and your generators are already offline! ⚠"+RESET)
            time.sleep(1)

        print()

    if game_state["fullturn"] % 3 == 1:
        Switch_price = Switch_price + random.randint(-10,10)
        Xbox_price = Xbox_price + random.randint(-10,10)
        Playstation_price = Playstation_price + random.randint(-10,10)
        Switch_price = round(Switch_price / 5) * 5
        Xbox_price = round(Xbox_price / 5) * 5
        Playstation_price = round(Playstation_price / 5) * 5
        if not customers_this_turn == 10 and not game_state["fullturn"] == 1:
            customers_this_turn = customers_this_turn + 1

        Switch_price = clampPrice(Switch_price, Switch_min, Switch_max)
        Xbox_price = clampPrice(Xbox_price, Xbox_min, Xbox_max)
        Playstation_price = clampPrice(Playstation_price, Playstation_min, Playstation_max)

    if not generators_active:
        base_maintenance = 0

        for gen in game_state["SwitchGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Switch_maintainance * reduction

        for gen in game_state["XboxGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Xbox_maintainance * reduction

        for gen in game_state["PlaystationGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Playstation_maintainance * reduction


        maintenance = int(base_maintenance * getMaintenanceModifier())

        if game_state["money"] >= maintenance:
            game_state["money"] -= maintenance
            generators_active = True
            print(GREEN+"You managed to pay overdue maintenance!")
            print("Generators are back online."+RESET)
            time.sleep(1)

    if game_state["fullturn"] % 3 == 0:
        base_maintenance = 0

        for gen in game_state["SwitchGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Switch_maintainance * reduction

        for gen in game_state["XboxGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Xbox_maintainance * reduction

        for gen in game_state["PlaystationGenerators"]:
            reduction = 1 - (0.15 * gen["eco"])
            base_maintenance += Playstation_maintainance * reduction

        modifier = getMaintenanceModifier()
        maintenance = int(base_maintenance * modifier)

        print()
        print(YELLOW+"Maintenance day!"+RESET)
        print(YELLOW+"Cost of maintenance: ", maintenance, "c."+RESET)
        time.sleep(1)

        if game_state["money"] >= maintenance:
            game_state["money"] -= maintenance
            generators_active = True
            print(GREEN+"Maintenance paid. Generators operational"+RESET)
            time.sleep(3)
        
        else:
            generators_active = False
            print(RED+"⚠You cannot afford to pay the maintenance fee!⚠"+RESET)
            print(RED+"⚠Generators will shut down until the payment is made.⚠"+RESET)
            print()
            time.sleep(3)

    #----------------------before turn stuff------------------------

    subturn = 0
    if game_state["active_event"] == "sale":
        if len(game_state["customers"]) < (customers_this_turn + 3):
            for b in range((customers_this_turn + 3) - len(game_state["customers"])):
                addCustomer()
    else:
        if len(game_state["customers"]) < customers_this_turn:
            for b in range(customers_this_turn - len(game_state["customers"])):
                addCustomer()

    if game_state["tutorial"] == True:
        print()
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"Before a turn you will be notified of how many customers are waiting and what they want."+RESET)
        print(BLUE+"These ones both want a Switch."+RESET)
        print()
    
    print(YELLOW+"Customers waiting", len(game_state["customers"]), ":" +RESET)

    for i, customer in enumerate(game_state["customers"]):
        row_color = DEFAULT if i % 2 == 0 else CYAN

        amount = customer.get("amount", 1)
        print()
        if customer["type"] == "scammer":
                cType = "normal"
        else:
            cType = customer["type"]
        print(
            row_color+" [", i, "] ", customer['name'], " (",
            cType, ") wants",
            amount, customer['want'], "((e)s).",
            "They will wait ", customer['patience'], " more turns."+RESET)

    print()
    print(DEFAULT+"Currently, you have:"+RESET)
    print()
    print(DEFAULT+" - ",  int(game_state["Switch"]), " Switch(es)"+RESET)
    print(CYAN+" - ", int(game_state["Xbox"]), " Xbox(es)"+RESET)
    print(DEFAULT+" - ", int(game_state["Playstation"]), " Playstation(s)"+RESET)
    print()
    print(DEFAULT+"Currently, the generators you have are:"+RESET)
    print(DEFAULT+" - ", len(game_state["SwitchGenerators"]), " Switch generator(s)"+RESET)
    print(CYAN+" - ", len(game_state["XboxGenerators"]), " Xbox generator(s)"+RESET)
    print(DEFAULT+" - ", len(game_state["PlaystationGenerators"]), " Playstation generator(s)"+RESET)

    status = "ONLINE" if generators_active else "OFFLINE"
    color = GREEN if generators_active else RED

    print(color + "Generators status:", status +RESET)
    print()
    print(DEFAULT+"Shopkeeping staff:", effective_shop_staff, "employees"+RESET)
    print(CYAN+"Customers you can serve per turn:", effective_shop_staff, "."+RESET)
    print(DEFAULT+"Manufacturing staff:", effective_manufacturing_staff, "."+RESET)
    print(CYAN+"Hand-craft time:",
        getCraftTime(), "seconds"+RESET)
    print(DEFAULT+"Marketing staff:", effective_marketing_staff, "."+RESET)
    print(CYAN+"Effectiveness:", effective_marketing_staff, "."+RESET)
    print(DEFAULT+"Security staff:", effective_security_staff, "."+RESET)
    print(CYAN+"Scam protection level:", max(0, 0 + (effective_security_staff * 2)), "."+RESET)



          

    time.sleep(5)
    print()
    print(CYAN+"----------------------turn", game_state["fullturn"], "begin-----------------------"+RESET)
    print()
    subturn = 1

    while subturn <= 3:

        time.sleep(2)
        print()
        print(CYAN+"----------------------subturn ", subturn, "------------------------"+RESET)
        print()

        if game_state["tutorial"] == True:
            if subturn == 1:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Once your turn starts, you will then be asked what you want to do."+RESET)
                print(BLUE+"In each turn you will have three 'subturns'. In a subturn, if you wish,"+RESET)
                print(BLUE+"you can end your turn even if you have not used all three subturns."+RESET)
                print(BLUE+"This time, select 'buy generators'. Let's get a Switch generator."+RESET)
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
        print(DEFAULT+"Your money is: ", game_state["money"], "c."+RESET)
        print()
        print(CYAN+"Choose an action category:"+RESET)
        print()
        if game_state["tutorial"] == True:
            if subturn == 1:
                print(BLUE+" [1] Buy generators"+RESET)
                print(MAGENTA+" [2] Hand crafting"+RESET)
            else:
                print(MAGENTA+" [1] Buy generators"+RESET)
                print(BLUE+" [2] Hand crafting"+RESET)
        else:
            print(MAGENTA+" [1] Buy generators"+RESET)
            print(MAGENTA+" [2] Hand crafting"+RESET)
        if canClaimBronze() and not game_state["awards"]["bronze"]:
            print(BRONZE+" [3] Staff management"+RESET)
        elif canClaimSilver() and not game_state["awards"]["silver"] and game_state["awards"]["bronze"]:
            print(SILVER+" [3] Staff management"+RESET)
        elif canClaimGold() and not game_state["awards"]["gold"] and game_state["awards"]["silver"]:
            print(GOLD+" [3] Staff management"+RESET)
        elif canClaimPlatinum() and not game_state["awards"]["platinum"] and game_state["awards"]["gold"]:
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

        game_state["turnUsed"] = False
        if choice == 0:
            print()
            choice = 9
            validAction = False
            subturn = 4
            game_state["turnUsed"] = True

        if choice == 1:

                print()
                print(CYAN+"--- Buy Generators ---"+RESET)
                print()
                print(CYAN+"You have:"+RESET)
                print()
                print(DEFAULT+" - ", len(game_state["SwitchGenerators"]), " Switch generator(s)"+RESET)
                print(CYAN+" - ", len(game_state["XboxGenerators"]), " Xbox generator(s)"+RESET)
                print(DEFAULT+" - ", len(game_state["PlaystationGenerators"]), " Playstation generator(s)"+RESET)
                status = "ONLINE" if generators_active else "OFFLINE"
                color = GREEN if generators_active else RED
                print(color + "Generators status:", status +RESET)
                print()

                if game_state["tutorial"] == True:
                    print(BLUE+"-Tutorial-"+RESET)
                    print(BLUE+"Buy a Switch generator with your 100 coins."+RESET)
                    print(BLUE+"However, do note: every generator you buy equates to"+RESET)
                    print(BLUE+"more money added to the maintenance fee (in 2 turns)"+RESET)
                    print()

                if "get_Switch_generator" in possibleActions:
                    if game_state["tutorial"] == True:
                        print(BLUE+" [1] Switch generator - 100c"+RESET)
                    else:
                        print(GREEN+" [1] Switch generator - 100c"+RESET)
                else:
                    print(RED+" [1] Switch generator - 100c (too expensive)"+RESET)

                if "get_Xbox_generator" in possibleActions:
                    print(GREEN+" [2] Xbox generator - 200c"+RESET)
                else:
                    print(RED+" [2] Xbox generator - 200c (too expensive)"+RESET)
                
                if "get_Playstation_generator" in possibleActions:
                    print(GREEN+" [3] Playstation generator - 300c"+RESET)
                else:
                    print(RED+" [3] Playstation generator - 300c (too expensive)"+RESET)

                print(MAGENTA+" [4] Upgrade Generators"+RESET)
                
                print()
                print(MAGENTA+" [0] Back"+RESET)
                print()

                while True:
                    try:
                        sub = int(input(MAGENTA+"> "))

                        if sub == 0:
                            break

                        if sub == 1:
                            if game_state["money"] >= 100:
                                game_state["SwitchGenerators"].append({
                                    "efficiency": 1,
                                    "eco": 0
                                })
                                game_state["money"] -= 100
                                print(GREEN+"Bought a Switch generator."+RESET)
                                game_state["turnUsed"] = True
                                break
                            else:
                                print(RED+"You can't afford that."+RESET)
                        
                        elif sub == 2:
                            if game_state["money"] >= 200 and "get_Xbox_generator" in possibleActions:
                                game_state["XboxGenerators"].append({
                                    "efficiency": 1,
                                    "eco": 0
                                })
                                game_state["money"] -= 200
                                print(GREEN+"Bought an Xbox generator."+RESET)
                                game_state["turnUsed"] = True
                                break

                            elif game_state["money"] >= 200 and not "get_Xbox_generator" in possibleActions:
                                print(YELLOW+"You need a Switch generator first."+RESET)
                            
                            else:
                                print(RED+"You can't afford that."+RESET)
                        
                        elif sub == 3:
                            if game_state["money"] >= 300 and "get_Playstation_generator" in possibleActions:
                                game_state["PlaystationGenerators"].append({
                                    "efficiency": 1,
                                    "eco": 0
                                })
                                game_state["money"] -= 300
                                print(GREEN+"Bought a Playstation generator."+RESET)
                                game_state["turnUsed"] = True
                                break

                            elif game_state["money"] >= 300 and not "get_Playstation_generator" in possibleActions:
                                print(YELLOW+"You need an Xbox generator first."+RESET)

                            else:
                                print(RED+"You can't afford that."+RESET)

                        elif sub == 4:
                            print()
                            print(CYAN+"--- Generator Upgrades---"+RESET)
                            print()
                            if len(game_state["SwitchGenerators"]) >= 1:
                                print(GREEN+" [1] Switch generator"+RESET)
                            else:
                                print(RED+" [1] Switch generator (none to upgrade)"+RESET)
                            if len(game_state["XboxGenerators"]) >= 1:
                                print(GREEN+" [2] Xbox generator"+RESET)
                            else:
                                print(RED+" [2] Xbox generator (none to upgrade)"+RESET)
                            if len(game_state["PlaystationGenerators"]) >= 1:
                                print(GREEN+" [3] Playstation generator"+RESET)
                            else:
                                print(RED+" [3] Playstation generator (none to upgrade)"+RESET)
                            print()
                            print(MAGENTA+" [0] Back"+RESET)
                            print()

                            try:
                                upgrade_choice = int(input("> "))
                                
                                if upgrade_choice == 0:
                                    break

                                elif upgrade_choice == 1:
                                    selected_list = game_state["SwitchGenerators"]
                                    base_cost_eff = 90
                                    base_cost_eco = 70
                                    gen_name = "Switch"
                                elif upgrade_choice == 2:
                                    selected_list = game_state["XboxGenerators"]
                                    base_cost_eff = 180
                                    base_cost_eco = 150
                                    gen_name = "Xbox"
                                elif upgrade_choice == 3:
                                    selected_list = game_state["PlaystationGenerators"]
                                    base_cost_eff = 250
                                    base_cost_eco = 200
                                    gen_name = "Playstation"

                                else:
                                    print(RED + "Invalid. Please enter [0-3]." + RESET)
                                    continue

                            except:
                                print(RED+"Invalid. Please try again."+RESET)
                                continue
                            
                            if len(selected_list) == 0:
                                print(RED + "You have no generators of this type." + RESET)
                                continue

                            while True:
                                print()
                                print(CYAN+f"--- {gen_name} Generators ---"+RESET)
                                print()

                                for i, gen in enumerate(selected_list):
                                    print(
                                        MAGENTA+f"[{i}] Efficiency: {gen['efficiency']} | Eco: {gen['eco']}"
                                    )
                                print()
                                print(MAGENTA+" [-1] Back")
                                print()

                                try:
                                    index = int(input(MAGENTA+"> "))

                                    if index == -1:
                                            break
                                    if not 0 <= index < len(selected_list):
                                        print(RED+"Invalid generator number."+RESET)
                                        continue
                                except:
                                    print(RED+"Invalid. Please try again."+RESET)
                                    continue

                                gen = selected_list[index]

                                while True:
                                    print()
                                    print(CYAN+"--- Upgrade options ---"+RESET)
                                    print()
                                    if not gen["efficiency"] >= 3:
                                        print(GREEN+" [1] Upgrade efficiency"+RESET)
                                    else:
                                        print(YELLOW+" [1] Upgrade efficiency (MAXED OUT)"+RESET)
                                    if not gen["eco"] >= 3:
                                        print(GREEN+" [2] Upgrade eco mode"+RESET)
                                    else:
                                        print(YELLOW+" [2] Upgrade economy mode (MAXED OUT)"+RESET)

                                    print()
                                    print(MAGENTA+" [0] Back")
                                    print()

                                    try:
                                        upgrade_type = int(input(MAGENTA+"> "))

                                        if upgrade_type == 0:
                                            break
                                        elif upgrade_type == 1:
                                            if gen["efficiency"] >= 3:
                                                print(YELLOW + "Efficiency already maxed!" + RESET)
                                                continue

                                            cost = int(base_cost_eff * gen["efficiency"])
                                            print(DEFAULT+f"Cost: {cost}c"+RESET)
                                            print()

                                            while True:
                                                print(MAGENTA+"Are you sure? [1 - Yes] [2 - No]")
                                                try:
                                                    confirm = int(input(MAGENTA+"> "))

                                                    if confirm == 2:
                                                        print(YELLOW+"Upgrade cancelled."+RESET)
                                                        break
                                                    elif confirm == 1:
                                                        if game_state["money"] >= cost:
                                                            gen["efficiency"] += 1
                                                            game_state["money"] -= cost
                                                            print(GREEN + "Efficiency upgraded!" + RESET)
                                                            game_state["turnUsed"] = True
                                                        else:
                                                            print(RED+"Not enough money!"+RESET)

                                                        break

                                                    else:
                                                        print(RED+"Invalid. Please enter [1-2]."+RESET)

                                                except:
                                                    print(RED+"Invalid. Please try again.")
                                            break

                                        elif upgrade_type == 2:
                                            if gen["eco"] >= 3:
                                                print(YELLOW+"Economy mode already maxed!"+RESET)
                                                continue
                                            cost = base_cost_eco * ((gen["eco"] + 1))
                                            print(f"cost: {cost}c")
                                            print()

                                            while True:
                                                print(MAGENTA+"Are you sure? [1 - Yes] [2 - No]"+RESET)
                                                try:
                                                    confirm = int(input(MAGENTA+"> "))

                                                    if confirm == 2:
                                                        print(YELLOW+"Upgrade cancelled."+RESET)

                                                    elif confirm == 1:
                                                        if game_state["money"] >= cost:
                                                            gen["eco"] += 1
                                                            game_state["money"] -= cost
                                                            print(GREEN+"Economy upgrade installed!"+RESET)
                                                            game_state["turnUsed"] = True
                                                        else:
                                                            print(RED+"Not enough money!"+RESET)
                                                        break
                                                    else:
                                                        print(RED+"Invalid. Please enter [1-2]."+RESET)
                                                except:
                                                    print(RED+"Invalid. Please try again.")
                                            break

                                        else:
                                            print(RED+"Invalid. Please enter [0-2]."+RESET)
                                    
                                    except:
                                        print(RED+"Invalid. Please try again."+RESET)
                        
                    except:
                        print(RED+"Invalid. Please try again."+RESET)


        elif choice == 2:
            print()
            print(CYAN+"--- Hand Crafting ---"+RESET)
            print()
            print(CYAN+"You have:"+RESET)
            print()
            print(DEFAULT+" - ",  int(game_state["Switch"]), " Switch(es)"+RESET)
            print(CYAN+" - ", int(game_state["Xbox"]), " Xbox(es)"+RESET)
            print(DEFAULT+" - ", int(game_state["Playstation"]), " Playstation(s)"+RESET)
            print()

            if game_state["tutorial"] == True:
                print()
                print(BLUE+"-Tutorial-"+RESET)
                print(BLUE+"Make a Switch."+RESET)
                print()

            if "make_Switch" in possibleActions:
                if game_state["tutorial"] == True:
                    print(BLUE+" [1] One Switch"+RESET)
                else:
                    print(GREEN+" [1] One Switch"+RESET)
            
            else:
                print(RED+" [1] Switch (requires generators)"+RESET)

            if "make_Xbox" in possibleActions:
                print(GREEN+" [2] One Xbox"+RESET)

            else:
                print(RED+" [2] Xbox (requires generators)"+RESET)

            if "make_Playstation" in possibleActions:
                print(GREEN+" [3] One Playstation"+RESET)
            
            else:
                print(RED+" [3] Playstation (requires generators)"+RESET)
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
                    if game_state["active_event"] == "shortage":
                        craft_time += 3

                    if productchoice == 1 and "make_Switch" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        game_state["Switch"] += 1
                        print(GREEN+"You now have one more Switch"+RESET)
                        game_state["turnUsed"] = True
                        break

                    elif productchoice == 2 and "make_Xbox" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        game_state["Xbox"] += 1
                        print(GREEN+"You now have one more Xbox."+RESET)
                        game_state["turnUsed"] = True
                        break

                    elif productchoice == 3 and "make_Playstation" in possibleActions:
                        print(MAGENTA+"making product..."+RESET)
                        time.sleep(craft_time)
                        game_state["Playstation"] += 1
                        print(GREEN+"You now have one more Playstation."+RESET)
                        game_state["turnUsed"] = True
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
            security_cost = getSecurityStaffCost()

            print(DEFAULT+"Total shopkeeping staff:", game_state["Shop_staff"], "."+RESET)
            print(CYAN+"Total manufacturing staff:", game_state["manufacturing_staff"], "." +RESET)
            print(DEFAULT+"Total marketing staff:", game_state["marketing_staff"], "." +RESET)
            print(CYAN+"Total security staff:", game_state["security_staff"], "."+RESET)
            print()
            if game_state["Shop_staff"] == 10:
                print(YELLOW+"[1] Hire shopkeeping staff - MAXED OUT (customers 10)"+RESET)
            elif game_state["money"] >= shop_cost:
                print(GREEN+" [1] Hire shopkeeping staff -", shop_cost, "c"+RESET)
            else:
                print(RED+" [1] Hire shopkeeping staff -", shop_cost, "c (too expensive)"+RESET)

            if getCraftTime() == 1:
                print(YELLOW+" [2] Hire manufacturing staff - MAXED OUT (craft time 1s)"+RESET)

            elif game_state["money"] >= manu_cost:
                print(GREEN+" [2] Hire manufacturing staff -", manu_cost, "c"+RESET)
            else:
                print(RED+" [2] Hire manufacturing staff -", manu_cost, "c (too expensive)"+RESET)
            
            if game_state["marketing_staff"] == 10:
                print(YELLOW+"[3] Hire marketing staff - MAXED OUT (influence +13)"+RESET)
            elif game_state["money"] >= market_cost:
                print(GREEN+" [3] Hire marketing staff -", market_cost, "c"+RESET)
            else:
                print(RED+" [3] Hire marketing staff -", market_cost, "c (too expensive)"+RESET)
            
            if game_state["security_staff"] == 5:
                print(YELLOW+" [4] Hire security staff - MAXED OUT (scammer risk 0%)"+RESET)
            elif game_state["money"] >= security_cost:
                print(GREEN+" [4] Hire security staff -", security_cost, "c"+RESET)
            else:
                print(RED+" [4] Hire security staff -", security_cost, "c (too expensive)"+RESET)

                        
            print()
            print(CYAN+"--- Trophies ---"+RESET)
            print()

            if not game_state["awards"]["bronze"] and canClaimBronze():
                print(BRONZE+" [6] Claim Bronze Shop Trophy"+RESET)           

            elif game_state["awards"]["bronze"] and not game_state["awards"]["silver"] and canClaimSilver():
                    print(SILVER+" [7] Claim Silver Shop Trophy"+RESET)                

            elif game_state["awards"]["silver"] and not game_state["awards"]["gold"] and canClaimGold():
                        print(GOLD+" [8] Claim Gold Superstore Trophy"+RESET)             

            elif game_state["awards"]["gold"] and not game_state["awards"]["platinum"] and canClaimPlatinum():
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
                        if game_state["Shop_staff"] == 10:
                            print(YELLOW+"You already have the maximum amount of shopkeeping staff."+RESET)
                        elif game_state["money"] >= shop_cost:
                            game_state["money"] -= shop_cost
                            game_state["Shop_staff"] += 1
                            print(GREEN+"You hired a shopkeeping staff member!"+RESET)
                            game_state["turnUsed"] = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 2:
                        if getCraftTime() == 1:
                            print(YELLOW+"Your manufacturing process is already fully optimised."+RESET)
                        elif game_state["money"] >= manu_cost:
                            game_state["money"] -= manu_cost
                            game_state["manufacturing_staff"] += 1
                            print(GREEN+"You hired manufacturing staff!"+RESET)
                            game_state["turnUsed"] = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 3:
                        if game_state["marketing_staff"] == 10:
                            print(YELLOW+"Your marketing campaign is already fully optimised. (Influence: 10)"+RESET)
                        elif game_state["money"] >= market_cost:
                            game_state["money"] -= market_cost
                            game_state["marketing_staff"] += 1
                            print(GREEN+"You hired marketing staff! More VIPs may shop here."+RESET)
                            game_state["turnUsed"] = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)
                    
                    elif sub == 4:
                        if game_state["security_staff"] == 5:
                            print(YELLOW+"Security team fully deployed."+RESET)
                        elif game_state["money"] >= security_cost:
                            game_state["money"] -= security_cost
                            game_state["security_staff"] += 1
                            print(GREEN+"You hired security staff! Your shop is now more secure."+RESET)
                            game_state["turnUsed"] = True
                            break
                        else:
                            print(RED+"You can't afford that."+RESET)

                    
                    elif sub == 6 and canClaimBronze() and not game_state["awards"]["bronze"]:
                        game_state["awards"]["bronze"] = True
                        applyAwardBuff("bronze")
                        print(BRONZE+"🥉 Bronze Shop Trophy earned! 🥉"+RESET)
                        print(BRONZE+"Reputation increased!"+RESET)
                        time.sleep(3)
                        game_state["turnUsed"] = True
                        break

                    elif sub == 7 and canClaimSilver() and game_state["awards"]["bronze"]:
                        game_state["awards"]["silver"] = True
                        applyAwardBuff("silver")
                        print(SILVER+"🥈 Silver Shop Trophy earned! 🥈"+RESET)
                        print(SILVER+"Extra shop staff hired for free!"+RESET)
                        time.sleep(4)
                        game_state["turnUsed"] = True
                        break

                    elif sub == 8 and canClaimGold() and game_state["awards"]["silver"]:
                        game_state["awards"]["gold"] = True
                        applyAwardBuff("gold")
                        print(GOLD+"🥇 Gold Superstore Trophy earned! 🥇"+RESET)
                        print(GOLD+"Your shop is now famous!"+RESET)
                        time.sleep(3)
                        game_state["turnUsed"] = True
                        break

                    elif sub == 9 and canClaimGoal():
                        game_state["awards"]["platinum"] = True
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
                                    time.sleep(6)
                                    game_state["game_won"] = True
                                    break
                                else:
                                    applyAwardBuff("platinum")
                                    print()
                                    print(PLATINUM+"I knew you'd stay, master of business!"+RESET)
                                    print(PLATINUM+"With this award you will receive many buffs!"+RESET)
                                    print(PLATINUM+"Enjoy your free play now!"+RESET)
                                    time.sleep(6)
                                    break
                            except:
                                print(RED+"That is invalid, master of business. Please try again")

                        print()
                        game_state["turnUsed"] = True
                        break

                    
                    else:
                        if canClaimAward():
                            print(RED+"Invalid. Please enter [0-3] or [6-9]."+RESET)
                        else:
                            print(RED+"Invalid. Please enter [0-3].")
                
                except:
                    print(RED+"Invalid. Please try again.")

        if game_state["turnUsed"] == True:
            subturn += 1
        if game_state["game_won"] == True:
            break

        staff = game_state["Shop_staff"] + game_state["manufacturing_staff"] + game_state["marketing_staff"] + game_state["security_staff"]

    if game_state["game_won"] == True:
        break


    #----------------------------------selling here------------------------------------------------------------------------------
    print()
    time.sleep(1)
    print(CYAN+"-----------------------turn end------------------------"+RESET)
    time.sleep(2)

    production_multiplier = 1

    if game_state["active_event"] == "shortage":
        production_multiplier = 0.5

    if generators_active:
        for gen in game_state["SwitchGenerators"]:
            game_state["Switch"] += int(gen["efficiency"] * genProduction * production_multiplier)

        for gen in game_state["XboxGenerators"]:
            game_state["Xbox"] += int(gen["efficiency"] * genProduction * production_multiplier)

        for gen in game_state["PlaystationGenerators"]:
            game_state["Playstation"] += int(gen["efficiency"] * genProduction * production_multiplier)

    
    else:
        print(RED+"⚠Your generators are inactive so could not produce products this turn.⚠"+RESET)

    if game_state["tutorial"] == True:
        print()
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"After a turn you can then sell your made products to waiting customers."+RESET)
        print(BLUE+"Sell two of your Switches to these normal customers."+RESET)
        print(BLUE+"Some customers will occasionally have a different type such as vips who pay more."+RESET)
        print()

    print()
    print(DEFAULT+"Time to sell products:"+RESET)
    print()
    print(DEFAULT+"You have:"+RESET)
    print()
    print(CYAN+" - ", int(game_state["Switch"]), " Switch(es)"+RESET)
    print(DEFAULT+" - ", int(game_state["Xbox"]), " Xbox(es)"+RESET)
    print(CYAN+" - ", int(game_state["Playstation"]), " Playstation(s)"+RESET)

    game_state["customers"].sort(
    key=lambda c: (
        c["type"] != "vip",     # VIPs first
        c["patience"]           # low patience first
    )
)

    if effective_marketing_staff > 0:
        print(GREEN+"📣 Marketing campaign active (+",game_state["marketing_staff"], " influence) 📣"+RESET)
    if effective_security_staff > 0:
        print(GREEN+"🛡 Security presence deters suspicious activity. 🛡"+RESET)


    print(DEFAULT+"Customers in shop:"+RESET)
    for i, customer in enumerate(game_state["customers"]):
        if game_state["tutorial"] == True:
            row_color = BLUE if i % 2 == 0 else CYAN
        else:
            row_color = DEFAULT if i % 2 == 0 else CYAN

        amount = customer.get("amount", 1)
        if customer["type"] == "scammer":
            cType = "normal"
        else:
            cType = customer["type"]
        print(
            row_color+" [", i, "] ", customer ['name'],
            "(" + cType.capitalize() + ")", " wants: ",
            amount, customer['want'],
            "((e)s) they will wait ", customer['patience'], "turns."+RESET
        )
        if customer["type"] == "bargainer":
            percent = int(customer["multiplier"] * 100)
            print(YELLOW + f"💬 Current offer: {percent}% of market price. (this may rise or fall)" + RESET)

        if customer["patience"] == 1:
                print(RED+"⚠ This customer is about to leave! ⚠"+RESET)
        print()

    orig_sale_money = game_state["money"]

    customers_served = 0
    max_servesPerTurn = effective_shop_staff
    if game_state["active_event"] == "sale":
        max_servesPerTurn = effective_shop_staff + 3

    while customers_served < max_servesPerTurn and len(game_state["customers"]) > 0:
        print()
        print(MAGENTA+"You can serve ", max_servesPerTurn - customers_served, " more customer(s)."+RESET)
        print(MAGENTA+"Enter customer number to serve, -1 to stop, or -2 to serve all."+RESET)

        try:
            choice = int(input(MAGENTA+">"))

            if choice == -2:
                i = 0
                while i < len(game_state["customers"]) and customers_served < max_servesPerTurn:
                    customer = game_state["customers"][i]
                    want = customer["want"]
                    amount = customer.get("amount", 1)

                    #right, lets see, do we have enough ___s?
                    can_serve = True
                    # - scammers 😈 -
                    if customer["type"] == "scammer":
                        if want == "Switch" and game_state["Switch"] < 2:
                            can_serve = False
                        elif want == "Xbox" and game_state["Xbox"] < 2:
                            can_serve = False
                        elif want == "Playstation" and game_state["Playstation"] < 2:
                            can_serve = False
                    
                    # - normals 😀 -
                    else:
                        if want == "Switch" and game_state["Switch"] < amount:
                            can_serve = False
                        elif want == "Xbox" and game_state["Xbox"] < amount:
                            can_serve = False
                        elif want == "Playstation" and game_state["Playstation"] < amount:
                            can_serve = False
                        elif want == "all" and (game_state["Switch"] < 1 or game_state["Xbox"] < 1 or game_state["Playstation"] < 1):
                            can_serve = False
                    
                    if not can_serve:
                        i += 1
                        continue

                    # Now we need to actually SELL IT!!!
                    if customer["type"] == "scammer":
                        if want == "Switch":
                            game_state["Switch"] -= 2
                        elif want == "Xbox":
                            game_state["Xbox"] -= 2
                        elif want == "Playstation":
                            game_state["Playstation"] -= 2
                        
                        total_price = 0
                        print(RED+f"{customer['name']} scammed you! They took extra stack and paid nothing!"+RESET)
                        print(RED + f"{customer['name']} slipped away into the crowd..." + RESET)
                    else:
                        if want == "Switch":
                            game_state["Switch"] -= amount
                            base_price = Switch_price

                        elif want == "Xbox":
                            game_state["Xbox"] -= amount
                            base_price = Xbox_price

                        elif want == "Playstation":
                            game_state["Playstation"] -= amount
                            base_price = Playstation_price

                        elif want == "all":
                            game_state["Switch"] -= 1
                            game_state["Xbox"] -= 1
                            game_state["Playstation"] -= 1
                            base_price = int((Switch_price + Xbox_price + Playstation_price) * 1.1)
                    
                    if customer["type"] != "scammer":
                        total_price = base_price * amount
                    
                    if customer["type"] == "vip":
                        total_price = int(total_price * (1 + (customer['patience'] / 10)))
                    elif customer["type"] == "impatient":
                        total_price = int(total_price * 0.9)
                    elif customer["type"] == "bulk":
                        total_price = int(total_price * 0.9)
                    elif customer["type"] == "normal":
                        total_price = int(total_price * (0.8 + (game_state["reputation"] / 100) * 0.4))
                    elif customer["type"] == "bargainer":
                        total_price = int(total_price * customer["multiplier"])
                    
                    game_state["money"] += total_price

                    orig_reputation = game_state["reputation"]

                    if customer['type'] == "normal":
                        game_state["reputation"] += random.randint(1,2)

                    elif customer['type'] == "impatient":
                        game_state["reputation"] += random.randint(0,1)

                    elif customer['type'] == "vip":
                        game_state["reputation"] += random.randint(2,5)

                    elif customer['type'] == "bulk":
                        game_state["reputation"] += random.randint(1,3)

                    elif customer['type'] == "grand":
                        game_state["reputation"] += random.randint(2,5)

                    elif customer['type'] == "bargainer":
                        game_state["reputation"] += random.randint(0,2)

                    elif customer['type'] == "scammer":
                        game_state["reputation"] -= random.randint(0,2)

                    if game_state["active_event"] == "journalist":
                        game_state["reputation"] += int((game_state["reputation"] - orig_reputation) * 0.5)

                    clampReputation()

                    if customer["type"] == "vip":
                        game_state["vip_served"] += 1
                    else:
                        game_state["non_vip_served"] += 1

                    if customer["type"] != "scammer":
                        print(GREEN + f"Served {customer['name']} for {total_price}c." + RESET)

                    game_state["customers"].pop(i)
                    customers_served += 1

            if choice == -1:
                break
            if not 0 <= choice < len(game_state["customers"]):
                print(RED+"Invalid customer number."+RESET)
                time.sleep(1)
                continue
            
            customer = game_state["customers"][choice]
            want = customer["want"]
            amount = customer.get("amount", 1)

            #find base prices
            if customer["type"] == "scammer":
                if want == "Switch":
                    if game_state["Switch"] >= 2:
                        game_state["Switch"] -= 2
                    else:
                        print(RED+"You don't have enough Switches!"+RESET)
                        time.sleep(1)
                        continue

                elif want == "Xbox":
                    if game_state["Xbox"] >= 2:
                        game_state["Xbox"] -= 2
                    else:
                        print(RED+"You don't have enough Switches!"+RESET)
                        time.sleep(1)
                        continue

                elif want == "Playstation":
                    if game_state["Playstation"] >= 2:
                        game_state["Playstation"] -= 2
                    else:
                        print(RED+"You don't have enough Switches!"+RESET)
                        time.sleep(1)
                        continue
                

                print(RED+f"{customer['name']} scammed you! They took extra stack and paid nothing!"+RESET)
                print(RED + f"{customer['name']} slipped away into the crowd..." + RESET)
                total_price = 0

            elif want == "Switch" and not customer["type"] == "scammer":
                if game_state["Switch"] < amount:
                    print(RED+"You don't have enough Switches!"+RESET)
                    time.sleep(1)
                    continue
                base_price = Switch_price
                game_state["Switch"] -= amount
            
            elif want == "Xbox" and not customer["type"] == "scammer":
                if game_state["Xbox"] < amount:
                    print(RED+"You don't have enough Xboxes!"+RESET)
                    time.sleep(1)
                    continue
                base_price = Xbox_price
                game_state["Xbox"] -= amount

            elif want == "Playstation" and not customer["type"] == "scammer":
                if game_state["Playstation"] < amount:
                    print(RED+"You don't have enough Playstations!"+RESET)
                    time.sleep(1)
                    continue
                base_price = Playstation_price
                game_state["Playstation"] -= amount
            
            elif want == "all":
                if game_state["Switch"] >= 1 and game_state["Xbox"] >= 1 and game_state["Playstation"] >= 1:
                    game_state["Switch"] -= 1
                    game_state["Xbox"] -= 1
                    game_state["Playstation"] -= 1
                    total_price = (Switch_price + Xbox_price + Playstation_price)
                    total_price = int(total_price * 1.1)
            
            #here is the base total price, code!
            if not customer["type"] == "scammer":
                total_price = base_price * amount

            #don't forget to add type multipliers
            if customer["type"] == "vip":
                total_price = int(total_price * (1 + (customer['patience'] / 10)))

            elif customer["type"] == "impatient":
                total_price = int(total_price * 0.9)
            
            elif customer['type'] == "bulk":
                #you get a ten percent discount, bulky guys!!!
                total_price = int(total_price * 0.9)

            elif customer['type'] == "normal":
                #reputation affects price!!!
                total_price = int(total_price * (0.8 + (game_state["reputation"] / 100) * 0.4))
            
            elif customer["type"] == "bargainer":
                total_price = int(total_price * customer["multiplier"])

            game_state["money"] += total_price
            orig_reputation = game_state["reputation"]
            if customer['type'] == "normal":
                game_state["reputation"] += random.randint(1,2)
            
            elif customer['type'] == "impatient":
                game_state["reputation"] += random.randint(0,1)

            elif customer['type'] == "vip":
                game_state["reputation"] += random.randint(2,5)
            
            elif customer['type'] == "bulk":
                game_state["reputation"] += random.randint(1,3)
            
            elif customer['type'] == "grand":
                game_state["reputation"] += random.randint(2,5)
            
            elif customer['type'] == "bargainer":
                game_state["reputation"] += random.randint(0,2)
            
            elif customer['type'] == "scammer":
                game_state["reputation"] -= random.randint(0,2)

            if game_state["active_event"] == "journalist":
                game_state["reputation"] += int((game_state["reputation"] - orig_reputation) * 0.5)
            clampReputation()

            if customer["type"] == "vip":
                game_state["vip_served"] += 1
            else:
                game_state["non_vip_served"] += 1

            if customer["type"] != "scammer":
                print(
                    GREEN+"Sold", amount, want, "((e)s) to",
                    customer['name'], "(" + customer['type'] + ") for",
                    total_price, "c."+RESET
                )
            time.sleep(1)


            game_state["customers"].pop(choice)
            customers_served += 1

            # re display updated customer list
            if len(game_state["customers"]) > 0:
                print()
                print(DEFAULT+"Updated customers:"+RESET)
                for i, customer in enumerate(game_state["customers"]):
                    if game_state["tutorial"] == True:
                        row_color = BLUE if i % 2 == 0 else CYAN
                    else:
                        row_color = DEFAULT if i % 2 == 0 else CYAN

                    amount = customer.get("amount", 1)

                    if customer["type"] == "scammer":
                        cType = "normal"
                    else:
                        cType = customer["type"]

                    print(
                        row_color+" [", i, "] ", customer['name'],
                        "(" + cType.capitalize() + ") wants:",
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
    if game_state["tutorial"] == True:
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"After a turn you will receive a summary of that turn!"+RESET)
        print()
    print(DEFAULT+"Turn ", game_state["fullturn"], " summary:"+RESET)
    print(CYAN+ prependPlusSign(int(game_state["Switch"] - orig_Switches)), " Switch(es)"+RESET)
    print(DEFAULT+ prependPlusSign(int(game_state["Xbox"] - orig_Xboxes)), " Xbox(es)"+RESET)
    print(CYAN+ prependPlusSign(int(game_state["Playstation"] - orig_Playstations)), " Playstation(s)"+RESET)
    print(DEFAULT+"-", orig_money - orig_sale_money, " spent"+RESET)
    print(CYAN+"+", game_state["money"] - orig_sale_money, " sales"+RESET)

    print(DEFAULT+ prependPlusSign(int(game_state["money"] - orig_money)), " overall profit"+RESET)
    print()
    if game_state["awards"]["platinum"] == True:
        print(DEFAULT+"Shop reputation:", game_state["reputation"], "/ 125"+RESET)
    else:
        print(DEFAULT+"Shop reputation:", game_state["reputation"], "/ 100"+RESET)
    if game_state["reputation"] >= 100:
        print(GOLD+"Customers talk about your shop across the city!"+RESET)

    elif game_state["reputation"] >= 80 and game_state["reputation"] < 100:
        print(GREEN+"Your shop is well respected! VIPs love it here."+RESET)

    elif game_state["reputation"] <= 20:
        print(RED+"Your shop has a bad reputation… customers are more impatient."+RESET)
    
    print()
    
    if game_state["money"] <= 99:
        print(YELLOW+"Money:", game_state["money"], "c. Keep saving up!"+RESET)
    elif game_state["money"] >= 100 and game_state["money"] <= 750:
        print(GREEN+"Money:", game_state["money"], "c."+RESET)
    elif game_state["money"] >= 750:
        print(GOLD+"Money:", game_state["money"], "c. You are rich!"+RESET)
    
        
    
    print()
    print(DEFAULT+"Shop award rank:"+RESET)

    if game_state["awards"]["platinum"]:
        print(PLATINUM+"💎 Platinum Superstore Trophy — LEGENDARY SHOP!!! 💎"+RESET)
        print(PLATINUM+"💎 Well done on your big achievement!!! 💎"+RESET)
        print(PLATINUM+"💎 You have reached the highest rank!!! 💎")

    elif game_state["awards"]["gold"]:
        print(GOLD+"🥇 Gold Superstore Trophy — Elite business 🥇"+RESET)
        print(GOLD+"Platinum trophy requirements:"+RESET)
        print(GOLD+" -",GOAL_COST, "c"+RESET)
        print(GOLD+" - One of every generator"+RESET)
        print(GOLD+" - Rep: 100 (max)"+RESET)

    elif game_state["awards"]["silver"]:
        print(SILVER+"🥈 Silver Shop Trophy — Growing success 🥈"+RESET)
        print(SILVER+"Gold trophy requirements:"+RESET)
        print(SILVER+" - 1300c"+RESET)
        print(SILVER+" - Rep: 70"+RESET)
        print(SILVER+" - One of every staff member"+RESET)

    elif game_state["awards"]["bronze"]:
        print(BRONZE+"🥉 Bronze Shop Trophy — On the rise 🥉"+RESET)
        print(BRONZE+"Silver trophy requirements:"+RESET)
        print(BRONZE+" - 800c"+RESET)
        print(BRONZE+" - Rep: 60"+RESET)

    else:
        print(DEFAULT+"No trophies yet — keep building your shop!"+RESET)
        print(DEFAULT+"First trophy requirements:"+RESET)
        print(DEFAULT+" - 300 or more coins"+RESET)
        print(DEFAULT+" - reputation of 50 or above"+RESET)

    if game_state["active_event"] is not None:
        game_state["event_turns_left"] -= 1

        if game_state["event_turns_left"] <= 0:
            if game_state["active_event"] == "sale":
                print(RED+"The sale has ended. Things return to normal."+RESET)
            elif game_state["active_event"] == "shortage":
                print(GREEN+"Supply lines restored. Production normalised."+RESET)
            elif game_state["active_event"] == "journalist":
                print(YELLOW+"The journalist has left your shop now."+RESET)
            elif game_state["active_event"] == "cyber_attack":
                print(GREEN+"Your IT team restored the generators!"+RESET)

            game_state["active_event"] = None
    
    if game_state["tutorial"] == True:
        game_state["tutorial"] = False
        print()
        print(BLUE+"-Tutorial-"+RESET)
        print(BLUE+"Well, I think thats about it. You know all you need to know."+RESET)
        print(BLUE+"It was nice teaching you but it's time you continue on your own!"+RESET)
        print(BLUE+"Enjoy my game! :)"+RESET)
        print()

    print()
    print()
    print(CYAN+"-------------------------------------------------------"+RESET)
    time.sleep(8)
    print()
    print()
