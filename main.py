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
            numSelections = 8
            print("1 - Display all courses\n2 - Search courses by parameter\n3 - Add/remove courses from system\n4 - Add/ Remove User(s)\n5 - Link Student/instructor to course\n6 - Unlink Student/instructor to course\n7 - Log Out\n8 - Quit")
        # Instructor Selections
        elif (userType == "INSTRUCTOR"):
            numSelections = 6
            print("1 - Display all courses\n2 - Search courses by parameter\n3 - Assemble/Print Course Roster\n4 - Print Semester Schedule\n5 - Log Out\n6 - Quit")

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
                #print semester schedule
                loggedInUser.print_schedule()
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
                # Check semester schedule for conflicts
                loggedInUser.check_for_conflicts()
            elif (userType == "INSTRUCTOR"):
                #logout
                print("Logging Out...")
                defaultlogin(loggedInUser)
            elif (userType == "ADMIN"):
                # Link a student or instructor to a course
                print("1. Link a student to a course\n2. Link an instructor to a course")
                admin_input = ""
                while type(admin_input) != int:
                    try:
                        admin_input = int(input("Enter your selection: "))
                    except:
                        print("Error: Input not an integer")
                if (admin_input > 2) or (admin_input < 1):
                    print("Error: Input out of range. Returning to main menu.")

                if admin_input == 1:
                    loggedInUser.link_student_to_course()
                elif admin_input == 2:
                    loggedInUser.link_instructor_to_course()
            

        elif (userInput == 6):
            #logout
            if (userType == "STUDENT"):
                print("Logging out...")
                defaultlogin(loggedInUser)
            elif userType == "INSTRUCTOR":
                # Quit
                print("Exiting...")
                quit()
            elif (userType == "ADMIN"):
                # Link a student or instructor to a course
                print("1. Unlink a student to a course\n2. Unlink an instructor from a course")
                admin_input = ""
                while type(admin_input) != int:
                    try:
                        admin_input = int(input("Enter your selection: "))
                    except:
                        print("Error: Input not an integer")
                if (admin_input > 2) or (admin_input < 1):
                    print("Error: Input out of range. Returning to main menu.")
                if admin_input == 1:
                    loggedInUser.unlink_student_from_course()
                elif admin_input == 2:
                    loggedInUser.unlink_instructor_from_course()

        elif (userInput == 7):
            #quit
            if (userType == "STUDENT"):
                print("Exiting...")
                quit()

            elif (userType == "ADMIN"):
                    #logout
                    print("Logging Out...")
                    defaultlogin(loggedInUser)

        elif (userInput == 8):
            #quit
            if (userType == "ADMIN"):
                print("Exiting...")
                quit()    

main()