import tkinter as tk
from tkinter import messagebox

from classes import *
from databaseFunctions import *

database = sqlite3.connect("database.db")
cursor = database.cursor()

import hashlib

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x200")

        self.username_label = tk.Label(root, text="Email Address:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.check_login)
        self.login_button.pack()

        self.credentials_window = None

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        database = sqlite3.connect("database.db")
        cursor = database.cursor()

        if check_login_credentials(username, password):
            cursor.execute("SELECT * FROM LOGINS WHERE ID = ? and PASSWORD = ? ", (username, password))
            tables = ["STUDENT", "ADMIN", "INSTRUCTOR"]
            for i in tables:
                query = "SELECT * FROM " + i + " WHERE EMAIL = '" + username + "'"
                cursor.execute(query)
                userInfo = cursor.fetchall()
                if (len(userInfo) > 0):
                    userType = i
                    break

            #store all user info in object corresponding to user type
            loggedInUser = user()
            if (userType == "STUDENT"):
                loggedInUser = student()
            elif (userType == "ADMIN"):
                loggedInUser = admin()
            elif (userType == "INSTRUCTOR"):
                loggedInUser = instructor()

            loggedInUser.set_id(userInfo[0][0])
            loggedInUser.set_first_name(userInfo[0][1])
            loggedInUser.set_last_name(userInfo[0][2])

            self.show_credentials(username, password, userType)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_credentials(self, username, password, userType):
        self.root.withdraw()  # Hide the login window

        # Student Selections
        if (userType == "STUDENT"):
            new_window = tk.Tk()
            new_window.title("LOGIN | STUDENT-LEVEL")
            new_window.geometry("500x200")

            credentials_label1 = tk.Button(new_window, text="Display all courses", command=self.logout)
            credentials_label1.pack()

            credentials_label2 = tk.Button(new_window, text="Search Courses by Parameter", command=self.logout)
            credentials_label2.pack()

            credentials_label3 = tk.Button(new_window, text="Add/ Remove Course from Semester Schedule", command=self.logout)
            credentials_label3.pack()

            credentials_label4 = tk.Button(new_window, text="Check Semester Schedule for Conflicts", command=self.logout)
            credentials_label4.pack()

        # Admin Selections
        elif (userType == "ADMIN"):
            new_window = tk.Tk()
            new_window.title("LOGIN | ADMINISTRATOR-LEVEL")
            new_window.geometry("500x200")

            credentials_label1 = tk.Button(new_window, text="Display all courses", command=self.logout)
            credentials_label1.pack()

            credentials_label2 = tk.Button(new_window, text="Search Courses by Parameter", command=self.logout)
            credentials_label2.pack()

            credentials_label3 = tk.Button(new_window, text="Add/ Remove Course from System", command=self.logout)
            credentials_label3.pack()

            credentials_label4 = tk.Button(new_window, text="Add/ Remove User(s)", command=self.logout)
            credentials_label4.pack()
         
        # Instructor Selections
        elif (userType == "INSTRUCTOR"):
            new_window = tk.Tk()
            new_window.title("LOGIN | INSTRUCTOR-LEVEL")
            new_window.geometry("500x200")

            credentials_label1 = tk.Button(new_window, text="Display all courses", command=self.logout)
            credentials_label1.pack()

            credentials_label2 = tk.Button(new_window, text="Search Courses by Parameter", command=self.logout)
            credentials_label2.pack()

            credentials_label3 = tk.Button(new_window, text="Assemble/ Print Course Roster", command=self.logout)
            credentials_label3.pack()

        # Global User Selections
        logout_button = tk.Button(new_window, text="Log Out", command=self.logout)
        logout_button.pack()

        new_window.protocol("WM_DELETE_WINDOW", self.logout_and_show_login)  # Handle window close event

    def logout(self):
        self.root.deiconify()  # Show the login window
        #self.root.destroy()

    def logout_and_show_login(self):
        self.root.deiconify()  # Show the login window
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)  # Re-enable window close event
        self.root.update()  # Update the window to avoid any potential issues
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()