from poplib import CR
import sqlite3
from subprocess import CREATE_NEW_PROCESS_GROUP

database = sqlite3.connect("Assignment3/assignment3.db")
cursor = database.cursor()

def create_table():
    print("Creating a new table.")
    tableName = input("Enter table name: ")
    numAttributes = ""
    while (type(numAttributes) != int):
        try:
            numAttributes = int(input("Enter number of attributes for the table: "))
        except: 
            print("Error: Input not an integer")
    if (numAttributes <= 0):
        print("Number of attributes not a positive integer, cancelling table creation")
        return
    print(numAttributes)
    createCmd = """CREATE TABLE """ + tableName + """ (  """ + input("Enter name of the key value attribute for the table: ") + """ PRIMARY KEY NOT NULL,"""
    for i in range(2, numAttributes+1):
        print("Attribute #" + str(i))
        textOrNumber = ""
        while (textOrNumber != 1 and textOrNumber != 2):
            textOrNumber = int(input("Enter a 1 for the attribute to be text, or a 2 for it to be a number: "))
            while type(textOrNumber) != int:
                try:
                    textOrNumber = int(input("Try again: "))
                except:
                    print("Error: Input not an integer")
        textOrNumberStr = ""
        if textOrNumber == 1:
            print("Selected: TEXT")
            textOrNumberStr == " TEXT"
        else:
            print("Selected: NUMBER")
            textOrNumberStr = " NUMBER"
        createCmd = createCmd + input("Attribute name: ") + textOrNumberStr + " NOT NULL"
        if i != numAttributes:
            createCmd = createCmd + ""","""
        else:
            createCmd = createCmd + """);"""

    try:
        cursor.execute(createCmd)
    except:
        print("Table " + tableName + " already exists.")

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

def insert_data():
        table_name = input("Enter the table name (ADMIN, INSTRUCTOR, STUDENT, COURSE): ")
        if table_name not in ["ADMIN", "INSTRUCTOR", "STUDENT", "COURSE"]:
            print("Error: Invalid table name")
            return
        attributes = []
        if table_name == "ADMIN":
            attributes = ["ID", "NAME", "SURNAME", "TITLE", "OFFICE", "EMAIL"]
        elif table_name == "INSTRUCTOR":
            attributes = ["ID", "NAME", "SURNAME", "TITLE", "HIREYEAR", "DEPT", "EMAIL"]
        elif table_name == "STUDENT":
            attributes = ["ID", "NAME", "SURNAME", "GRADYEAR", "MAJOR", "EMAIL"]
        else:
            attributes = ["CRN", "TITLE", "DEPT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS"]

        data = "("
        counter = 0
        for i in attributes:
            data = data + "'" + str(input("Enter " + i + ": ")) + "'"
            if counter != len(attributes) - 1:
                 data = data + ", "
            counter = counter + 1
        data = data + ")"

        try:
            cursor.execute(f"INSERT INTO {table_name} VALUES {data}")
            database.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error: Failed to insert data.")
            print(e)

def delete_data():
    print("Selected: Delete Data")
    databases = ["ADMIN", "INSTRUCTOR", "STUDENT", "COURSE"]
    databasesKeyVal = ["ID", "ID", "ID", "CRN"]
    counter = 0
    for i in databases:
        print (str(counter) + " - " + str(i))
        counter = counter + 1
    try:
        dbSelection = int(input("Select database to delete input from (0-3 or Q to quit): "))
    except:
        print("Returning to main function")
        return
    if (dbSelection > 3) or (dbSelection < 0):
        print("Input out of range, returning to main function")
        return
    try: 
            deleteSelection = input("Enter the key value of the item you'd like to delete, or Q to quit: ")
    except:
        print("Returning to main function")
        return
    deleteText = "DELETE FROM " + databases[dbSelection] + " WHERE " + databasesKeyVal[dbSelection] + " = " + deleteSelection;
    cursor.execute(deleteText)

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

    # Create new table - Selection 0
    if userInput == 0:
        create_table()
    # Search by Parameter - Selection 1
    elif userInput == 1:
        search()
    # Insert new data to table - Selection 2
    elif userInput == 2:
        insert_data()
    # Update data in table - Selection 3
    elif userInput == 3:
        pass
    # Remove data from table - Selection 4
    elif userInput == 4:
        delete_data()
    # Print all tables - Selection 5
    elif userInput == 5:
        print_tables()
    # Exit program - Selection 6
    elif userInput == 6:
        user_input = input("Are you sure you'd like to exit? (Y/N): ")
        if user_input == "Y" or user_input == "y":
            print("Exiting")
            exit = True
        else:
            exit = False

database.commit()

database.close()