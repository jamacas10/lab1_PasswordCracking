## Jebel Macias ###
# Lab-1(OPTION C) #
## (9/11/2018) ####
import hashlib
import os.path
from os import path

#Userinput is a method used to acquire 3 inputs.
#This includes the file name containing users, SaltValues
#and passwords, the minimum, and maximum number of digits
#possible in each password. Takes no parameters, and returns
#userInputs into an array.
##############################################################
def userInput():
    userAnswers = [None] * 3
    check0 = 0
    check1 = 0
    check2 = 0
    while check0 == 0:
        userAnswers[0] = (str(input('What is the name of the .txt file that contains the list of users, salt values, and passwords?\n')))
        if path.exists(str(userAnswers[0])):
            check0 = 1
        else:
            print("The file you input does not exist.")
            check0 = 0
    while check1 <= 0:#Assures user input is non-negative
        userAnswers[1] = (str(input('What is the minimum number of digits possible in each passwords?\n')))
        if userAnswers[1].isdigit():#Assures userinput is a number
            check1 = int(userAnswers[1])
        else:
            check1 = 0
    while check2 < check1:#Assures user input is greater than minimum.
        userAnswers[2] = (str(input('What is the max number of digits possible in each passwords?\n')))
        if userAnswers[2].isdigit():
            check2 = int(userAnswers[2])
        else:
            check2 = 0
    return userAnswers

#The method readFromFile takes the fileName, and appends each line
#in the file to an empty array(linesFromFile). Then a 2d array is created
#containing 3 rows, and n(len(linesFromFile)) columns. The first index in each
#line containing userNames, second, saltsValues, third, hashedPasswords. The
#method requires the fileName in its parameters and returns the 2d array(listOfPassWords)
###########################################################################################
def readFromFile(fileName):
    linesFromFile = []
    try:
        with open(fileName, 'r') as file:
            for line in file:
                linesFromFile.append(line)

             listOfPassWords = [[None for x in range(3)]for y in range(len(linesFromFile))]#Defines an array with 3 rows, and n(lines in file) columns
             for line in range(len(linesFromFile)):
                listOfPassWords[line] = linesFromFile[line].strip().split(",", 2)
    except Exception as e:
        print("Failed to load file " + filename + " in method readFromFile.")
        return

    return listOfPassWords

#The recursive method bruteForce seeks to determine the passwords of every
#user in a file by iterating through every possible solution. The method
#contains two base cases, the first determines if all passwords have been solved,
#second, if the minimun number of digits has reached the maximum nmber of digits.
#The method iterates from start to the maxDigit(minimum number of digits currently),
#then iterates through every user in the listOfPasscodes(2d array previous method)
#appending i to each saltvalue and comparing it to each hashed password. If the
#sha256 of the salt value and the current i is equal to a users password, then that
#user is deleted from the list.
###########################################################################
def bruteForce(min, max, maxDigit, listOfPasscodes, solved, start, numberOfPossibleSolutions):
    if solved == numberOfPossibleSolutions:#BaseCase1:Assures not all passcodes have beensolved
        print("Solved all users passcodes!")
        return
    if min>max:#BaseCase2:Assures method does not go beyond max number of digits in a password
        print("Failed to solve all passcodes.:'('")
        return
    else:
        try:
            for i in range(start, maxDigit):#Counter is current number of digits in a single passcode
                for j in range(len(listOfPasscodes)):
                    passWordAttempt = str(i).zfill(min) + str(listOfPasscodes[j][1])#concatentates current string(i) with salt value
                    if(hash_with_sha256(passWordAttempt)==listOfPasscodes[j][2]):
                        print(str(i).zfill(min) + "  " + listOfPasscodes[j][1] + "  " + listOfPasscodes[j][0])
                        solved += 1
                        start = i+1
                        del(listOfPasscodes[j])#deletes user at current index
                        return bruteForce(min, max, maxDigit, listOfPasscodes, solved, start, numberOfPossibleSolutions)

        except Exception as e:
            print("Failed to read through file in method bruteForce, assure file is formatted correctly. [<user>, <saltvalue>, <hashedPassword>]")
            return
        print("###############################")
        print("Finsihed reviewing all " + str(min) + " digit strings." )
        print("Currently solved:" + str(solved) + "\n" + "Unsolved passwords remaining:" + str(numberOfPossibleSolutions-solved))
        print("###############################")
        return bruteForce(min + 1, max, maxDigit * 10, listOfPasscodes, solved, 0, numberOfPossibleSolutions)#Returns next number of digits in a single passcode

#The method hash_with_sha256 generates a hased code using a single, and
#returns a hashed string
def hash_with_sha256(str):
    hash_object = hashlib.sha256(str.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

#The method main calls all other methods in the program, and defnines
#the beginning digit length by using the minimum value.
def main():
    userAnswers = userInput()
    fileName = userAnswers[0]
    min = int(userAnswers[1])
    max = int(userAnswers[2])
    listOfPasswords = readFromFile(userAnswers[0])
    counter = ""
    try:
        for i in range(min):
            counter += "9"
        print("Password  SaltValue  User")
        bruteForce(min, max, int(counter)+1, listOfPasswords, 0, 0, len(listOfPasswords))
    except Exception as e:
        print("Failed during the method main, assure file is formatted correctly. [<user>, <saltvalue>, <hashedPassword>]")

main()
