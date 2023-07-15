from calendar import c
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
    if (table == "COURSE"):
        cursor.execute("SELECT * FROM COURSE")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        column_names = column_names[:-1]
        print(column_names)
        for row in rows:
            row_values = row[:-1]
            print(row_values)
    else:
        cursor.execute("SELECT * FROM " + table)
        query_result = cursor.fetchall()
        for j in query_result:
            print(j)
    database.commit()
    database.close()

def search(table, attribute, query):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    
    try:
        cursor.execute("""SELECT * FROM """ + table + """ WHERE """ + attribute + """ = '""" + query + """'""")
    except:
        raise TypeError("Error in search()")

    query_result = cursor.fetchall()

    return query_result

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

def add_data(table):
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


#returns True if student successfully added to roster, False otherwise
def add_to_roster(studentID, courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()
    if (course == None):
        print("Error in add_to_roster(): courseCRN " + str(courseCRN) + " not found.")
        return False
    if (check_if_student_in_roster(studentID, courseCRN)):
        print("Error in add_to_roster(): Student ID#" + str(studentID) + " already in course #" + str(courseCRN))
        return False
    courseRoster = course[9]
    if (courseRoster == None):
        courseRoster = ""
    newCourseRoster = courseRoster + str(studentID) + ","
    cursor.execute("UPDATE COURSE SET ROSTER = '" + newCourseRoster + "' WHERE CRN = '" + courseCRN + "'")
    database.commit()
    database.close()
    return True


#returns True if student successfully removed from roster, False otherwise
def remove_from_roster(studentID, courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()
    if (course == None):
        print("Error in remove_from_roster(): courseCRN " + str(courseCRN) + " not found.")
        return False
    else:
        courseRoster = course[9]
        if (courseRoster == None):
            courseRoster = ""
        if (not check_if_student_in_roster(studentID, courseCRN)):
            print("Error in remove_from_roster(): Student ID#" + str(studentID) + " not in course #" + str(courseCRN))
            return False
        courseRosterArr = []
        currentStudent = ""
        for i in courseRoster:
            if (i == None):
                break
            elif (i == ","):
                courseRosterArr.append(currentStudent)
                currentStudent = ""
                continue
            currentStudent = currentStudent + i
        courseRosterArr.remove(str(studentID))
        newCourseRoster = ""
        for i in courseRosterArr:
            newCourseRoster = str(i) + ","
        cursor.execute("UPDATE COURSE SET ROSTER = '" + newCourseRoster + "' WHERE CRN = '" + courseCRN + "'")  
        database.commit()
        database.close()
        return True


def check_if_student_in_roster(studentID, courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()

    if (course == None):
            return False
    else:
        courseRosterStr = course[9]
        if (courseRosterStr == None):
            courseRosterStr = ""

    courseRoster = []
    currentStudent = ""
    for i in courseRosterStr:
        if (i == None):
            break
        elif (i == ","):
            courseRoster.append(currentStudent)
            currentStudent = ""
            continue
        currentStudent = currentStudent + i

    for i in courseRoster:
        if (str(i) == str(studentID)):
            return True
    
    return False
        
       
def print_roster(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()

    if (len(course) == 0):
            print("Course not found.")
            return
    else:
        courseRosterStr = course[9]
        if (courseRosterStr == None):
            courseRosterStr = ""

    courseRoster = []
    currentStudent = ""
    for i in courseRosterStr:
        if (i == None):
            break
        elif (i == ","):
            courseRoster.append(currentStudent)
            currentStudent = ""
            continue
        currentStudent = currentStudent + i

    if (len(courseRoster) == 0):
        print("No students in roster.")
        return
    print("Course roster for CRN #" + courseCRN + ":")
    for i in courseRoster:
        cursor.execute("SELECT * FROM STUDENT WHERE ID = '" + i + "'")
        student = cursor.fetchone()
        studentInfo = "ID: " + i + "; Name = " + student[1] + " " + student[2] + ";"
        print(studentInfo)