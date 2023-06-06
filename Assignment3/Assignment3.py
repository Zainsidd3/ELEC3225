import sqlite3

database = sqlite3.connect("Assignment3/assignment3.db")
cursor = database.cursor()

def print_tables():
    print("Printing all tables")
    databases = ["ADMIN", "INSTRUCTOR", "STUDENT", "COURSE"]
    for i in databases:
        try: 
            print("\nPrinting table " + i)
            cursor.execute("""SELECT * FROM """ + i)
            query_result = cursor.fetchall()
            for j in query_result:
                print(j)
        except:
            print("Error: Missing table " + i + ", continuing.")

exit = False
while (exit == False):
    print("0 - Create new table\n1 - Search by parameter\n2 - Insert new entry to table\n3 - Update existing table entry\n4 - Remove existing table entry\n5 - Print all tables\n6 - Exit")
    userInput = ""
    while (type(userInput) != int):
        try:
            userInput = int(input("Enter your selection: "))
        except: 
            print("Error: Input not an integer")
    if (userInput > 6) or (userInput < 0):
        print("Error: Input out of range (0-6), please try again")

    if userInput == 0:
        pass
    elif userInput == 1:
        pass
    elif userInput == 2:
        pass
    elif userInput == 3:
        pass
    elif userInput == 4:
        pass
    elif userInput == 5:
        print_tables()
    elif userInput == 6:
        userInput = input("Are you sure you'd like to exit? (Y/N): ")
        if (userInput == "Y") or (userInput == "y"):
            exit = True
            print("Exiting")
        else:
            exit = False
