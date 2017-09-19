#Simple Calculator for Binary Numbers using the two's complement form.
# input will be in num1 op num2 format, output will be the result of the binary operation.

__author__ = 'Apoorva Chitre'

# query loop defined by the value of choice taken by the user to either continue or exit

choice = "yes"

while choice == "yes" :

    #user is prompted to input the data
    inputData = input("Please enter two 8-bit binary numbers and the operator in number operator number format: ")

    #number 1 number 2 and the operator are extracted from the input string
    index = 0
    for op in inputData :
        if op == "+" or op == "-" or op == "*" or op == "/" :
            break
        index+= 1

    num1 = inputData[:index]
    op = inputData[index]
    num2 = inputData[index+1:]

    error = False

    # function to convert two's complement of input number to it's decimal form

    def twosCompToBin(number) :

        sum = 0
        # for negative number
        if number[0] == "1" :
            for i in range(0,8) :
                if number[i] == "0" :
                    number[i] == "1"
                    sum+= ( 2 ** (7-i) ) * int(number[i])
                elif number[i] == "1" :
                    number[i] == "0"
                    sum+= ( 2 ** (7-i) ) * int(number[i])

            sum += 1
            sum = -(sum)

        # for positive number
        if number[0] == "0" :
            for i in range (0, 8) :
                if number[i] == "0" :
                     sum+= ( 2 ** (7-i) ) * int(number[i])
                elif number[i] == "1" :
                    sum+= ( 2 ** (7-i) ) * int(number[i])

        return sum

    # function to convert decimal number to binary
    def toBinary(num) :
        if num < 2 :
            return num
        else :
            return str(toBinary(num // 2)) + str(num % 2)

    #function to convert decimal to two's complement form
    def decToTwosCompBin (number) :

        #if result is negative
        if number < 0 :
            number = -(number)
            number += 1
            binary = toBinary(number)
            for i in range(len(binary), 8) :
                binary = "0" + binary

            for i in range(0,8) :
                if binary[i] == "0" :
                    binary[i] == "1"

                elif binary[i] == "1" :
                     binary[i] == "0"

            return binary

        # if result is positive
        if number > 0 :
            binary = toBinary(number)
            for i in range (len(binary), 8) :
                binary = "0" + binary

            return binary

    operand1 = twosCompToBin(num1)
    operand2 = twosCompToBin(num2)

    result = 0

    #decimal operations for each operator
    if op == "+" :
        result = operand1 + operand2

    elif op == "-" :
        result = operand1 - operand2

    elif op == "/" :
        # to check divide by zero condition
        if operand2 == 0 :
            print("Incorrect Divide by Zero Operation!")
            error = True
        else :
            result = operand1 // operand2

    elif op == "*" :
        result = operand1 * operand2

    else :
        print ("Invalid Operation")
        error = True


    if not error :
        # to check if result causes overflow or not
        if result < -128 or result > 127 :
            print("Binary Overflow, result out of specified range!")

        else :
            finalresult = decToTwosCompBin(result)
            print("Result of Operation :" , end='\n')
            print(num1,op,num2,"=",finalresult,sep='')

    choice = input("Do you want to continue ? yes or no : ")

    # Sample Output:
    #   Please enter two 8-bit binary numbers and the operator in number operator number format: 00001100 + 00001010
    #   Result of Operation :
    #   00001100 + 00001010=00001100
    #   Do you want to continue ? yes or no : no












































