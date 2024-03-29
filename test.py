import unittest

from databaseFunctions import *
from classes import *

class Tests(unittest.TestCase):
    def test_successful_login(self):              # Test successful login with correct credentials
        self.assertTrue(check_login_credentials("hamiltonm", "admin1"))

    def test_failed_login(self):                  # Test failed login with incorrect password
        self.assertFalse(check_login_credentials("hamiltonm", "wrongpassword"))

    def test_logout(self):                        # Test successful logout
        #set up a mock logged in user
        loggedInUser = user()
        loggedInUser.set_id(999)
        loggedInUser.set_first_name("TEST")
        loggedInUser.set_last_name("USER")
        
        #logout the user
        loggedInUser = user()
        self.assertTrue(loggedInUser.get_ID() == 0)

    def test_successful_add(self):                # Test successful addition of a student to a course roster
        self.assertTrue(add_to_roster(999, "001"))

    def test_add_to_invalid_CRN(self):            # Test addition to an invalid CRN
        self.assertFalse(add_to_roster(999, "NOTACRN"))

    def test_successful_removal(self):            # Test successful removal of a student from a course roster
        self.assertTrue(remove_from_roster(999, "001"))

    def test_remove_from_invalid_CRN(self):       # Test removal from an invalid CRN
        self.assertFalse(remove_from_roster(999, "NOTACRN"))

    def test_remove_student_not_in_roster(self): # Test removal of a student not in the course roster
        self.assertFalse(remove_from_roster(999, "002"))

    def test_successful_course_search(self):     # Test successful search for a course

        self.assertTrue(len(search("COURSE", "CRN", "001")) == 1)

    def test_failed_course_search(self):         # Test failed search for a non-existent course
        self.assertTrue(len(search("COURSE", "CRN", "999")) == 0)

    def test_invalid_table_search(self):         # Test search on an invalid table name
        with self.assertRaises(TypeError):
            search("NOTATABLE", "CRN", "001")

    def test_invalid_attribute_search(self):    # Test search with an invalid attribute
        with self.assertRaises(TypeError):
            search("COURSE", "AAAAA", "001")
    
    def test_successful_add_course(self):
        self.assertTrue(insert_course_data("123", ("123", "Social Sciences", "PSYC", "1000", "WF", "Fall", "2023", "3", "Nobody", "0")))

    def test_invalid_add_course(self):
        self.assertFalse(insert_course_data("001", ("001", "Intro to Engineering", "BSCO", "1200", "MWF", "Spring", "2024", "3", "Nelson", "0")))

    def test_successful_delete_course(self):
        self.assertTrue(delete_data("123"))

    def test_invalid_delete_course(self):
        self.assertFalse(delete_data("NOTACRN"))

    def test_print_roster(self):
        courseCRN = "001"  # Replace with the desired course CRN to test
        students = print_roster(courseCRN)
        self.assertIsNotNone(students)  # Check if the roster is not None
        self.assertIsInstance(students, list)  # Check if the roster is a list

    def test_print_roster_contains_student(self):
        courseCRN = "001"  # Replace with the desired course CRN to test
        expectedStudentID = "10012"  # Replace with the expected student ID in the roster

        students = print_roster(courseCRN)
        self.assertIsNotNone(students)  # Check if the roster is not None
        self.assertIsInstance(students, list)  # Check if the roster is a list

        studentFound = False
        for student in students:
            if expectedStudentID in student:
                studentFound = True
                break

        self.assertTrue(studentFound)  # Check if the expected student ID is found in the roster

    def test_get_table(self):
        tableName = "COURSE"
        expectedCRN = "001"

        courses = get_table(tableName)
        courseFound = False
        for course in courses:
            if expectedCRN in course:
                courseFound = True
                break
        
        self.assertTrue(courseFound)

    def test_invalid_table(self):
        tableName = "NOTATABLE"

        with self.assertRaises(sqlite3.OperationalError):
            get_table(tableName)

    def test_conflicts(self):
        ID = "10001"
        semester = "Sp"
        year = "2023"

        self.assertTrue(check_schedule_for_conflicts(ID, semester, year))

    def test_no_conflicts(self):
        ID = "10001"
        semester = "Su"
        year = "2023"

        self.assertFalse(check_schedule_for_conflicts(ID, semester, year))

    def test_get_student_course_list(self):
        ID = "10001"
        semester = "Sp"
        year = 2023

        courseList = get_student_course_list(ID, semester, year)
        self.assertTrue(len(courseList) > 0)

    def test_0_student_course_list(self):
        ID = "10001"
        semester = "Sp"
        year = 2025

        courseList = get_student_course_list(ID, semester, year)
        self.assertTrue(len(courseList) == 0)

    def test_add_student(self):
        self.assertTrue(add_student("kristofj", ("10021", "Justin", "Kristof", "2024", "BSCO", "kristofj"), "12345"))

    def test_remove_student(self):
        self.assertTrue(remove_account("kristofj"))

    def test_add_instructor(self):
        self.assertTrue(add_instructor("testi", ("20017", "Test", "Instructor", "Full Prof.", "2020", "HUSS", "testi"), "54321"))

    def test_remove_instructor(self):
        self.assertTrue(remove_account("testi"))

    def test_instructor_class_list(self):
        instructorEmail = "georgef"
        semester = "Sp"
        year = 2023
        courses = get_instructor_course_list(instructorEmail, semester, year)
        self.assertTrue(len(courses) > 0)

    def test_link_student_to_course(self):
        email = "mcfetridgee"
        CRN = "016"

        self.assertTrue(link_student_to_course(email, CRN))

    def test_unlink_student_from_course(self):
        ID = "10012"
        CRN = "016"

        self.assertTrue(remove_from_roster(ID, CRN))

    def test_link_instructor_to_course(self):
        email = "patrickn"
        CRN = "016"

        self.assertTrue(link_instructor_to_course(email, CRN))
        database = sqlite3.connect("database.db")
        
        #unlink
        cursor = database.cursor()
        cursor.execute("UPDATE COURSE SET INSTRUCTOR = NULL WHERE CRN = ?", (CRN,))
        database.commit()
        database.close()

if __name__ == '__main__':
    unittest.main()
