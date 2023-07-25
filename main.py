from classes import *
from databaseFunctions import *

database = sqlite3.connect("database.db")
cursor = database.cursor()

def defaultlogin(loggedInUser):
    loggedInUser = user()
    main()

def main():
    while True:
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        if check_login_credentials(email, password):
            print("Login successful!")
            break
        else:
            print("Invalid email or password. Please try again.")

    tables = ["STUDENT", "ADMIN", "INSTRUCTOR"]
    for i in tables:
        query = "SELECT * FROM " + i + " WHERE EMAIL = '" + email + "'"
        cursor.execute(query)
        userInfo = cursor.fetchall()
        if (len(userInfo) > 0):
            userType = i
            break

    #store all user info in object
    loggedInUser = user()
    if (userType == "STUDENT"):
        loggedInUser = student()
    elif (userType == "ADMIN"):
        loggedInUser = admin()
    elif (userType == "INSTRUCTOR"):
        loggedInUser = instructor()

    loggedInUser.set_id(userInfo[0][0])
    loggedInUser.set_first_name(userInfo[0][1])
    loggedInUser.set_last_name(userInfo[0][2])
    print("Welcome, " + userType + ":")
    loggedInUser.print_info()

    exit = False
    while (exit == False):
        numSelections = 4
        print("1 - Display all courses\n2 - Search courses by parameters")
        if (userType == "STUDENT"):
            print("3 - Add/remove course from semester schedule")
            numSelections = numSelections + 1
        elif (userType == "ADMIN"):
            print("3 - Add/remove courses from system")
            numSelections = numSelections + 1
        elif (userType == "INSTRUCTOR"):
            print("3 - Assemble/Print Course Roster")
            numSelections = numSelections + 1
        if ((userType == "STUDENT") or (userType == "INSTRUCTOR")):
            print("4 - Log Out\n5 - Quit")
        # Admin Selection Options
        elif (userType == "ADMIN"):
            print("4 - Add/ Remove User(s)\n5 - Log Out\n6 - Quit")
            numSelections = numSelections + 1

        userInput = ""
        # Get menu selection from user and check that it's valid
        while type(userInput) != int:
            try:
                userInput = int(input("Enter your selection: "))
            except:
                print("Error: Input not an integer")
        if (userInput > numSelections) or (userInput < 1):
            print("Error: Input out of range (0-" + str(numSelections) + "), please try again")

        if (userInput == 1):
            #display all courses
            print("Selected: Display all courses")
            loggedInUser.print_all_courses()
        elif (userInput == 2):
            #search courses by parameters
            print("Selected: Search for a course")
            loggedInUser.search_for_course()
        elif (userInput == 3):
            if (userType == "STUDENT"):
                #add/remove course from sem. schedule
                loggedInUser.modify_schedule()
            elif (userType == "ADMIN"):
                #add/remove courses from system
                loggedInUser.modify_course()
            elif (userType == "INSTRUCTOR"):
                #assemble/print course roster
                loggedInUser.print_class_list()
        elif (userInput == 4):
            if ((userType == "STUDENT") or (userType == "INSTRUCTOR")):
                print("Logging Out...")
                defaultlogin(loggedInUser)
            elif (userType == "ADMIN"):
                choice = ""
                print("Would you like to add or remove an account?\n1 - Add\n2 - Remove")
                while type(choice) != int:
                    try:
                        choice = int(input("Enter your selection: "))
                    except:
                        print("Error: Input not an integer")
                if (choice > 2) or (choice < 1):
                    print("Error: Input out of range. Please try again")
                if (choice == 1):
                    loggedInUser.add_account()
                elif (choice == 2):
                    loggedInUser.remove_account()
        elif (userInput == 5):
            #quit
            if ((userType == "STUDENT") or (userType == "INSTRUCTOR")):
                print("Exiting...")
                quit()
            elif (userType == "ADMIN"):
                print("Logging Out...")
                defaultlogin(loggedInUser)
        elif (userInput == 6):
            if (userType == "ADMIN"):
                print("Exiting...")
                quit()

main()