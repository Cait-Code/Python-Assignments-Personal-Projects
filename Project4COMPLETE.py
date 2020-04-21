class Pizza:

    def __init__(self, size, crust, sauce, toppings):
        self.size = size
        self.crust = crust
        self.sauce = sauce
        self.toppings = toppings

    def __getSize(self):
        try:
            while True:
                sizeOfPizza = input("What size pizza do you want? (S)mall, (M)edium, or (L)arge ")
                if sizeOfPizza not in ("s", "S", "l", "L", "m", "M"):
                    print("That is not a size we have. Try again")
                else:
                    break
        except:
            pass

        return sizeOfPizza

    def __getCrust(self):
        try:
            while True:
                crustOfPizza = input("What curst do you want? (H)and-tossed, (T)hin, (C)heese Stuffed or (D)eep Dish ")
                if crustOfPizza not in ("H", "h", "T", "t", "C", "c", "D", "d"):
                    print("That is not a curst we have. Try again")
                else:
                    break
        except:
            pass

        return crustOfPizza

    def __getSauce(self):
        try:
            while True:
                sauceOfPizza = input("How much sauce do you want? (N)one, (E)xtra, or (L)ight ")
                if sauceOfPizza not in ("N", "n", "E", "e", "L", "l"):
                    print("That is not a level of sauce we have. Try again")
                else:
                    break
        except:
            pass

        return sauceOfPizza

    def __getToppings(self):

        toppingsOfPizza = []
        print(
            "(E)xtra cheese, (M)ushrooms, (G)oat cheese\n(T)omatoes, (P)ineapple, (F)resh veggies\n(K)alamata olives, (G)reen olives, (B)lack olives\nB(A)con, Pepperon(I), (H)am, Bee(F)")
        try:
            while True:
                choice = input("Enter a topping or done: ")
                choice = choice.upper()
                if choice in ("E", "M", "G", "T", "P", "F", "K", "G", "B", "A", "I", "H", "F"):
                    toppingsOfPizza.append(choice)
                elif choice == 'DONE':
                    break
                else:
                    print("That is not a valid input. Try again.")
        except:
            pass

        return toppingsOfPizza


def makeOrder(pizzaSize, pizzaCrust, pizzaSauce, pizzaToppings):
    thisOrder = []
    thisOrder.append(pizzaSize)
    thisOrder.append(pizzaCrust)
    thisOrder.append(pizzaSauce)
    thisOrder.append(pizzaToppings)

    return thisOrder


if __name__ == "__main__":

    orderList = []
    unfinished = True
    orderNum = 0

    while True:
        print("Welcome to Pie in the Sky Pizza Shoppe!")
        whatToDo = input("(O)rder a pizza\n(F)inish an order \n(D)isplay un-finished orders\n(E)xit\n")
        if whatToDo in ("o", "O"):
            orderNum += 1
            size, crust, sauce, toppings = '', '', '', ''
            order = Pizza(size, crust, sauce, toppings)
            size = order._Pizza__getSize()
            crust = order._Pizza__getCrust()
            sauce = order._Pizza__getSauce()
            toppings = order._Pizza__getToppings()
            thisOrder = makeOrder(size, crust, sauce, toppings)
            print('This order number is',orderNum)
            orderList.append(orderNum)
        elif whatToDo in ("f", "F"):
            while True:
                number = input("Please enter the order number: ")
                number = int(number)
                if number in orderList:
                    orderList.remove(number)
                    break
                else:
                    print("That is not a valid order number. Try again")
        elif whatToDo in ("D", "d"):
            if len(orderList) == 0:
                print("All orders complete")
            else:
                print(*orderList, "is not complete.")
        elif whatToDo in ("e", "E"):
            break
        else:
            print("Type an O, F, D, or E")