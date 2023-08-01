import sqlite3

# ---------------------------- ADMIN FUNCTIONS ---------------------------- #

def check_if_course_exists(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()

    if (course == None):
        return False
    else:
        return True

def insert_course_data(courseCRN, data):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    if (check_if_course_exists(courseCRN)):
        print("Error in add_to_roster(): Course CRN#" + str(courseCRN) + " already exists")
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

def delete_data(courseCRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM COURSE WHERE CRN = '" + courseCRN + "'")
    course = cursor.fetchone()
    if (course == None):
        print("Error in delete_data(): courseCRN " + str(courseCRN) + " not found.")
        return False
    else:
        cursor.execute("DELETE FROM COURSE WHERE CRN = '" + courseCRN + "'")
        database.commit()
        database.close()
        return True

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

def add_instructor(email, instructor_info, password):
        # Insert the instructor info into the INSTRUCTORS table
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("INSERT INTO INSTRUCTOR (ID, NAME, SURNAME, TITLE, HIREYEAR, DEPT, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)", instructor_info)
        database.commit()

        cursor.execute("INSERT INTO LOGINS (ID, PASSWORD) VALUES (?,?)", (email, password))
        database.commit()
        database.close()

def add_student(email, student_info, password):
        # Insert the student info into the STUDENTS table
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        cursor.execute("INSERT INTO STUDENT (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?, ?, ?, ?, ?, ?)", student_info)
        database.commit()

        cursor.execute("INSERT INTO LOGINS (ID, PASSWORD) VALUES (?,?)", (email, password))
        database.commit()
        database.close()

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

        # Checks for INSTRUCTOR account
        elif instructor_count > 0:
            cursor.execute("SELECT NAME FROM INSTRUCTOR WHERE EMAIL=?", (email,))
            instructor_name = cursor.fetchone()[0]

            cursor.execute("DELETE FROM INSTRUCTOR WHERE EMAIL=?", (email,))
            database.commit()
            cursor.execute("DELETE FROM LOGINS WHERE ID=?", (email,))
            database.commit()
            print("Instructor account removed successfully.")

        # No account found
        else:
            print("Email address not found...")
        database.close()

# ------------------------------------------------------------------------- #


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


# returns True if the given student is in the roster of course #courseCRN, False otherwise
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
       
# returns a list with the info of all of the students in the given course 
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
        print("No students in roster.")
        return []

    students = []
    for studentID in courseRoster:
        cursor.execute("SELECT * FROM STUDENT WHERE ID = ?", (studentID,))
        student = cursor.fetchone()
        studentInfo = "ID: " + studentID + "; Name = " + student[1] + " " + student[2] + ";"
        students.append(studentInfo)
    
    return students

# returns a list of all of the courses the given student is enrolled in, in the given semester + year
# studentID - the ID of the student to check
# semester - expecting Sp, Su, or F (Spring, Summer, Fall)
# year - the year of the schedule to check
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
# studentID - the ID of the student to check
# semester - expecting Sp, Su, or F (Spring, Summer, Fall)
# year - the year of the schedule to check
# day - the day of classes to check
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

        

#returns an array of ints [startTime, endTime]
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
def get_course_days(CRN):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT DAYS FROM COURSE WHERE CRN = '" + CRN + "'")
    days = cursor.fetchone()[0]

    daysArr = []

    for i in days:
        daysArr.append(i)

    return daysArr