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
        search("COURSE")

class student(user):
    def modify_schedule(self):
        add_or_remove_from_roster(self.ID)

    #def print_schedule(self):
    #    #print the student's schedule
    #    print("Called student.print_schedule()")

class instructor(user):
    #def print_schedule(self):
    #    #print the instructor's schedule
    #    print("Called instructor.print_schedule()")

    def print_class_list(self):
        #print the instructor's class list
        courseCRN = str(input("Enter course CRN to print the roster of: "))
        print_roster(courseCRN)

class admin(user):
    pass
    #def add_course(self, course_id, course_name):
    #    #add a course using the course's id and name
    #    print("Called admin.add_course() with course_id", str(course_id), "and course_name", course_name)

    def remove_course(self):
        #remove a course using the course's id
        delete_data("COURSE")

    #def add_user(self, new_user_id):
    #    #add a user to the system
    #    print("Called admin.add_user() with new_user_id", str(new_user_id))

    #def remove_user(self, user_id):
    #    #remove a user from the system
    #    print("Called admin.remove_user() with user_id", str(user_id))

    #def add_to_course(self, student_id, course_id):
    #    #add a user to a course using the student's id and the course's id
    #    print("Called admin.add_to_course() with student id", str(student_id), "and course_id", str(course_id))

    #def remove_from_course(self, student_id, course_id):
    #    #remove a user from a course using the student's id and the course's id
    #    print("Called admin.remove_from_course() with student id", str(student_id), "and course_id", str(course_id))

    #def search_for_course(self, course_name):
    #    #search for a course using the course's name
    #    print("Called admin.search_for_course() with course_name", course_name)