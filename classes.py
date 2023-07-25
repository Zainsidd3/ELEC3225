from databaseFunctions import *

class user:
    #Set all values to empty/0 when first created
    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.ID = 0
    
    def set_first_name(self, newFirstName):
        #set the user's first name
        self.firstName = newFirstName

    def set_last_name(self, newLastName):
        #set the user's last name
        self.lastName = newLastName

    def set_id(self, newID):
        #set the user's ID
        self.ID = newID
    
    def get_ID(self):
        return self.ID

    def print_info(self):
        #print the user's info
        print("Name =", self.firstName, self.lastName, "; ID =", self.ID)

    def print_all_courses(self):
        #print course table
        print_table("COURSE")

    def search_for_course(self):
        print("Searching for course")
        courseAtt = ["CRN", "TITLE", "DEPT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS"]
        counter = 0

        for i in courseAtt:
            print(str(counter) + " - " + str(i))
            counter = counter + 1

        attribute = ""
        while (type(attribute) != int):
            try:
                attribute = int(input("Enter your selection: "))
            except: 
                print("Error: Input not an integer")
            if (attribute > 7) or (attribute < 0):
                print("Error: Input out of range (0-7), please try again")
                attribute = ""

        queryVal = input("Enter Value: ")
        result = search("COURSE", courseAtt[attribute], queryVal)
        if (len(result) == 0):
            print("No results found.")
        for i in result:
            print(i)

class student(user):
    def modify_schedule(self):
        print("1 - Add yourself to a course roster\n2 - Remove yourself from a course roster\n3 - Go back to main menu")
        userInput = 0
        while (userInput > 3 or userInput < 1):
            try:
                userInput = int(input("Enter your selection (1-3): "))
            except:
                print("Error, input unrecognized. Please try again.")
        if (userInput == 1):
            # add to a course
            print("Add yourself to a course roster")
            CRN = input("Enter the CRN of the course you'd like to add: ")
            if (check_if_student_in_roster(self.ID, CRN)):
                print("You're already in this course.")
                return
            else:
                if (add_to_roster(self.ID, CRN)):
                    print("You have successfully been added to course #" + CRN + ".")
                return
        
        elif (userInput == 2):
            # remove from a course
            print("Remove yourself from a course roster")
            CRN = input("Enter the CRN of the course you'd like to remove yourself from: ")
            if (not check_if_student_in_roster(self.ID, CRN)):
                print("You are not in this course.")
                return
            if (remove_from_roster(self.ID, CRN)):
                print("You have been successfully removed from course #" + CRN + ".")
            return

    def print_schedule(self):
        #print the student's schedule
        semester = ""
        while (semester != "Su" and semester != "Sp" and semester != "F"):
            semester = str(input("Enter semester (Su = Summer, Sp = Spring, F = Fall, case sensitive):"))
            if (semester != "Su" and semester != "Sp" and semester != "F"):
                print("Invalid input, please try again.")
        year = 0
        while (year <= 0):
            try:
                year = int(input("Enter year: "))
            except:
                print("Input not an int, please try again.")
                continue
            if (year <= 0):
                print("Invalid input, please try again.")
        schedule = get_student_course_list(self.ID, semester, year)
        if (len(schedule) == 0):
            print("Not registered for any classes in the " + str(year) + " " + semester + " semester.")
            return
        mondayCourses = []
        tuesdayCourses = []
        wednesdayCourses = []
        thursdayCourses = []
        fridayCourses = []
        dayCourses = [mondayCourses, tuesdayCourses, wednesdayCourses, thursdayCourses, fridayCourses]
        days = ["M", "T", "W", "R", "F"]
        for i in schedule:
            for j in range(len(days)):
                if days[j] in i[2]:
                    dayCourses[j].append(i[0] + "; Time: " + i[1])

        for i in range(len(days)):
            if (len(dayCourses[i]) == 0):
                print("No courses on " + days[i] + ".")
                continue
            print(days[i] + " Schedule:") 
            for j in dayCourses[i]:
                print(j)
        return

    def check_for_conflicts(self):
        #check the student's schedule for conflicts
        print("Called student.check_for_conflicts()")


class instructor(user):
    def print_class_list(self):
        print("1 - Print the course roster of a specific course\n2 - Go back to the main menu")


        userInput = 0
        while userInput > 2 or userInput < 1:
            try:
                userInput = int(input("Enter your selection (1-2): "))
            except ValueError:
                print("Error, input unrecognized. Please try again.")

        if userInput == 1:
            # Print the course roster of a specific course
            print("Print the course roster of a specific course")
            CRN = input("Enter the CRN of the course: ")
            students = print_roster(CRN)
            if students:
                print("Course roster for CRN #" + CRN + ":")
                for student in students:
                    print(student)
            return []
    
    def print_schedule():
        #print the instructor's teaching schedule
        print("Called instructor.print_schedule()")

class admin(user):
    def modify_course(self):
        print("1 - Add a course\n2 - Remove a course\n3 - Go back to main menu")
        userInput = 0
        while (userInput > 3 or userInput < 1):
            try:
                userInput = int(input("Enter your selection (1-3): "))
            except:
                print("Error, input unrecognized. Please try again.")
        if (userInput == 1):
            # add a course
            print("Add a course")
            CRN = input("Enter the CRN for the new course: ")
            if (check_if_course_exists(CRN)):
                print("This course already exists.")
                return
            else:
                attributes = ["TITLE", "DEPT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS", "INSTRUCTOR", "ROSTER"]
                data = "('" + CRN + "', "
                counter = 0
                for i in attributes:
                    if (i == "TIME"):
                        startTime = -1
                        while (int(startTime) < 0 or int(startTime) > 2400):
                            startTime = str(input("Enter start time for the course (24 hour format, e.g. 1:30pm = 1330): "))
                            if (int(startTime) < 0 or int(startTime) > 2400):
                                print("Entered invalid start time, please try again.")
                        endTime = -1
                        while (int(endTime) < 0 or int(endTime) > 2400 or int(endTime) < int(startTime)):
                            endTime = str(input("Enter end time for the course (24 hour format, e.g. 1:30pm = 1330): "))
                            if (int(startTime) < 0 or int(startTime) > 2400):
                                print("Entered invalid end time, please try again.")
                            if (int(endTime) < int(startTime)):
                                print("End time must be after the start time, please try again.")
                        newData = startTime + "-" + endTime
                    elif (i == "DAYS"):
                        days = []
                        while (days == []):
                            daysStr = input("Enter the days of the course in MTWRF format (e.g. 'MRF' = Monday+Thursday+Friday, case sensitive):")
                            for i in daysStr:
                                if (i == "M" or i == "T" or i == "W" or i == "R" or i == "F"):
                                    if i in days:
                                        print("Duplicate day detected, please try again.")
                                        days = []
                                        break
                                    else: 
                                        days.append(i)
                                else:
                                    print("Unknown day detected (" + i + "), please try again.")
                                    days = []
                                    break
                        #put list in order
                        correctOrder = ["M", "T", "W", "R", "F"]
                        newData = ""
                        for i in correctOrder:
                            if i in days:
                                newData = newData + i
                    elif (i == "SEMESTER"):
                        semester = ""
                        while (semester != "Su" and semester != "Sp" and semester != "F"):
                            semester = str(input("Enter semester (Su = Summer, Sp = Spring, F = Fall, case sensitive):"))
                            if (semester != "Su" and semester != "Sp" and semester != "F"):
                                print("Invalid input, please try again.")
                        newData = semester
                    elif (i != "INSTRUCTOR" and i != "ROSTER"):
                        newData = str(input("Enter " + i + ": "))
                    else:
                        newData = ""

                    data = data + "'" + newData + "'"
                    if counter != len(attributes) - 1:
                            data = data + ", "
                    counter = counter + 1
                data = data + ")"
                
                print(data)
                if (insert_course_data(CRN, data)):
                    print("You have successfully added course #" + CRN + ".")
                return
        elif (userInput == 2):
            # remove a course
            print("Remove a course")
            CRN = input("Enter the CRN of the course you'd like to remove: ")
            if (not check_if_course_exists(CRN)):
                print("This course does not exist.")
                return
            if (delete_data(CRN)):
                print("You have sucessfully removed course #" + CRN + ".")
            return

    def add_account(self):
        #add a user to the system
        email = input("Enter the email address: ")

        if (not check_email_exists(email)):
            print("Account type: ")
            print("1 - Student")
            print("2 - Instructor")
            account_type = input("Enter the account type: ")

            if account_type == "1":
                student_info = (
                    input("Enter ID: "),
                    input("Enter NAME: "),
                    input("Enter SURNAME: "),
                    input("Enter GRADYEAR: "),
                    input("Enter MAJOR: "),
                    email
                )
                password = input("Please enter the password for the new account: ")
                add_student(email, student_info, password)
                print("Student account added successfully.")
            elif account_type == "2":
                instructor_info = (
                    input("Enter ID: "),
                    input("Enter NAME: "),
                    input("Enter SURNAME: "),
                    input("Enter TITLE: "),
                    input("Enter HIREYEAR: "),
                    input("Enter DEPT: "),
                    email
                )
                password = input("Please enter the password for the new account: ")
                add_instructor(email, instructor_info, password)
                print("Instructor account added successfully.")
            else:
                print("Invalid account type. Please try again.")
        else:
            print("Email address already exists in the database.")

    def remove_account(self):
        email = input("Enter the email address of the account you would like to remove: ")
        remove_account(email)


    def add_student_to_course(self):
        #add a student to a course
        print("Called admin.add_student_to_course()")

    def remove_student_from_course(self):
        #remove a student from a course
        print("Called admin.remove_student_from_course()")

    def add_instructor_to_course(self):
        #add an instructor to a course
        print("Called admin.add_instructor_to_course()")

    def remove_instructor_from_course(self):
        #remove an instructor from a course
        print("Called admin.remove_instructor_from_course()")