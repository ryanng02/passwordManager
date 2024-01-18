from encrypt import AES256
from save import Saver
import os

masterPasswordCheck = b'rO7eHaBy39Ij9aiMmSYLKVgokztzeThXzlv2puiU/SM='

saver = Saver("passwords.txt")
passwords = saver.read()
loggedIn = False

while True: #if you are not logged in you have to input your master password
    if not loggedIn:
        print("Master Password: ", end="")
        masterPassword = input()

        encrypter = AES256(masterPassword)

        if encrypter.encrypt("textToMatch") != masterPasswordCheck:
            print("Password Incorrect!")
            input()
            continue #going back up
        else:
            loggedIn = True

    os.system("cls") #clearing the console after everything

    print("1. Find Password")
    print("2. Add Password")
    print("3. Delete Password")

    print("\nChoice: ", end="")
    choice = int(input()) #allows input and convert into integer

    if choice <1 or choice >3:
        print("Choice needs to be a number between 1 - 3")
        input()
        continue

    print("Application Name: ", end="")
    app = input()

    if choice == 1:
        for entry in passwords:
            if app in encrypter.decrypt(entry[0]): #if input above is inside of password then we are going to print
                print("\n--------------------------------------------")
                print(f"Application: {encrypter.decrypt(entry[0])}")
                print(f"Password: {encrypter.decrypt(entry[1])}")
        input()

    elif choice == 2:
        print("Password: ", end="")
        password = input()

        passwords.append([encrypter.encrypt(app).decode(),encrypter.encrypt(password).decode()]) #set as string instead of byte
        saver.save(passwords)

    elif choice == 3:
        for entry in passwords:
            if app == encrypter.decrypt(entry[0]):
                print(f"Are you sure you want to delete '{app}' [y/n]: ", end ="")
                confirm = input()

                if confirm == "y":
                    del passwords [passwords.index(entry)]
                    saver.save (passwords)

                break