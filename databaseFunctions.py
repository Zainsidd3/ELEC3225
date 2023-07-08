import sqlite3

def check_login_credentials(email, password):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    # Check if the email and password match in the LOGINS table
    cursor.execute("SELECT COUNT(*) FROM LOGINS WHERE ID=? AND PASSWORD=?", (email, password))
    login_count = cursor.fetchone()[0]

    if login_count > 0:
        return True
    else:
        return False
    database.commit()
    database.close()

def create_table():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
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
    database.commit()
    database.close()

def print_tables():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
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
    database.commit()
    database.close()

#print one table
def print_table(table):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM " + table)
    query_result = cursor.fetchall()
    for j in query_result:
        print(j)
    database.commit()
    database.close()

def search(table):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    # Search Admin table
    if table == "ADMIN":
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
        
    # Search Instructor table
    elif table == "INSTRUCTOR":
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

    # Search Student table
    elif table == "STUDENT":
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

    # Search COURSE table
    elif table == "COURSE":
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
    print("Results found: " + str(len(query_result)))
    for i in query_result:
        print(i)
    database.close()

def insert_data():
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
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
        database.commit()
        database.close()

def update_data():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    print("Selected: Update Data")
    databases = ["ADMIN", "INSTRUCTOR", "STUDENT", "COURSE"]
    databasesKeyVal = ["ID", "ID", "ID", "CRN"]
    counter = 0
    for i in databases:
        print (str(counter) + " - " + str(i))
        counter = counter + 1
    try:
        dbSelection = int(input("Select database to update input from (0-3 or press Q to quit): "))
    except:
        print("Returning to main function")
        return
    if (dbSelection > 3) or (dbSelection < 0):
        print("Input out of range 0-3, returning to main function and try again")
        return
    try: 
        ("UPDATE ADMIN SET title = 'Vice-President' WHERE id=30002;")

    except:
        print("Returning to main function")
        return
    if (dbSelection == 0):
        ("UPDATE ADMIN SET title = 'Vice-President' WHERE id=30002;")
        print("ADMIN Title Was Succesfully Updated")
        return            
    database.commit()
    database.close()

def delete_data():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
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
    database.commit()
    database.close()

def delete_data(table):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    if (table == "COURSE"):
        databasesKeyVal = "CRN"
    else:
        databasesKeyVal = "ID"
    deleteSelection = input("Enter the " + databasesKeyVal + " of the item you'd like to delete, or Q to quit: ")
    if (deleteSelection == "Q"):
        print("Returning to main menu")
        return
    deleteText = "DELETE FROM " + table + " WHERE " + databasesKeyVal + " = '" + deleteSelection + "'";
    cursor.execute(deleteText)
    database.commit()
    database.close()


def match_instructors():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    print("Selected: Match instructors to courses")
    courseCRN = str(input("Enter course CRN to find potential instructors: "))
    cursor.execute("""SELECT * FROM COURSE WHERE CRN = '""" + courseCRN + """'""")
    query_result = cursor.fetchall()
    if (len(query_result) == 1):
        print("Selected course:")
        print(query_result[0])
    else:
        print("No course found, returning to main.")
        return

    print("Finding potential professors for course #" + courseCRN + "...")
    cursor.execute("""SELECT * FROM INSTRUCTOR WHERE DEPT = '""" + query_result[0][2] + """'""")
    query_result = cursor.fetchall()
    if (len(query_result) == 0):
        print("No matching professors found in database.")
        return
    for i in query_result:
        print(i)
    database.commit()
    database.close()

def add_remove(table):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    
    if table == "COURSE":
        databasesKeyVal = "CRN"
    else:
        databasesKeyVal = "ID"

    operation = input("Enter 'add' to add a course or 'remove' to remove a course: ")

    if operation == "add":
        # Check if the course already exists
        deleteSelection = input("Enter the " + databasesKeyVal + " of the course you'd like to add: ")
        cursor.execute("SELECT * FROM " + table + " WHERE " + databasesKeyVal + " = ?", (deleteSelection,))
        existing_course = cursor.fetchone()

        if existing_course:
            print("Course already exists in the table.")
        else:
            attributes = []
            if table == "ADMIN":
                attributes = ["ID", "NAME", "SURNAME", "TITLE", "OFFICE", "EMAIL"]
            elif table == "INSTRUCTOR":
                attributes = ["ID", "NAME", "SURNAME", "TITLE", "HIREYEAR", "DEPT", "EMAIL"]
            elif table == "STUDENT":
                attributes = ["ID", "NAME", "SURNAME", "GRADYEAR", "MAJOR", "EMAIL"]
            elif table == "COURSE":
                attributes = ["CRN", "TITLE", "DEPT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS"]
            else:
                print("Invalid table name.")
                return

            data = "("
            counter = 0
            for attr in attributes:
                value = input(f"Enter {attr}: ")
                data = data + f"'{value}'"
                if counter != len(attributes) - 1:
                    data = data + ", "
                counter = counter + 1
            data = data + ")"

            try:
                cursor.execute(f"INSERT INTO {table} VALUES {data}")
                database.commit()
                print("Course added successfully.")
            except Exception as e:
                print("Error: Failed to add the course.")
                print(e)

    elif operation == "remove":
        deleteSelection = input("Enter the " + databasesKeyVal + " of the course you'd like to remove: ")
        cursor.execute("SELECT * FROM " + table + " WHERE " + databasesKeyVal + " = ?", (deleteSelection,))
        existing_course = cursor.fetchone()

        if existing_course:
            cursor.execute("DELETE FROM " + table + " WHERE " + databasesKeyVal + " = ?", (deleteSelection,))
            database.commit()
            print("Course removed successfully.")
        else:
            print("Course not found in the table.")
    else:
        print("Invalid operation.")

    database.close()






#exit = False
#while (exit == False):
#    print("0 - Create new table\n1 - Search by parameter\n2 - Insert new entry to table\n3 - Update existing table entry\n4 - Remove existing table entry\n5 - Print all tables\n6 - Match courses to potential intructors\n7 - Exit")
#    userInput = ""
#    # Get menu selection from user and check that it's valid
#    while type(userInput) != int:
#        try:
#            userInput = int(input("Enter your selection: "))
#        except:
#            print("Error: Input not an integer")
#    if (userInput > 7) or (userInput < 0):
#        print("Error: Input out of range (0-7), please try again")

#    # Create new table - Selection 0
#    if userInput == 0:
#        create_table()

#    # Search by Parameter - Selection 1
#    elif userInput == 1:
#        search()

#    # Insert new data to table - Selection 2
#    elif userInput == 2:
#        insert_data()

#    # Update data in table - Selection 3
#    elif userInput == 3:
#        update_data()

#    # Remove data from table - Selection 4
#    elif userInput == 4:
#        delete_data()

#    # Print all tables - Selection 5
#    elif userInput == 5:
#        print_tables()

#    # Match instructors to courses - Selection 6
#    elif userInput == 6:
#        match_instructors()

#    # Exit program - Selection 7
#    elif userInput == 7:
#        user_input = input("Are you sure you'd like to exit? (Y/N): ")

#        if user_input == "Y" or user_input == "y":
#            print("Exiting")
#            exit = True
#        else:
#            exit = False