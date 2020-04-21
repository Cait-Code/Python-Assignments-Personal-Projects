def main():
    print("Ooh-de-la-lay! Ooh-de-la-lay! Fortune tellers!\n"
          "Fortunes forecast! Lucky charms!")
    name = input("Hmmm... the future is cloudy. What is your name?")
    howMany = eval(input("Oo-dee-lally! How exciting! How many fortunes do you wish to get today?"))
    priceFortune = howMany * 1.99
    taxFortune = priceFortune*0.09
    print("Your total for today's session will be:", (priceFortune + taxFortune))
    luckyNumbers = eval(input("I will tell your fortune."+" "+name+ "," +" "+"enter your lucky integer number."))
    fortuneList = []
    for num in range(howMany):
        if (luckyNumbers <0 or luckyNumbers >100):
            luckyNumbers = eval(input("Oops"+" "+name+ ". I cannot tell your fortune until you enter a valid number."))
        if (0<= luckyNumbers <= 100):
            fortuneList.append(luckyNumbers)
            wrap = luckyNumbers % 10
        if (luckyNumbers == 10 or luckyNumbers == 0 or luckyNumbers == 100):
            wrap = 10
        if (wrap == 1):
            print(name+"! This is your lucky day!")
            print("You will get an A")
        if (wrap == 2):
            print(name+"! This is your lucky day!")
            print("You will learn to program")
        if (wrap == 3):
            print(name+"! This is your lucky day!")
            print("You are destined to become a master coder")
        if (wrap == 4):
            print(name+"! This is your lucky day!")
            print("May the force be with you")
        if (wrap == 5):
            print(name+"! This is your lucky day!")
            print("Wow. You look like a programmer")
        if (wrap == 6):
            print(name+"! This is your lucky day!")
            print("The code is strong with this one")
        if (wrap == 7):
            print(name+"! This is your lucky day!")
            print("You will be testing your code often")
        if (wrap == 8):
            print(name+"! This is your lucky day!")
            print("Taco cat spelled backwards is taco cat")
        if (wrap == 9):
            print(name+"! This is your lucky day!")
            print("Your name will go down, down, down in history")
        if (wrap == 10):
            print(name+"! This is your lucky day!")
            print("You will master python")
        if (num == howMany -1):
            break
        luckyNumbers = eval(input("I will tell your fortune."+" "+ name +"," +" "+"enter your lucky integer number."))

    print("You entered the following lucky numbers:")
    print(fortuneList)






main()