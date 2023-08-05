import sqlite3

# ---------------------------- GLOBAL USER FUNCTIONS ---------------------------- #

# checks login credentials against db
# email (string)
# password (string)
def check_login_credentials(email, password):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    # Check if the email and password match in the LOGINS table
    cursor.execute("SELECT COUNT(*) FROM LOGINS WHERE ID=? AND PASSWORD=?", (email, password))
    login_count = cursor.fetchone()[0]

    database.close()
    if login_count > 0:
        return True
    else:
        return False

# returns list of all rows in a table
# table (string) - name of the table to return ("COURSE", "INSTRUCTOR", "ADMIN", "STUDENT")
def get_table(table):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    result = []
    if (table == "COURSE"):
        cursor.execute("SELECT * FROM COURSE")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        column_names = column_names[:-1]
        result.append(column_names)
        for row in rows:
            row_values = row[:-1]
            result.append(row_values)
    else:
        cursor.execute("SELECT * FROM " + table)
        query_result = cursor.fetchall()
        for j in query_result:
            result.append(row_values)
    database.close()

    return result

# searches tables for specific attributes
# table (string) - the table to search ("INSTRUCTOR", "ADMIN", "STUDENT", or "COURSE")
# attribute (string) - name of the attribute to search (e.g. "CRN")
# query (string) - entry being searched for (e.g. "001")
def search(table, attribute, query):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    
    try:
        cursor.execute("""SELECT * FROM """ + table + """ WHERE """ + attribute + """ = '""" + query + """'""")
    except:
        raise TypeError("Error in search()")

    query_result = cursor.fetchall()

    database.close()

    return query_result


# ------------------------------------------------------------------------- #

# ---------------------------- ADMIN FUNCTIONS ---------------------------- #

# returns True if course already exists in system, False otherwise
# courseCRN (string) - course CRN to check
def check_if_course_exists(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()

    database.close()

    if (course == None):
        return False
    else:
        return True

# adds a new course to the system
# data (list) - formatted as [CRN, DEPT, TIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR, ROSTER] all strings
def insert_course_data(courseCRN, data):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    if (check_if_course_exists(courseCRN)):
        print("Error in add_to_roster(): Course CRN#" + str(courseCRN) + " already exists")
        database.close()
        return False
    try:
        cursor.execute(f"INSERT INTO COURSE VALUES {data}")
        database.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error: Failed to insert data.")
        print(e)
    database.commit()
    database.close()
    return True

# deletes a course from the system, returns True if successful, False otherwise
# courseCRN (string) - the courseCRN to remove
def delete_data(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()
    if (course == None):
        print("Error in delete_data(): courseCRN " + str(courseCRN) + " not found.")
        database.close()
        return False
    else:
        cursor.execute("DELETE FROM COURSE WHERE CRN = '" + courseCRN + "'")
        database.commit()
        database.close()
        return True

# checks if an account with the given email already exists
# email (string) - email to check system for
def check_email_exists(email):
        # Check if the email exists in STUDENT, INSTRUCTOR, or LOGINS tables
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(*) FROM STUDENT WHERE EMAIL=?", (email,))
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM INSTRUCTOR WHERE EMAIL=?", (email,))
        instructor_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM LOGINS WHERE ID=?", (email,))
        login_count = cursor.fetchone()[0]

        database.close()

        return student_count + instructor_count + login_count > 0

# adds an instructor account to the system
# email (string) - email for the new instructor
# instructor_info (list) - formatted as [ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL], all strings
# password (string) - password for the new instructor
def add_instructor(email, instructor_info, password):
        # Insert the instructor info into the INSTRUCTORS table
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)", instructor_info)
        database.commit()

        cursor.execute("INSERT INTO LOGINS (ID, PASSWORD) VALUES (?,?)", (email, password))
        database.commit()
        database.close()
        return True

# adds a student account to the system
# email (string) - email for the new student
# student_info (list) - formatted as [ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL], all strings
# password (string) - password for the new student
def add_student(email, student_info, password):
        # Insert the student info into the STUDENTS table
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)", student_info)
        database.commit()

        cursor.execute("INSERT INTO LOGINS (ID, PASSWORD) VALUES (?,?)", (email, password))
        database.commit()
        database.close()
        return True

# removes an account from the system
# email (string) - email of the account to remove from the system
def remove_account(email):
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(*) FROM STUDENT WHERE EMAIL=?", (email,))
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM INSTRUCTOR WHERE EMAIL=?", (email,))
        instructor_count = cursor.fetchone()[0]

        # Checks for STUDENT account
        if student_count > 0:
            cursor.execute("SELECT ID FROM STUDENT WHERE EMAIL=?", (email,))
            student_id = cursor.fetchone()[0]

            cursor.execute("DELETE FROM STUDENT WHERE EMAIL=?", (email,))
            database.commit()
            cursor.execute("DELETE FROM LOGINS WHERE ID=?", (email,))
            database.commit()
            print("Student account removed successfully.")
            database.close()
            return True

        # Checks for INSTRUCTOR account
        elif instructor_count > 0:
            cursor.execute("SELECT NAME FROM INSTRUCTOR WHERE EMAIL=?", (email,))
            instructor_name = cursor.fetchone()[0]

            cursor.execute("DELETE FROM INSTRUCTOR WHERE EMAIL=?", (email,))
            database.commit()
            cursor.execute("DELETE FROM LOGINS WHERE ID=?", (email,))
            database.commit()
            print("Instructor account removed successfully.")
            database.close()
            return True

        # No account found
        else:
            print("Email address not found...")
            database.close()
            return False

def link_student_to_course(student_email, courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    # Check if the student exists
    if not check_email_exists(student_email):
        print("Student with email", student_email, "does not exist.")
        database.close()
        return False

    # Check if the course exists
    if not check_if_course_exists(courseCRN):
        print("Course with CRN", courseCRN, "does not exist.")
        database.close()
        return False

    # Link student to course
    if add_to_roster(student_email, courseCRN):
        print("Student", student_email, "linked to course", courseCRN, "successfully.")
    else:
        print("Failed to link student to the course.")
    
    database.close()
    return True

def link_instructor_to_course(instructor_email, courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    # Check if the instructor exists
    if not check_email_exists(instructor_email):
        print("Instructor with email", instructor_email, "does not exist.")
        database.close()
        return False

    # Check if the course exists
    if not check_if_course_exists(courseCRN):
        print("Course with CRN", courseCRN, "does not exist.")
        database.close()
        return False

    cursor.execute("UPDATE COURSE SET INSTRUCTOR = ? WHERE CRN = ?", (instructor_email, courseCRN))
    database.commit()
    database.close()
    return True

# ------------------------------------------------------------------------- #

# ---------------------------- INSTRUCTOR FUNCTIONS ---------------------------- #

# returns a list with the info of all of the students in the given course 
# courseCRN (string) - CRN of the roster to print
def print_roster(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = ?", (courseCRN,))
    course = cursor.fetchone()

    if course is None:
        print("Course not found.")
        return []
    else:
        courseRosterStr = course[9]
        if courseRosterStr is None:
            courseRosterStr = ""

    courseRoster = []
    currentStudent = ""
    for i in courseRosterStr:
        if i == ",":
            courseRoster.append(currentStudent)
            currentStudent = ""
        else:
            currentStudent += i

    if len(courseRoster) == 0:
        database.close()
        return []

    students = []
    for studentID in courseRoster:
        cursor.execute("SELECT * FROM STUDENT WHERE ID = ?", (studentID,))
        student = cursor.fetchone()
        studentInfo = "ID: " + studentID + "; Name = " + student[1] + " " + student[2] + ";"
        students.append(studentInfo)
    
    database.close()
    return students

# returns a list of all classes the instructor is teaching [[CRN, [DAYS], [StartTime, EndTime]], ...]
# instructorID (string) - the email of the instructor to check
# semester (string) - expecting Sp, Su, or F (Spring, Summer, Fall)
# year (int) - the year of the schedule to check
def get_instructor_course_list(instructorEmail, semester, year):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT TITLE, TIME, DAYS FROM COURSE WHERE INSTRUCTOR = '" + instructorEmail + "' AND SEMESTER = '" + semester + "' AND YEAR = '" + str(year) + "'")
    courses = cursor.fetchall()

    database.close()
    return courses

# ------------------------------------------------------------------------- #

# ---------------------------- STUDENT FUNCTIONS ---------------------------- #

# returns True if student successfully added to the roster, False if the course does not exist or if student already in the roster
# studentID (string) - the ID of the student to check
# courseCRN (string) - the CRN of the course roster to remove student from
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

# returns True if student successfully removed from the roster, False if the course does not exist or if student not in the roster
# studentID (string) - the ID of the student to check
# courseCRN (string) - the CRN of the course roster to remove student from
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

# returns True if student is found in the given course roster, False if the course does not exist or if the student is not in the roster
# studentID (string) - the ID of the student to check
# courseCRN (string) - the CRN of the course roster to check
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


    database.close() 

    for i in courseRoster:
        if (str(i) == str(studentID)):
            return True
    
    return False

# returns a list of all of the courses the given student is enrolled in, in the given semester + year
# studentID (string) - the ID of the student to check
# semester (string) - expecting Sp, Su, or F (Spring, Summer, Fall) 
# year (int) - the year of the schedule to check
def get_student_course_list(studentID, semester, year):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT CRN, SEMESTER, YEAR FROM COURSE")
    allCourses = cursor.fetchall()

    studentCourses = []
    for i in allCourses:
        if (check_if_student_in_roster(studentID, i[0]) and semester == i[1] and year == i[2]):
            cursor.execute("SELECT TITLE, TIME, DAYS FROM COURSE WHERE CRN = '" + i[0] + "'")
            courseInfo = cursor.fetchone()
            studentCourses.append(courseInfo)


    return studentCourses

# returns a list of all of the courses the given student is enrolled in, in the given semester + year + day
# studentID (string) - the ID of the student to check
# semester (string) - expecting Sp, Su, or F (Spring, Summer, Fall)
# year (string) - the year of the schedule to check
# day (string) - the day of classes to check ("M", "T", "W", "R", or "F")
def get_day_course_crns(studentID, semester, year, day):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT CRN FROM COURSE WHERE SEMESTER = '" + semester + "' AND YEAR = '" + year + "'")
    allCourses = cursor.fetchall()

    courses = []
    for i in allCourses:
        if (not check_if_student_in_roster(studentID, i[0])):
            continue
        if day in get_course_days(i[0]):
            courses.append(i[0])

    return courses

#returns True if conflicts detected on adding a new course, False otherwise
# studentID (string) - the student's ID
# newCRN (string) - the new course CRN that's being added to the student's schedule
def check_for_new_conflicts(studentID, newCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT SEMESTER, YEAR, TIME, DAYS FROM COURSE WHERE CRN = '" + newCRN + "'")
    newCourse = cursor.fetchone()
    newCourseSemester = newCourse[0]
    newCourseYear = newCourse[1]
    newCourseTime = get_course_times(newCRN)
    newCourseStartTime = int(newCourseTime[0])
    newCourseEndTime = int(newCourseTime[1])
    newCourseDays = get_course_days(newCRN)
    
    for day in newCourseDays:
        courses = get_day_course_crns(studentID, newCourseSemester, newCourseYear, day)
        for course in courses:
            times = get_course_times(course)
            # if new start time or new end time are between start and end time of an existing course
            if ((newCourseStartTime >= times[0] and newCourseStartTime <= times[1]) or (newCourseEndTime >= times[0] and newCourseEndTime <= times[1])):
                print("Error: New course overlaps with course #" + course)
                return False
            
   
    return True

# returns True if conflicts found in the given schedule, False otherwise
# studentID (string) - the student's ID
# semester (string) - expecting Sp, Su, or F (Spring, Summer, Fall)
# year (string) - the year of the schedule to check
def check_schedule_for_conflicts(studentID, semester, year):
    days = ["M", "T", "W", "R", "F"]
    courseTimes = []
    for day in days:
        dayCourses = get_day_course_crns(studentID, semester, year, day)
        dayTimes = []
        for course in dayCourses:
            dayTimes.append(get_course_times(course))
        courseTimes.append(dayTimes)
    
    for daySchedule in courseTimes:
        for i in range(len(daySchedule)):
            #compare to all start/end times in current day
            for j in range(len(daySchedule)):
                #skip if comparing to current course
                if (i == j):
                    continue
                if (daySchedule[i][0] >= daySchedule[j][0] and daySchedule[i][0] <= daySchedule[j][1] or daySchedule[i][1] >= daySchedule[j][0] and daySchedule[i][1] <= daySchedule[j][1]):
                    return True

    return False

# returns an array of ints [startTime, endTime]
# CRN (string) - the course's CRN
def get_course_times(CRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT TIME FROM COURSE WHERE CRN = '" + CRN + "'")
    time = cursor.fetchone()[0]
    startTime = ""
    startTimeDone = False
    endTime = ""
    for i in time:
        if (i == "-"):
            startTimeDone = True
            continue
        else:
            if (not startTimeDone):
                startTime = startTime + i
            else:
                endTime = endTime + i

    return [int(startTime), int(endTime)]

#returns of an array of the days for a course (e.g. ['M', 'W', 'R'])
# CRN (string) - the course's CRN
def get_course_days(CRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT DAYS FROM COURSE WHERE CRN = '" + CRN + "'")
    days = cursor.fetchone()[0]

    daysArr = []

    for i in days:
        daysArr.append(i)

    return daysArr
# ------------------------------------------------------------------------- #