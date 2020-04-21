import time
import random

# Figuring out how users might respond
choiceA = ["A", "a"]        #List that estblishes the choices(A or a) when using choice a
choiceB = ["B", "b"]
choiceC = ["C", "c"]

#Gold is assigned to an empty list and XP is assigned as 0
gold = []
XP = 0

#Weapon for Boss
legendarySword = 0

#inventory - Dictionary
inv = {"Potion" : 0}

#Type of Enemy - Dictionary(Comment)
enemy = {"name": None, "health": None, "attack": None}      #Establishes the enemy name, health and attack
Goblin = {"name":"Goblin", "health":(10),"attack":(10,20,30)}       #Establishes the characteristics of a specific enemy
Troll = {"name":"Troll","health":(30),"attack":(5,15,20)}       #Shows the potential damage they can deal
Spider = {"name":"Spider","health":(20),"attack":(20,30,35)}
Warlock = {"name":"Warlock","health":(40),"attack":(10,20,30)}
UndeadKnight = {"name":"Undead Knight","health":(30),"attack":(5,20,25)}
Zombie = {"name" : "Zombie", "health" : (20), "attack" : (5, 10, 25)}

bossEnemy = {"name":None, "health":None, "attack":None}             #boss has separate combat
Boss = {"name":"BOSS","health":(70),"attack":(10,20,30)}



required = ("\nYou must only use A, B, or C\n")  # Cutting down on duplication


# The story is broken into sections, starting with "intro"
def intro():
    print("Your eyes adjust to the bright beeming light,the sound of trumpets and harps make you realize your surroundings.\n"
          "That’s right, you were at your village’s annual festival. \n"
          "Your eyes catch a bright purple tent in the middle of the foregrounds, with a large sign saying, 'CURIOUS TO SEE WHAT YOUR FUTURE HOLDS? COME SEE MADAME WOLPH'S READINGS.'\n"
          "You will:")
    time.sleep(1)
    print("""    A. Enter the tent 
    B. Walk away, deciding that it's not worth your time""")    #4 spaces for indentation
    answer = input(" >>> ")
    if answer in choiceA:
        path_Enter()
    elif answer in choiceB:
        print("You missed out on this life changing chance.")
        path_gameOver()
    else:
        print(required)
        intro()


def path_Enter():
    print("\nYou walk into the huge tent, seeing tarot cards and candles on display.\n"
          "In the middle of the room there is a woman shrouded in a velvet cloak, seated at table with a purple, mystic crystal ball\n"
          "She gives a little chuckle. TELL ME, PEASANT. DO YOU WANT TO KNOW WHAT YOUR FUTURE HOLDS?\n"
          "You answer:")
    time.sleep(1)
    print("""    A. Yes I do
    B. Actually...nevermind I don't""")
    answer = input(" >>> ")
    if answer in choiceA:
        path_Fortune()
    elif answer in choiceB:
        print("WHAT A PITY. I KNEW A MERE PEASANT LIKE YOU WOULDN'T WANT TO CHANGE YOUR BORING LIFE.\n"
              "HAVE FUN CONTINUING IN BEING A DISGRACE")
        path_gameOver()
    else:
        print(required)
        path_Enter()


def path_Fortune():     #Defines and calls the function
    print("\nAHHH I KNEW YOU WERE A SMART ONE FROM THE BEGINNING.\n"
          "TELL ME, PEASANT. HAVE YOU EVER WISHED TO DO MORE IN YOUR LIFE? BE MORE?\n"
          "WELL NOW'S YOUR CHANCE.\n"
          "TELL ME. DO YOU WISH TO BE A KNIGHT RISING IN THE RANKS UNDER YOUR KING?")
    time.sleep(1)
    print("""    A. I want to be a noble
    B. I just want to go home""")
    answer = input(" >>> ")
    if answer in choiceA:
        print("AHH I SEE. YOU WISH TO CHANGE YOUR FATE. WELL THEN, WHAT YOU WANT IS WHAT YOU SHALL GET.\n"
              "JUST CLOSE YOUR EYES AND LET THE DARKNESS COME THROUGH.\n"
              "Blackness hits you.\n")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("...")
        path_Nobility()
    elif answer in choiceB:
        print("HOW BORING. LOOKS LIKE YOU CAN'T ESCAPE BEING A PEASANT. TURNS OUT RESISTANCE IS FEUDAL. GO ON THEN. LEAVE.")
        path_gameOver()
    else:
        print(required)
        path_Fortune()


# This marks the beginning of the nobility route -------------
health = 100 #current health
maxHealth = 100 #max health
healthDashes = 20 #Max displayed dashes


def healthBar():
    dashConvert = int(maxHealth/healthDashes)
    currentDashes = int(health/dashConvert)
    remainingHealth = healthDashes - currentDashes  # Get the health remaining to fill as space => 12 spaces

    healthDisplay = ''.join(['-' for i in range(currentDashes)])  # Convert 8 to 8 dashes as a string:   "--------"
    remainingDisplay = ''.join(
        [' ' for i in range(remainingHealth)])  # Convert 12 to 12 spaces as a string: "            "
    percent = str(int((health / maxHealth) * 100)) + "%"  # Get the percent as a whole number:   40%

    print("\x1b[1;31m" + "|" + healthDisplay + remainingDisplay + "|" + "\x1b[0m")  # Print out textbased healthbar
    print("\x1b[1;31m" + "         " + percent + "\x1b[0m")


    '''This health bar will change depending on the different percentages you have'''       #Multiline comment about the health bar stats


def openInventory():
    for x in inv:
        if inv[x] > 0:
            print(x + ":", inv[x])
        elif inv[x] == 0:
            print(x + ":", inv[x])
            newPotion()
    path_Cave()



def newPotion():
    global health
    if inv["Potion"] > 0 and health <= 80:
        print("Do you want to drink a Potion?\n")
        time.sleep(1)
        print("""    A. Yes
    B. No""")
        answer = input(" >>> ")
        if answer in choiceA:
            health += 20
            print('You used a Potion')
            inv['Potion'] -= 1          #Subtracts one potion from the list if used
            print('You now have', (inv['Potion']), "potions")
            print("Your health is now", health)
        elif answer in choiceB:
            path_Cave()
        else:
            print(required)
            newPotion()


def sortGold():
    for i in range(0, len(gold)):       #Sorts the amount of gold from largest to smallest
        for j in range(i, len(gold)):
            if gold[j] < gold[i]:
                temp = gold[i]
                gold[i] = gold[j]
                gold[j] = temp
    return gold


def upgradeLevel():
    if XP >= 100 and XP < 200:
        print("Congratulations! You are now a Knight!")
    elif XP >= 200 and XP < 300:
        print("Congratulations! You are now a Baron!")
    elif XP >= 300 and XP < 400:
        print("Congratulations! You are now a Viscount!")
    elif XP >= 400 and XP < 500:
        print("Congratulations! You are now a Marquess!")       #Print your level
        print("Proceed to the Final Boss.\n")



def path_Nobility():
    print("\n\n\n CONGRATULATIONS PEASANT. YOU HAVE BEEN GIVEN A QUEST BY THE KING HIMSELF. COMPLETE HIS TASKS TO EARN FAVOR IN THE COURT.\n\n")
    time.sleep(1)
    print("This is your health bar. It will increase or decrease based on your health during a battle.")
    healthBar()
    print("\n\nDo you accept this change in fate?\n")
    time.sleep(1)
    print("""    A. Yes I accept
    B. Ummm what's going on??
    C. No way! Let me go back!""")
    answer = input(" >>> ")
    if answer in choiceA:       #This nested if statement checks to see if the input is correct and checks if the additional userinput matches the code
        #Has the try and except block, while loop, read file
        while(True):
            print("Enter the word, 'OPEN', to read the quest from the King")
            time.sleep(1)
            try:        #Checks if the input is correct and if it is not, raises a ValueError
                userInput = input("")
                if userInput == "OPEN" or userInput == "open":
                    file = open("Quest.txt", "r")           #Opens and reads from a quest file
                    quest = file.read()
                    print(quest)
                    time.sleep(2)

                    file.close()
                    break
                else:
                    raise ValueError

            except ValueError:
                print("This is not the correct word, please try again.")
        print("\nNOW PEASANT LET US CONTINUE THIS JOURNEY.\n")
        path_Cave()
    elif answer in choiceB:
        print("PEASANT. I SAID WHAT I SAID. LET ME REPEAT MYSELF.\n")
        path_Nobility()
    elif answer in choiceC:
        print("VERY WELL, IF THAT IS WHAT YOU WISH. BEGONE.\n")
        path_gameOver()
    else:
        print(required)
        path_Nobility()


def path_Cave():
    print("\nYou travel through the forbidden cave, searching for the mystic chest.\n")
    print("What would you like to do:")
    time.sleep(1)
    print("""    A. I want to explore
    B. I want to rest
    C. I want to see my inventory""")
    answer = input(" >>> ")
    if answer in choiceA:
        pickMonster()
    elif answer in choiceB:
        path_rest()
    elif answer in choiceC:
        openInventory()
    else:
        print(required)
        path_Cave()


def path_rest():
    print("\nYou wake up from your nap and feel rejuvinated!\n"
          "While walking you run into a chest!\n"
          "Want to open it?")
    time.sleep(1)
    print("""    A. I'll open it
    B. Hmmm...I'll skip it for now""")
    answer = input(" >>> ")
    if answer in choiceA:
        inv["Potion"] += 1
        print("You now have a new health potion!\n")
        path_Cave()
    if answer in choiceB:
        print("You continue onwards with your quest.\n")
        path_Cave()
    else:
        print(required)
        path_rest()


def pickMonster():
    print("\nYou walk through a narrow path.\n"
          "As you journey on, you recover your lost health. You are back at full HP!\n"
          "Ahead of you, the path splits into two different tunnels, one heading left and the other to the right.\n"
          "What will you do?")
    time.sleep(1)
    print("""    A. I want to go left
    B. I want to go right""")
    answer = input(" >>> ")
    if answer in choiceA:
        print(f"You have encountered a Spider\n")
        combat(Spider)
        pickMonster2()
    elif answer in choiceB:
        print(f"You have encountered a Troll\n")
        combat(Troll)
        pickMonster2()
    else:
        print(required)
        pickMonster()


def pickMonster2():
    print("\nYou continue onwards.\n"
          "As you journey on, you recover your lost health. You are back at full HP!\n"
          "Up ahead there is a slippery road to your left and a jagged road to your right.\n"
          "What will you do?")
    time.sleep(1)
    print("""    A. I want to go left
    B. I want to go right""")
    answer = input(" >>> ")
    if answer in choiceA:
        print(f"You have encountered a Goblin\n")
        combat(Goblin)
        pickMonster3()
    elif answer in choiceB:
        print(f"You have encountered a Warlock\n")
        combat(Warlock)
        pickMonster3()
    else:
        print(required)
        pickMonster2()


def pickMonster3():
    print("\nYou fall down a hole.\n"
          "As you journey on, you recover your lost health. You are back at full HP!\n"
          "Do you attempt to climb up? Or wander through the passage ways?\n"
          "What will you do?")
    time.sleep(1)
    print("""    A. I want to go up
    B. I want to go through""")
    answer = input(" >>> ")
    if answer in choiceA:
        print(f"You have encountered an Undead Knight\n")
        combat(UndeadKnight)
        merchant()
    elif answer in choiceB:
        print(f"You have encountered a Zombie\n")
        combat(Zombie)
        merchant()
    else:
        print(required)
        pickMonster3()


def combat (enemy):     #Defines the function with the parameter/dictionary of enemy and calls
    global health
    global XP
    global gold
    print("Do you wish to attack the beast?")
    print("""    A. Yes
    B. No""")
    answer = input(" >>> ")
    if answer in choiceA:
        time.sleep(1.5)
        print("\nA wise choice, the King will hear of your bravery.\n"
              "You withdraw your weapon and strike the foe.")
        player_damage = random.randint(1,70)        #Chooses a random int within the range 1-69 to deal damage to the enemy
        time.sleep(1.5)
        print(f"You have dealt {player_damage} damage to your foe.")

        NME_damage = random.choice(enemy["attack"])
        time.sleep(1.5)
        print(f"The enemy has hit you for {NME_damage} damage.")

        NME_health = enemy["health"]
        newNME_health = NME_health - player_damage
        print("The enemy has", newNME_health, "health left")
        if newNME_health <= 0:
            print("You have defeated the enemy!")
        else:
            player_damage = random.randint(1,70)
            print(f"You have dealt {player_damage} damage to your foe.")


        player_win = player_damage >= enemy["health"]

        '''Adjustment to health bar based on combat'''
        healthcheck = health
        newHealth = healthcheck - NME_damage
        dashConvert = int(maxHealth / healthDashes)
        currentDashes = int(newHealth / dashConvert)
        remainingHealth = healthDashes - currentDashes  # Get the health remaining to fill as space => 12 spaces

        healthDisplay = ''.join(['-' for i in range(currentDashes)])  # Convert 8 to 8 dashes as a string:   "--------"
        remainingDisplay = ''.join(
            [' ' for i in range(remainingHealth)])  # Convert 12 to 12 spaces as a string and uses a for loop to keep checking: "            "
        percent = str(int((newHealth / maxHealth) * 100)) + "%"  # Get the percent as a whole number:   40%

        print("\x1b[1;31m" + "|" + healthDisplay + remainingDisplay + "|" + "\x1b[0m")  # Print out textbased healthbar
        print("\x1b[1;31m" + "         " + percent + "\x1b[0m")

        #NEED TO IMPLEMENT INTO HEALTH BAR
        if newHealth <= 0:
            path_gameOver()

        """Reactions to beating the enemy"""
        if player_win:
            time.sleep(1.5)
            if newHealth >= 80:
                highHealth = ["That was just a flesh wound.", "It barely hit you!", "You live to fight another day.",
                              "Nobody can best you.", "Word will spread of this battle."]
                print(random.choice(highHealth))
            if newHealth < 80:
                midHealth = ["You stagger backwards having lost a substantial amount of health.",
                             "A valiant fight, but one that has cost you.", "You may not survive another battle."]
                print(random.choice(midHealth))
            if newHealth <= 50:
                lowHealth = ["You are dangerously low on health. Get some rest to restore your health."]
                print(lowHealth)
        XP += 100
        time.sleep(1.5)
        print("     \x1b[1;34m" + "|||UPDATE|||: You have gained 100 Experience Points.", end=" " + "\x1b[0m")
        print("\x1b[1;34m" +f"You now have [{XP}] XP."+ "\x1b[0m")
        gold.append(random.randint(50,100))         #Appends random amoutns of gold to the gold list
        time.sleep(1.5)
        print("     \x1b[1;33m"  +   "|||UPDATE|||: You looted the enemy for 10 gold.", end=" " + "\x1b[0m")
        print("\x1b[1;33m" + f"You now have {sum(gold)} gold." + "\x1b[0m")

        time.sleep(1.5)
        if XP == 100:
            print("     \x1b[1;36m"  +   "|||UPDATE|||: You have obtained the title of Knight!"+ "\x1b[0m")
        if XP == 200:
            print("     \x1b[1;36m"  +   "|||UPDATE|||: You have obtained the title of Baron!"+ "\x1b[0m")
        if XP == 300:
            print("     \x1b[1;36m"  +   "|||UPDATE|||: You have obtained the title of Viscount!"+ "\x1b[0m")

    else:
        print(required)         #if they do not select A or B - loop back to start of section
        combat(enemy)



def merchant():
    print("\nYou're drained from the fight\n"
          "You pass out.\n")
    time.sleep(2)
    print("After a moment, your eyes begin to blink open\n" 
          "A man stares directly at you. His face only 2 inches away from yours, watching your every movement.\n"
          "Deciding not to panic, you only scream on the inside.\n"
          "He continues to stare blankly.\n"
          "Time passes.\n")
    time.sleep(2)
    print("STOP STARING AT ME, YOU'RE MAKING ME UNCOMFORTABLE....\n" 
          "Suddenly, he whips open his robe.\n"
          "MY WARES, CARE TO TAKE A LOOK?")
    time.sleep(1)
    print("""    A. Um...sure
    B. You make me uncomfortable""")
    answer = input(" >>> ")
    if answer in choiceA:
        hiddenSword()
    elif answer in choiceB:
        print("I MAKE YOU UNCOMFORTABLE...you make me uncomfortable...\n"
              "Stop please...you're gonna make me cry\n"
              "LOOK JUST TAKE MY WARES OR GO...\n"
              "Please...\n"
              "You do nothing.\n"
              "The peddler grows even more uncomfortable.\n"
              "Suddenly, he knocks you out\n")
        time.sleep(2)
        merchant()
    else:
        print(required)
        merchant()


def hiddenSword():
    global legendarySword
    print("\nYOU'VE MADE THE RIGHT CHOICE TRAVELER.\n"
          "I HAVE HERE FOR YOU, THE LEGENDARY SWORD OF EXCALIBURN!\n"
          "HOWEVER, THIS BEAUTY DOESN'T COME FOR FREE.\n"
          "GIVE ME 150 GOLD AND THESE BEAUTY IS YOURS.\n"
          "What will you do?")
    time.sleep(1)
    print("""    A. Give him the money
    B. Walk away""")
    answer = input(" >>> ")
    if answer in choiceA:
        sortGold()
        neededGold = 150
        x = 0
        while sum(gold[:x]) < neededGold:       #Uses a while loop to check and stop once the sum of the gold int he list is less than the needed gold and adds the next part of the list
            x += 1
        print("You were able to hand over exactly", sum(gold[:x]), "out of", sum(gold), "gold.")
        legendarySword = 1
        print("You now have the LEGENDARY SWORD OF EXCALIBURN!\n\n")
        time.sleep(1)
        print("While walking you see an opening in the cavern.\n"
              "In the middle of the wide room, there lays the King's Chest!\n"
              "You run over to pick it up but a dragon swoops down.\n")
        time.sleep(1)
        print(f"You have encountered a Dragon\n")
        if legendarySword == 1:
            combat(Boss)
            reportBack()
    elif answer in choiceB:
        print("WHATEVER YOU SAY TRAVELER...\n"
              "BUT JUST A WARNING. YOU MAY FIND YOURSELF IN PERIL WITHOUT MY WARES.\n")
        time.sleep(1)
        print("While walking you see an opening in the cavern.\n"
              "In the middle of the wide room, there lays the King's Chest!\n"
              "You run over to pick it up but a dragon swoops down.\n")
        time.sleep(1)
        if legendarySword == 0:
            print("You try and fight the dragon, but he blows his fiery breath on you!\n"
                  "Too bad.")
            path_gameOver()
    else:
        print(required)
        hiddenSword()


def reportBack():
    if XP == 400:
        print("You decide to report to the king.")
        file = open("DragonSlayer.txt", "w")        #Writes a letter back to the king

        file.write("Your majesty, it is I the newly anointed Viscount reporting back to you.\n")
        file.write("The quest was a success and the enemies were defeated.\n")
        file.write("Thank you for the opportunity to serve you. It was truly an honor.\n")

        file.close()

        time.sleep(1)
        print("\nAfter a while, a crow comes flying towards you with a scroll tied to its feet.\n"
              "It's a message from the King.")

        replyFile = open("Congrats.txt", "r")

        message = replyFile.read()
        print(message)
        time.sleep(2)

        replyFile.close()
        print("     \x1b[1;36m" + "|||UPDATE|||: You have obtained the title of Marquess!" + "\x1b[0m")
        endgame()


def endgame():
    time.sleep(2)
    print("...")

    time.sleep(2)
    print("You find yourself back in the fortune tellers tent. She looks at you, speechless, somewhat fascinated.")
    time.sleep(2)
    print(". . .")
    time.sleep(3)
    print("'YOU HAVE DONE WELL, PEASANT. PERHAPS YOUR FUTURE IS NOT SO BLEAK AFTER ALL.\n"
          "NOW GO FULFILL YOUR FATE AND DO NOT FORGET ABOUT MADAME WOLPH WHEN YOU REACH IT.'")






def path_gameOver():
    playAgain = "yes"
    while playAgain == "yes" or playAgain == "y":
        print("The end is the beginning, yet you go on. Peasant.\n\n\n")
        intro()






intro()




