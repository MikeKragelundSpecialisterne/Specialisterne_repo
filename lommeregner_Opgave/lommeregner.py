import math
sqrt = False
def getUserInputs():
    #User inputs
    sqrtinput = input("Vil du finde kvadratrod? Y/N")
    print(sqrtinput)
    if sqrtinput == "Y" or sqrtinput == "y":
        sqrt = True
    else: 
        sqrt = False
    while True: 
        if sqrt == True:
            firstNumber = input("Skriv tallet du vil have kvadratrodden af")
        else:
            firstNumber = input("Skriv dit første tal! \n",)
        checkForQuit(firstNumber)
        try:
            firstNumber = float(firstNumber)
        except ValueError:
            print("indtast venligst et nummer")
            continue
        if not sqrt:
            secondNumber = input("Skriv dit andet tal! \n",)
            checkForQuit(firstNumber)
            try:
                secondNumber = float(secondNumber)
            except ValueError:
                print("indtast venligst et nummer")
                continue

            userAction = input("Skriv + - / * ** sqrt for at vælge action \n")
            checkForQuit(userAction)
        if sqrt:
            userAction = "sqrt"
            secondNumber = 0
         
        return userAction, firstNumber, secondNumber

#Checking for  zero division.
def DevidedZero(firstNumber, secondNumber, userAction):
    if(userAction == "/"):
        if(firstNumber or secondNumber == 0):
            return "Vi skal ikke dividere med 0, så bryder universet sammen...!!!"

#Validating the choosen user action
def UserActionValidation(userAction):
    actions = "+-/**sqrt"
    if userAction in actions:
        return True
    else:
        return False
    
def changeUserOperation(userAction): 
    nyUserAction = userAction
    #Message to user, and allow them to change operation in a loop
    if(UserActionValidation(userAction) == False):
        print("Du har angivet en udefinerbar operation. indtast en ny")
        while  UserActionValidation(nyUserAction) is False:
            nyUserAction = input("Skriv en operation \n");
            checkForQuit(nyUserAction)
    return nyUserAction

def calc(userAction, firstNumber, secondNumber):
    #Variabel for result
    result =0
    if userAction == "+":
        result = firstNumber + secondNumber
    elif userAction == "-":
        result = firstNumber - secondNumber
    elif userAction == "*":
        result = firstNumber * secondNumber
    elif userAction == "/":
        result = firstNumber / secondNumber
    elif userAction == "**":
        result = firstNumber ** secondNumber
    elif userAction =="sqrt":
        result = math.sqrt(firstNumber)
    
    #Return the result    
    return float(result)

def checkForQuit(input):
    if input == "q":
        print("Vi ses makker!")
        quit()

def calculatorApp():
    print("Lommeregner app!")
    print("Tryk q for lukning af programmet.")
    userAction, firstNumber, secondNumber = getUserInputs()
    #tjekker for  korrekt operation input 
    userAction = changeUserOperation(userAction)
    #Tjekker for 0 division
    DevidedZero(firstNumber, secondNumber, userAction)

    print("DIT RESULTAT ER!!! \n")
    print(calc(userAction, firstNumber,secondNumber))
    
#initialisere boolean til app funktion.  
stayAlive = True
while stayAlive == True: 
    calculatorApp()
    keepGoing = input("Vil du gerne lave en ny beregning? Y/N")
    checkForQuit(keepGoing)
    
    if keepGoing == "y":
        stayAlive = True
    else: 
        stayAlive = False