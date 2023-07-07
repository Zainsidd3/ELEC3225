from classes import *
from databaseFunctions import *

database = sqlite3.connect("database.db")
cursor = database.cursor()

#login stuff goes here
userEmail = "mcfetridgee"

#search student/admin/instructor tables to find a matching email to the one that logged in
tables = ["STUDENT", "ADMIN", "INSTRUCTOR"]
for i in tables:
    query = "SELECT * FROM " + i + " WHERE EMAIL = '" + userEmail + "'"
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
print("Login successful. Welcome, " + userType + ":")
loggedInUser.print_info()

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
print("4 - Quit")

