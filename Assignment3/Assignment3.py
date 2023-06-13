import sqlite3

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
        create_table()
    elif userInput == 1:
        pass
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