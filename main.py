import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class DatabaseManager:
    def __init__(self, connection):
        self.connection = connection

    def create_tables(self):
        cursor = self.connection.cursor()

        # Create Students table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Students')
            BEGIN
                CREATE TABLE Students (
                    StudentID INT PRIMARY KEY,
                    Name NVARCHAR(255),
                    Password NVARCHAR(255)
                )
            END
        ''')

        # Create Faculty table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Faculty')
            BEGIN
                CREATE TABLE Faculty (
                    FacultyID INT PRIMARY KEY,
                    Name NVARCHAR(255),
                    Password NVARCHAR(255)
                )
            END
        ''')

        # Create Admin table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Admin')
            BEGIN
                CREATE TABLE Admin (
                    Username NVARCHAR(255) PRIMARY KEY,
                    Password NVARCHAR(255)
                )
            END
        ''')

        # Create Courses table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Courses')
            BEGIN
                CREATE TABLE Courses (
                    CourseID INT PRIMARY KEY,
                    Name NVARCHAR(255)
                )
            END
        ''')

        # Create Enrollment table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Enrollment')
            BEGIN
                CREATE TABLE Enrollment (
                   
    StudentID INTEGER,
    CourseID INTEGER,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                )
            END
        ''')

        # Create Marks table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Marks')
            BEGIN
                CREATE TABLE Marks (
                    StudentID INT,
                    CourseID INT,
                    Assignment FLOAT,
                    Quiz FLOAT,
                    MidTerm FLOAT,
                    Final FLOAT,
                    Project FLOAT,
                    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                )
            END
        ''')
        cursor.execute('''
                   IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='FacultyCourses')
                   BEGIN
                       CREATE TABLE FacultyCourses (
                           FacultyID INT,
                           FacultyName NVARCHAR(255),
                           CourseID INT,
                           CourseName NVARCHAR(255),
                           FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID),
                           FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                       )
                   END
               ''')

        self.connection.commit()
        print("Tables created successfully.")

        # Create Attendance table
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='Attendance')
            BEGIN
                CREATE TABLE Attendance (
                    StudentID INT,
                    CourseID INT,
                    Date DATE,
                    Status NVARCHAR(50),
                    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                )
            END
        ''')

        self.connection.commit()
        print("Tables created successfully.")
class AddStudentForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.master = master
        self.connection = connection
        self.title("Add Student")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="Add Student", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_student_id = tk.Label(self, text="Student ID:")
        self.lbl_student_id.pack()
        self.entry_student_id = ttk.Entry(self)
        self.entry_student_id.pack()

        self.lbl_name = tk.Label(self, text="Name:")
        self.lbl_name.pack()
        self.entry_name = ttk.Entry(self)
        self.entry_name.pack()

        self.lbl_password = tk.Label(self, text="Password:")
        self.lbl_password.pack()
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_add = ttk.Button(self, text="Add", command=self.add_student)
        self.btn_add.pack(pady=10)

    def add_student(self):
        student_id = self.entry_student_id.get()
        name = self.entry_name.get()
        password = self.entry_password.get()

        # Check if the student ID already exists
        if self.is_student_exists(student_id):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        # Insert the student details into the database
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Students (StudentID, Name, Password) VALUES (?, ?, ?)",
                       (student_id, name, password))
        self.connection.commit()
        messagebox.showinfo("Success", "Student added successfully.")

    def is_student_exists(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
        return cursor.fetchone() is not None
class AssignCourseToFacultyForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("Assign Course to Faculty")
        self.geometry("400x300")
        self.connection = connection

        self.lbl_title = tk.Label(self, text="Assign Course to Faculty", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_faculty_id = tk.Label(self, text="Faculty ID:")
        self.lbl_faculty_id.pack()

        self.entry_faculty_id = ttk.Entry(self)
        self.entry_faculty_id.pack()

        self.lbl_faculty_name = tk.Label(self, text="Faculty Name:")
        self.lbl_faculty_name.pack()

        self.entry_faculty_name = ttk.Entry(self)
        self.entry_faculty_name.pack()

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()

        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.lbl_course_name = tk.Label(self, text="Course Name:")
        self.lbl_course_name.pack()

        self.entry_course_name = ttk.Entry(self)
        self.entry_course_name.pack()

        self.btn_assign = ttk.Button(self, text="Assign", command=self.assign_course)
        self.btn_assign.pack(pady=10)

    def assign_course(self):
        faculty_id = self.entry_faculty_id.get()
        faculty_name = self.entry_faculty_name.get()
        course_id = self.entry_course_id.get()
        course_name = self.entry_course_name.get()

        if not faculty_id or not faculty_name or not course_id or not course_name:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO FacultyCourses (FacultyID, FacultyName, CourseID, CourseName) VALUES (?, ?, ?, ?)",
                           (faculty_id, faculty_name, course_id, course_name))
            self.connection.commit()
            messagebox.showinfo("Success", "Course assigned to faculty successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
class AddFacultyForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("Add Faculty")
        self.geometry("400x300")
        self.connection = connection

        self.lbl_title = tk.Label(self, text="Add Faculty", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_faculty_id = tk.Label(self, text="Faculty ID:")
        self.lbl_faculty_id.pack()

        self.entry_faculty_id = ttk.Entry(self)
        self.entry_faculty_id.pack()

        self.lbl_name = tk.Label(self, text="Name:")
        self.lbl_name.pack()

        self.entry_name = ttk.Entry(self)
        self.entry_name.pack()

        self.lbl_password = tk.Label(self, text="Password:")
        self.lbl_password.pack()

        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_add = ttk.Button(self, text="Add", command=self.add_faculty)
        self.btn_add.pack(pady=10)

    def add_faculty(self):
        faculty_id = self.entry_faculty_id.get()
        name = self.entry_name.get()
        password = self.entry_password.get()

        if not faculty_id or not name or not password:
            messagebox.showerror("Error", "Please enter Faculty ID, Name, and Password")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Faculty (FacultyID, Name, Password) VALUES (?, ?, ?)", (faculty_id, name, password))
            self.connection.commit()
            messagebox.showinfo("Success", "Faculty added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


class ViewCoursesForm(tk.Toplevel):
    def __init__(self, connection, student_id):
        super().__init__()
        self.title("View Courses")
        self.geometry("400x300")
        self.connection = connection
        self.student_id = student_id

        self.lbl_title = tk.Label(self, text="Courses Assigned to You", font=("Helvetica", 14))
        self.lbl_title.pack(pady=10)

        # Create a Treeview widget to display the courses
        self.tree = ttk.Treeview(self, columns=("Course ID", "Course Name"))
        self.tree.heading("#0", text="Course ID")
        self.tree.heading("#1", text="Course Name")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Retrieve and display the courses assigned to the student
        self.populate_courses()

    def populate_courses(self):
        # Clear previous entries from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Query the database to get the courses assigned to the student
        cursor = self.connection.cursor()
        query = "SELECT Courses.CourseID,Courses.Name FROM Courses INNER JOIN Enrollment ON Courses.CourseID = Enrollment.CourseID WHERE Enrollment.StudentID = ?"
        print("SQL Query:", query)  # Debug
        print("Student ID:", self.student_id)  # Debug
        try:
            cursor.execute(query, (self.student_id,))
            courses = cursor.fetchall()
            print("Retrieved courses:", courses)  # Debug
            # Insert the courses into the Treeview

            for course in courses:
                self.tree.insert("", "end", text=course[0], values=(course[1]))


        except Exception as e:
            print("Error fetching courses:", e)  # Debug.



class AddCourseForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("Add Course")
        self.geometry("400x300")
        self.connection = connection

        self.lbl_title = tk.Label(self, text="Add Course", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()

        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.lbl_name = tk.Label(self, text="Name:")
        self.lbl_name.pack()

        self.entry_name = ttk.Entry(self)
        self.entry_name.pack()

        self.btn_add = ttk.Button(self, text="Add", command=self.add_course)
        self.btn_add.pack(pady=10)

    def add_course(self):
        course_id = self.entry_course_id.get()
        name = self.entry_name.get()

        if not course_id or not name:
            messagebox.showerror("Error", "Please enter both Course ID and Name")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Courses (CourseID, Name) VALUES (?, ?)", (course_id, name))
            self.connection.commit()
            messagebox.showinfo("Success", "Course added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
class AssignCourseToStudentForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("Assign Course to Student")
        self.geometry("300x200")
        self.connection = connection

        self.lbl_title = tk.Label(self, text="Assign Course to Student", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_student_id = tk.Label(self, text="Student ID:")
        self.lbl_student_id.pack()
        self.entry_student_id = ttk.Entry(self)
        self.entry_student_id.pack()

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()
        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.btn_assign = ttk.Button(self, text="Assign", command=self.assign_course)
        self.btn_assign.pack(pady=10)

    def assign_course(self):
        student_id = self.entry_student_id.get()
        course_id = self.entry_course_id.get()

        # Check if the student ID and course ID combination already exists
        if self.is_assignment_exists(student_id, course_id):
            messagebox.showerror("Error", "Course already assigned to the student.")
            return

        # Insert the enrollment details into the database
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Enrollment (StudentID, CourseID) VALUES (?, ?)", (student_id, course_id))
        self.connection.commit()
        messagebox.showinfo("Success", "Course assigned to student successfully.")

    def is_assignment_exists(self, student_id, course_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Enrollment WHERE StudentID = ? AND CourseID = ?", (student_id, course_id))
        return cursor.fetchone() is not None

class InputMarksForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.connection = connection
        self.title("Input Marks")
        self.geometry("500x400")

        self.lbl_title = tk.Label(self, text="Input Marks", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_student_id = tk.Label(self, text="Student ID:")
        self.lbl_student_id.pack()
        self.entry_student_id = ttk.Entry(self)
        self.entry_student_id.pack()

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()
        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.lbl_assignment = tk.Label(self, text="Assignment:")
        self.lbl_assignment.pack()
        self.entry_assignment = ttk.Entry(self)
        self.entry_assignment.pack()

        self.lbl_quiz = tk.Label(self, text="Quiz:")
        self.lbl_quiz.pack()
        self.entry_quiz = ttk.Entry(self)
        self.entry_quiz.pack()

        self.lbl_mid_term = tk.Label(self, text="Mid Term:")
        self.lbl_mid_term.pack()
        self.entry_mid_term = ttk.Entry(self)
        self.entry_mid_term.pack()

        self.lbl_final = tk.Label(self, text="Final:")
        self.lbl_final.pack()
        self.entry_final = ttk.Entry(self)
        self.entry_final.pack()

        self.lbl_project = tk.Label(self, text="Project:")
        self.lbl_project.pack()
        self.entry_project = ttk.Entry(self)
        self.entry_project.pack()

        self.btn_submit = ttk.Button(self, text="Submit", command=self.submit_marks)
        self.btn_submit.pack(pady=10)

    def submit_marks(self):
        # Get student ID, course ID, and marks from input fields
        student_id = self.entry_student_id.get()
        course_id = self.entry_course_id.get()
        assignment = self.entry_assignment.get()
        quiz = self.entry_quiz.get()
        mid_term = self.entry_mid_term.get()
        final = self.entry_final.get()
        project = self.entry_project.get()

        # Insert marks into database
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO Marks (StudentID, CourseID, Assignment, Quiz, MidTerm, Final, Project) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_id, course_id, assignment, quiz, mid_term, final, project)
        )
        self.connection.commit()
        print("Marks added successfully.")



class FacultyViewCoursesForm(tk.Toplevel):
    def __init__(self, connection, faculty_id):
        super().__init__()
        self.title("View Courses")
        self.geometry("400x300")
        self.connection = connection
        self.faculty_id = faculty_id

        self.lbl_title = tk.Label(self, text="Courses Assigned to You", font=("Helvetica", 14))
        self.lbl_title.pack(pady=10)

        # Create a Treeview widget to display the courses
        self.tree = ttk.Treeview(self, columns=("Course ID", "Course Name"))
        self.tree.heading("#0", text="Course ID")
        self.tree.heading("#1", text="Course Name")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Retrieve and display the courses assigned to the faculty
        self.populate_courses()

    def populate_courses(self):
        # Clear previous entries from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Query the database to get the courses assigned to the faculty
        cursor = self.connection.cursor()
        query = "SELECT Courses.CourseID, Courses.Name FROM Courses INNER JOIN FacultyCourses ON Courses.CourseID = FacultyCourses.CourseID WHERE FacultyCourses.FacultyID = ?"
        try:
            cursor.execute(query, (self.faculty_id,))
            courses = cursor.fetchall()
            # Insert the courses into the Treeview
            for course in courses:
                self.tree.insert("", "end", text=course[0], values=( course[1]))
        except Exception as e:
            print("Error fetching courses:", e)
class MarkAttendanceForm(tk.Toplevel):
    def __init__(self, master):
        super()._init_(master)
        self.title("Mark Attendance")
        self.geometry("400x300")

        self.lbl_title = tk.Label(self, text="Mark Attendance", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_student_id = tk.Label(self, text="Student ID:")
        self.lbl_student_id.pack()
        self.entry_student_id = ttk.Entry(self)
        self.entry_student_id.pack()

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()
        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.lbl_date = tk.Label(self, text="Date (YYYY-MM-DD):")
        self.lbl_date.pack()
        self.entry_date = ttk.Entry(self)
        self.entry_date.pack()

        self.lbl_status = tk.Label(self, text="Status (Present/Absent):")
        self.lbl_status.pack()
        self.entry_status = ttk.Entry(self)
        self.entry_status.pack()

        self.btn_mark = ttk.Button(self, text="Mark", command=self.mark_attendance)
        self.btn_mark.pack(pady=10)

    def mark_attendance(self, student_id, course_id, date, status):
        # Insert the attendance details into the database
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Attendance (StudentID, CourseID, Date, Status) VALUES (?, ?, ?, ?)",
                       (student_id, course_id, date, status))
        self.connection.commit()
        print("Attendance marked successfully.")
class ViewMarksForm(tk.Toplevel):
    def __init__(self, master, connection):
        super().__init__(master)
        self.title("View Marks")
        self.geometry("600x400")
        self.connection = connection
        self.master = master
        self.lbl_title = tk.Label(self, text="View Marks", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_course_id = tk.Label(self, text="Course ID:")
        self.lbl_course_id.pack()
        self.entry_course_id = ttk.Entry(self)
        self.entry_course_id.pack()

        self.btn_view = ttk.Button(self, text="View", command=self.view_marks)
        self.btn_view.pack(pady=10)

        # Create a Treeview widget to display the marks
        self.tree = ttk.Treeview(self, columns=("Student ID", "Quiz", "Assignment", "Mid", "Final", "Project"))
        self.tree.heading("#0", text="Student ID")
        self.tree.heading("#1", text="Quiz")
        self.tree.heading("#2", text="Assignment")
        self.tree.heading("#3", text="Mid")
        self.tree.heading("#4", text="Final")
        self.tree.heading("#5", text="Project")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def view_marks(self):
        student_id = self.master.student_id  # Assuming the parent of ViewMarksForm is StudentDashboard
        course_id = self.entry_course_id.get()

        # Retrieve marks for a particular student and course from the database
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Marks WHERE StudentID = ? AND CourseID = ?", (student_id, course_id))
        marks = cursor.fetchall()
        print("Marks for Course", course_id, "and Student ID", student_id)
        for mark in marks:
            print(marks)
            # Display marks in respective columns
            self.tree.insert("", "end",text=mark[0], values=( mark[1], mark[2], mark[3], mark[4], mark[5]))

class ViewAttendanceForm(tk.Toplevel):
    def __init__(self, master):
        super()._init_(master)
        self.title("View Attendance")
        self.geometry("400x300")

        self.lbl_title = tk.Label(self, text="View Attendance", font=("Helvetica", 18))
        self.lbl_title.pack(pady=10)

        self.lbl_student_id = tk.Label(self, text="Student ID:")
        self.lbl_student_id.pack()
        self.entry_student_id = ttk.Entry(self)
        self.entry_student_id.pack()

        self.btn_view = ttk.Button(self, text="View", command=self.view_attendance)
        self.btn_view.pack(pady=10)

        self.txt_attendance = tk.Text(self, height=10, width=50)
        self.txt_attendance.pack(pady=10)

    def view_attendance(self, student_id):
        # Retrieve attendance for a particular student from the database
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Attendance WHERE StudentID = ?", (student_id,))
        attendance = cursor.fetchall()
        print("Attendance:")
        for entry in attendance:
            print(entry)
# class StudentDashboard(tk.Frame):
#     def __init__(self, connection, student_id):
#         super().__init__()
#         self.title("Student Dashboard")
#         self.geometry("600x400")
#         self.connection = connection
#         self.StudentID = student_id
#
#     def create_widgets(self):
#         # Add widgets for student dashboard
#         lbl_title = tk.Label(self, text="Student Dashboard", font=("Helvetica", 18))
#         lbl_title.grid(row=0, column=0, pady=10)
#
#         btn_view_marks = ttk.Button(self, text="View Marks", command=self.view_marks)
#         btn_view_marks.grid(row=1, column=0, padx=10, pady=5, sticky="we")
#
#         btn_view_attendance = ttk.Button(self, text="View Attendance", command=self.view_attendance)
#         btn_view_attendance.grid(row=1, column=1, padx=10, pady=5, sticky="we")
#
#
#         self.btn_view_courses = ttk.Button(self, text="View Courses", command=self.view_courses)
#         self.btn_view_courses.pack()
#         btn_logout = ttk.Button(self, text="Logout", command=self.logout)
#         btn_logout.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")
#
#     def view_marks(self):
#         # Open the view marks form
#         ViewMarksForm(self)
#
#     def view_attendance(self):
#         # Open the view attendance form
#         ViewAttendanceForm(self)
#
#     def view_courses(self):
#         ViewCoursesForm(self, self.connection, self.StudentID)
#
#     def logout(self):
#         # You can destroy the current frame or window to log out the user
#         self.destroy()
#         # Then, show the welcome page again
#         self.master.show_welcome_page()
class AdminDashboard(tk.Frame):
    def __init__(self, master, connection):
        super().__init__(master)
        self.master = master
        self.connection = connection
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="Admin Dashboard", font=("Helvetica", 18))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=10)

        btn_add_student = ttk.Button(self, text="Add Student", command=self.add_student)
        btn_add_student.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        btn_assign_course_to_student = ttk.Button(self, text="Assign Course to Student", command=self.assign_course_to_student)
        btn_assign_course_to_student.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        btn_add_faculty = ttk.Button(self, text="Add Faculty", command=self.add_faculty)
        btn_add_faculty.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        btn_add_course = ttk.Button(self, text="Add Course", command=self.add_course)
        btn_add_course.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        btn_assign_course_to_faculty = ttk.Button(self, text="Assign Course to Faculty", command=self.assign_course_to_faculty)
        btn_assign_course_to_faculty.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        btn_logout = ttk.Button(self, text="Logout", command=self.logout)
        btn_logout.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def add_faculty(self):
        AddFacultyForm(self, self.connection)

    def add_student(self):
        AddStudentForm(self, self.connection)

    def add_course(self):
        AddCourseForm(self, self.connection)

    def assign_course_to_faculty(self):
        AssignCourseToFacultyForm(self, self.connection)

    def assign_course_to_student(self):
        AssignCourseToStudentForm(self, self.connection)

    def logout(self):
        self.destroy()
        self.master.show_welcome_page()

class FacultyDashboard(tk.Frame):
    def __init__(self, master, connection, faculty_id):
        super().__init__(master)
        self.master = master
        self.connection = connection
        self.faculty_id = faculty_id
        self.create_widgets()

    def create_widgets(self):
        # Add widgets for faculty dashboard
        lbl_title = tk.Label(self, text="Faculty Dashboard", font=("Helvetica", 18))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=10)
        btn_input_marks = ttk.Button(self, text="Input Marks", command=self.input_marks)
        btn_input_marks.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        btn_mark_attendance = ttk.Button(self, text="Mark Attendance", command=self.mark_attendance)
        btn_mark_attendance.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        btn_view_courses = ttk.Button(self, text="View Courses", command=self.view_courses)
        btn_view_courses.grid(row=2, column=2, padx=10, pady=5, sticky="we")
        btn_logout = ttk.Button(self, text="Logout", command=self.logout)
        btn_logout.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def input_marks(self):
        InputMarksForm(self, self.connection)

    def mark_attendance(self):
        # Prompt the user to enter attendance details
        student_id = input("Enter Student ID: ")
        course_id = input("Enter Course ID: ")
        date = input("Enter Date (YYYY-MM-DD): ")
        status = input("Enter Status (Present/Absent): ")

        # Insert the attendance details into the database
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Attendance (StudentID, CourseID, Date, Status) VALUES (?, ?, ?, ?)",
                       (student_id, course_id, date, status))
        self.connection.commit()
        print("Attendance marked successfully.")

    def view_courses(self):
        FacultyViewCoursesForm(self.connection, self.faculty_id)

    def logout(self):
        self.destroy()
        self.master.show_welcome_page()

class StudentDashboard(tk.Frame):
    def __init__(self, master, connection, student_id):
        super().__init__(master)
        self.student_id = student_id
        self.master = master
        self.connection = connection
        self.create_widgets()
    def create_widgets(self):
        # Add widgets for student dashboard
        lbl_title = tk.Label(self, text="Student Dashboard", font=("Helvetica", 18))
        lbl_title.grid(row=0, column=0, pady=10)

        btn_view_marks = ttk.Button(self, text="View Marks", command=self.view_marks)
        btn_view_marks.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        btn_view_attendance = ttk.Button(self, text="View Attendance", command=self.view_attendance)
        btn_view_attendance.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        btn_view_courses = ttk.Button(self, text="View Assigned Courses", command=self.view_courses)
        btn_view_courses.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        btn_logout = ttk.Button(self, text="Logout", command=self.logout)
        btn_logout.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def view_marks(self):
        ViewMarksForm(self, self.connection)

    def view_attendance(self):
        # Retrieve attendance for a particular student from the database
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Attendance WHERE StudentID = ?", (self.student_id,))
        attendance = cursor.fetchall()
        print("Attendance:")
        for entry in attendance:
            print(entry)

    def view_courses(self):
        ViewCoursesForm(self.connection, self.student_id)

    def logout(self):
        self.destroy()
        self.master.show_welcome_page()


class WelcomePage(tk.Frame):
    def __init__(self, master, connection):
        super().__init__(master)
        self.master = master
        self.connection = connection
        self.database_manager = DatabaseManager(connection)
        self.database_manager.create_tables()
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="Welcome to Learning Management System", font=("Helvetica", 18))
        lbl_title.pack(pady=20)

        self.lbl_status = tk.Label(self, text="", fg="red")
        self.lbl_status.pack()

        lbl_username = tk.Label(self, text="Username:")
        lbl_username.pack()
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack()

        lbl_password = tk.Label(self, text="Password:")
        lbl_password.pack()
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack()

        btn_login = ttk.Button(self, text="Login", command=self.login)
        btn_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        cursor = self.connection.cursor()

        # Check if the user is an admin
        if username == "admin" and password == "admin":
            self.destroy()
            admin_dashboard = AdminDashboard(self.master, self.connection)
            admin_dashboard.pack(fill=tk.BOTH, expand=True)
            return

        # Check if the user is a faculty
        try:
            username_int = int(username)  # Convert username to integer
        except ValueError:
            self.lbl_status.config(text="Invalid username format.")
            return

        cursor.execute("SELECT * FROM Faculty WHERE FacultyID = ? AND Password = ?", (username_int, password))
        faculty = cursor.fetchone()
        if faculty:
            # Retrieve the faculty ID
            faculty_id = faculty[0]  # Assuming the faculty ID is the first column in the table
            self.destroy()
            faculty_dashboard = FacultyDashboard(self.master, self.connection, faculty_id)
            faculty_dashboard.pack(fill=tk.BOTH, expand=True)
            return

        # Check if the user is a student
        cursor.execute("SELECT * FROM Students WHERE StudentID = ? AND Password = ?", (username, password))
        student = cursor.fetchone()
        if student:
            # Retrieve the student ID
            student_id = student[0]  # Assuming the student ID is the first column in the table
            self.destroy()
            student_dashboard = StudentDashboard(self.master, self.connection, student_id)
            student_dashboard.pack(fill=tk.BOTH, expand=True)
            return

        self.lbl_status.config(text="Invalid username or password.")


class LMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning Management System")
        self.geometry("600x400")
        self.connection = self.connect_to_database()
        self.welcome_page = WelcomePage(self, self.connection)
        self.welcome_page.pack(fill=tk.BOTH, expand=True)

    def connect_to_database(self):
        server = 'DESKTOP-KFOP342\\SQLEXPRESS'

        database = 'LMSDatabase'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection'
                                                                                               '=yes;')
        return connection

    def show_welcome_page(self):
        self.welcome_page = WelcomePage(self, self.connection)
        self.welcome_page.pack(fill=tk.BOTH, expand=True)

def main():
    app = LMSApp()
    app.mainloop()

if __name__ == "__main__":
    main()