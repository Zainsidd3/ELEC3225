import sqlite3

database = sqlite3.connect("Assignment3/assignment3.db")
cursor = database.cursor()

def print_tables():
    print("Printing all tables")
    databases = ["ADMIN", "INSTRUCTOR", "STUDENT", "COURSE"]
    for i in databases:
        try:
            print("\nPrinting table " + i)
            cursor.execute("SELECT * FROM " + i)
            query_result = cursor.fetchall()
            for j in query_result:
                print(j)
        except:
            print("Error: Missing table " + i + ", continuing.")

def search():
    print("What would you like to search for?\n1 - ADMIN\n2 - INSTRUCTOR\n3 - STUDENT\n4 - COURSE")
    userInput1 = ""
    while (type(userInput1) != int):
        try:
            userInput1 = int(input("Enter your selection: "))
        except: 
            print("Error: Input not an integer")
        if (userInput1 > 4) or (userInput1 < 1):
            print("Error: Input out of range (1-4), please try again")

    # Search Admin table
    if userInput1 == 1:
        print("ADMIN")
        adminAtt = ["ID", "NAME", "SURNAME", "TITLE", "OFFICE", "EMAIL"]
        counter = 0

        for i in adminAtt:
            print(str(counter) + " - " + str(i))
            counter = counter + 1

        userInput1 = ""
        while (type(userInput1) != int):
            try:
                userInput1 = int(input("Enter your selection: "))
            except: 
                print("Error: Input not an integer")
            if (userInput1 > 5) or (userInput1 < 0):
                print("Error: Input out of range (0-5), please try again")

        print(adminAtt[userInput1])

        queryVal = str(input("Enter Value: "))

        cursor.execute("""SELECT * FROM ADMIN WHERE """ + adminAtt[userInput1] + """ = '""" + queryVal + """'""")
        query_result = cursor.fetchall()

        for i in query_result:
	        print(i)
        
    # Search Instructor table
    elif userInput1 == 2:
        print("INSTRUCTOR")
        instructAtt = ["ID", "NAME", "SURNAME", "TITLE", "HIREYEAR", "DEPT", "EMAIL"]
        counter = 0

        for i in instructAtt:
            print(str(counter) + " - " + str(i))
            counter = counter + 1

        userInput1 = ""
        while (type(userInput1) != int):
            try:
                userInput1 = int(input("Enter your selection: "))
            except: 
                print("Error: Input not an integer")
            if (userInput1 > 6) or (userInput1 < 0):
                print("Error: Input out of range (0-6), please try again")

        print(instructAtt[userInput1])

        queryVal = input("Enter Value: ")

        cursor.execute("""SELECT * FROM INSTRUCTOR WHERE """ + instructAtt[userInput1] + """ = '""" + queryVal + """'""")
        query_result = cursor.fetchall()

        for i in query_result:
	        print(i)

    # Search Student table
    elif userInput1 == 3:
        print("STUDENT")
        studentAtt = ["ID", "NAME", "SURNAME", "GRADYEAR", "MAJOR", "EMAIL"]
        counter = 0

        for i in studentAtt:
            print(str(counter) + " - " + str(i))
            counter = counter + 1

        userInput1 = ""
        while (type(userInput1) != int):
            try:
                userInput1 = int(input("Enter your selection: "))
            except: 
                print("Error: Input not an integer")
            if (userInput1 > 5) or (userInput1 < 0):
                print("Error: Input out of range (0-5), please try again")

        print(studentAtt[userInput1])

        queryVal = input("Enter Value: ")

        cursor.execute("""SELECT * FROM STUDENT WHERE """ + studentAtt[userInput1] + """ = '""" + queryVal + """'""")
        query_result = cursor.fetchall()

        for i in query_result:
	        print(i)

    # Search COURSE table
    elif userInput1 == 4:
        print("COURSE")
        courseAtt = ["CRN", "TITLE", "DEPT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS"]
        counter = 0

        for i in courseAtt:
            print(str(counter) + " - " + str(i))
            counter = counter + 1

        userInput1 = ""
        while (type(userInput1) != int):
            try:
                userInput1 = int(input("Enter your selection: "))
            except: 
                print("Error: Input not an integer")
            if (userInput1 > 7) or (userInput1 < 0):
                print("Error: Input out of range (0-7), please try again")

        print(courseAtt[userInput1])

        queryVal = input("Enter Value: ")

        cursor.execute("""SELECT * FROM COURSE WHERE """ + courseAtt[userInput1] + """ = '""" + queryVal + """'""")
        query_result = cursor.fetchall()

exit = False
def insert_data():
        table_name = input("Enter the table name (ADMIN, INSTRUCTOR, STUDENT): ")
        if table_name not in ["ADMIN", "INSTRUCTOR", "STUDENT"]:
            print("Error: Invalid table name")
        
            id = input("Enter ID: ")
            name = input("Enter Name: ")
            surname = input("Enter Surname: ")
            grad_year = input("Enter Graduation Year: ")
            major = input("Enter Major: ")
            email = input("Enter Email: ")

        data = f"('{id}', '{name}', '{surname}', '{grad_year}', '{major}', '{email}')"
        try:
            cursor.execute(f"INSERT INTO {table_name} VALUES {data}")
            database.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error: Failed to insert data.")
            print(e)
exit = False
while (exit == False):
    print("0 - Create new table\n1 - Search by parameter\n2 - Insert new entry to table\n3 - Update existing table entry\n4 - Remove existing table entry\n5 - Print all tables\n6 - Exit")
    userInput = ""
    while type(userInput) != int:
        try:
            userInput = int(input("Enter your selection: "))
        except:
            print("Error: Input not an integer")
    if (userInput > 6) or (userInput < 0):
        print("Error: Input out of range (0-6), please try again")

    if userInput == 0:
        pass

    # Search by Parameter - Selection 1
    elif userInput == 1:
        search()
    elif userInput == 2:
        insert_data()
    elif userInput == 3:
        pass
    elif userInput == 4:
        pass
    elif userInput == 5:
        print_tables()
    elif userInput == 6:
        user_input = input("Are you sure you'd like to exit? (Y/N): ")
        if user_input == "Y" or user_input == "y":
            print("Exiting")
        else:
            exit = False