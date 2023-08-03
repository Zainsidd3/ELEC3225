from classes import *
from databaseFunctions import *

database = sqlite3.connect("database.db")
cursor = database.cursor()

# logout current user and return to main
def defaultlogin(loggedInUser):
    loggedInUser = user()
    main()

def main():
    #login loop
    while True:
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        if check_login_credentials(email, password):
            print("Login successful!")
            break
        else:
            print("Invalid email or password. Please try again.")

    # find user type and pull their info from db
    tables = ["STUDENT", "ADMIN", "INSTRUCTOR"]
    for i in tables:
        query = "SELECT * FROM " + i + " WHERE EMAIL = '" + email + "'"
        cursor.execute(query)
        userInfo = cursor.fetchall()
        if (len(userInfo) > 0):
            userType = i
            break

    #store all user info in object corresponding to user type
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
        # Student Selections
        if (userType == "STUDENT"):
            numSelections = 7
            print("1 - Display all courses\n2 - Search courses by parameter\n3 - Add/remove course from semester schedule\n4 - Check semester schedule\n5 - Check semester schedule for conflicts\n6 - Log Out\n7 - Quit")
        # Admin Selections
        elif (userType == "ADMIN"):
            numSelections = 6
            print("1 - Display all courses\n2 - Search courses by parameter\n3 - Add/remove courses from system\n4 - Add/ Remove User(s)\n5 - Log Out\n6 - Quit")
        # Instructor Selections
        elif (userType == "INSTRUCTOR"):
            numSelections = 5
            print("1 - Display all courses\n2 - Search courses by parameter\n3 - Assemble/Print Course Roster\n4 - Log Out\n5 - Quit")

        userInput = ""
        # Get menu selection from user and check that it's valid
        while type(userInput) != int:
            try:
                userInput = int(input("Enter your selection: "))
            except:
                print("Error: Input not an integer")
        if (userInput > numSelections) or (userInput < 1):
            print("Error: Input out of range (0-" + str(numSelections) + "), please try again")

        # Display all courses
        if (userInput == 1):
            print("Selected: Display all courses")
            loggedInUser.print_all_courses()
        # Search courses by parameters
        elif (userInput == 2):
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
            if (userType == "STUDENT"):
                #print semester schedule
                loggedInUser.print_schedule()
            elif (userType == "INSTRUCTOR"):
                #logout
                print("Logging Out...")
                defaultlogin(loggedInUser)
            elif (userType == "ADMIN"):
                #add/remove an account from system
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
            if (userType == "STUDENT"):
                #check semester schedule for conflicts
                loggedInUser.check_for_conflicts()
            elif (userType == "INSTRUCTOR"):
                #quit
                print("Exiting...")
                quit()
            elif (userType == "ADMIN"):
                #logout
                print("Logging Out...")
                defaultlogin(loggedInUser)

        elif (userInput == 6):
            #logout
            if (userType == "STUDENT"):
                print("Logging out...")
                defaultlogin(loggedInUser)
            #quit
            elif (userType == "ADMIN"):
                print("Exiting...")
                quit()

        elif (userInput == 7):
            #quit
            if (userType == "STUDENT"):
                print("Exiting...")
                quit()
            
main()