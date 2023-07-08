from classes import *
from databaseFunctions import *

database = sqlite3.connect("database.db")
cursor = database.cursor()

# ADDING USER INFO TO LOGINS TABLE
#def add_login(email, password):
#    # Insert the email and password into the LOGINS table
#    cursor.execute("INSERT INTO LOGINS (ID, PASSWORD) VALUES (?, ?)", (email, password))
#    database.commit()

#def add_new_login():
#    email = input("Enter new email address: ")
#    password = input("Enter the password for new account: ")

#    add_login(email, password)
#    print("Login details added to the LOGINS table.")

#while True:
#    add_new_login()

#    choice = input("Continue? (y/n): ")
#    if choice.lower() != 'y':
#        break

# LOGIN STUFF
def check_login_credentials(email, password):
    # Check if the email and password match in the LOGINS table
    cursor.execute("SELECT COUNT(*) FROM LOGINS WHERE ID=? AND PASSWORD=?", (email, password))
    login_count = cursor.fetchone()[0]

    if login_count > 0:
        return True
    else:
        return False

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
        numSelections = 3
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
        print("4 - Log Out")
        print("5 - Quit")

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
            print_table("COURSE")
        elif (userInput == 2):
            #search courses by parameters
            search("COURSE")
        elif (userInput == 3):
            if (userType == "STUDENT"):
                #add/remove course from sem. schedule
                pass
            elif (userType == "ADMIN"):
                #add/remove courses from system
                delete_data("COURSE")
            elif (userType == "INSTRUCTOR"):
                #assemble/print course roster
                pass
        elif (userInput == 4):
            print("Logging Out...")
            break
        else:
            #quit
            exit = True
            print("Exiting...")

main()