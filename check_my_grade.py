import csv
import os
import hashlib
import statistics
import time

users_csv = "login.csv"
students_csv = "student.csv"
professors_csv = "professor.csv"
courses_csv = "course.csv"
grades_csv = "grades.csv"

class Student:
    def __init__(self, first_name, last_name, email_address, courses="", grades="", marks=""):
        """Initialize student"""
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.courses = courses
        self.grades = grades
        self.marks = marks

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"Student(first_name={self.first_name}, last_name={self.last_name}, email_address={self.email_address}, courses={self.courses}, grades={self.grades}, marks={self.marks})"

    def __str__(self):
        """Returns a human-readable string representation."""
        return f"Student(first_name={self.first_name}, last_name={self.last_name}, email_address={self.email_address}, courses={self.courses}, grades={self.grades}, marks={self.marks})"

    def course_list(self):
        """Returns a list of courses the student is enrolled in."""
        return self.courses.split(",")

    def grade_list(self):
        """Returns a list of grades for the student’s courses."""
        return self.grades.split(",")

    def marks_list(self):
        """Returns a list of marks for the student’s courses."""
        return self.marks.split(",")

    def course_dict(self):
        """Returns a dictionary mapping courses to grades and marks."""
        course_dict = {}
        grade_list = self.grade_list()
        marks_list = self.marks_list()
        course_list = self.course_list()
        for i in range(len(course_list)):
            if not self.grades:
                course_dict[course_list[i]] = {"grade": "", "marks": ""}
            else:
                course_dict[course_list[i]] = {"grade": grade_list[i], "marks": marks_list[i]}
        return course_dict

    def course_dict_to_string(self, course_dict):
        """Updates student grades and marks from a dictionary."""
        self.grades = ""
        self.marks = ""
        for course in self.course_list():
            self.add_grade(course_dict[course]["grade"])
            self.add_marks(course_dict[course]["marks"])

    def add_course(self, course_id):
        """Adds a new course to the student’s list."""
        if not self.courses:
            self.courses = course_id
        else:
            self.courses = self.courses + "," + course_id

    def add_grade(self, grade_id):
        """Adds a grade for a specific course."""
        if not self.grades:
            self.grades = grade_id
        else:
            self.grades = self.grades + "," + grade_id

    def add_marks(self, marks):
        """Adds marks for a specific course."""
        if not self.marks:
            self.marks = marks
        else:
            self.marks = self.marks + "," + marks

    def update_first_name(self, first_name):
        """Updates the student’s first name."""
        self.first_name = first_name

    def update_last_name(self, last_name):
        """Updates the student’s last name."""
        self.last_name = last_name

    def check_my_grades(self):
        """Prints the student’s grades for each course."""
        course_dict = self.course_dict()
        for course in course_dict:
            print(f"Course: {course}, Grade: {course_dict[course]["grade"]}")

    def check_my_marks(self):
        """Prints the student’s marks for each course."""
        course_dict = self.course_dict()
        for course in course_dict:
            print(f"Course: {course}, Marks: {course_dict[course]["marks"]}")

    def to_dict(self):
        """Converts student details into a dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "courses": self.courses,
            "grades": self.grades,
            "marks": self.marks
        }


class StudentManagement:
    def __init__(self):
        """Initialize student management"""
        self.students = self.load_students()
        self.student_dict = {student.email_address: student for student in self.students}

    def load_students(self):
        """Load student objs from csv"""
        if os.path.exists(students_csv):
            with open(students_csv, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                students = [Student(**record) for record in reader]
                return students
        return []

    def save_students(self, data):
        """Saves student objs in csv"""
        data = [student.to_dict() for student in data]
        fieldnames = data[0].keys()
        with open(students_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        self.reload_students()

    def reload_students(self):
        """Reloads student objs"""
        self.students = self.load_students()
        self.student_dict = {student.email_address: student for student in self.students}

    def display_given_students(self, students):
        """Displays a list of specific students."""
        print("*********Students**************")
        for student in students:
            print(student)
        print("*******************************")

    def display_students(self):
        """Displays a list of all students."""
        print("*********Students**************")
        for student in self.students:
            print(student)
        print("*******************************")

    def get_student(self, email_address):
        """Finds and returns a student by their email."""
        return self.student_dict[email_address]

    def get_students(self, search_key):
        """Searches for students by name, email, or course details."""
        student_list = []
        for student in self.students:
            if search_key in student.first_name or \
            search_key in student.last_name or \
            search_key in student.email_address or \
            search_key in student.courses or \
            search_key in student.courses or \
            search_key in student.marks or \
            search_key in student.grades:
                student_list.append(student)
        return student_list

    def add_new_student(self, student):
        """Adds a new student to list, dioct and csv."""
        self.student_dict[student.email_address] = student
        self.save_students(self.student_dict.values())

    def delete_student(self, email_address):
        """Removes a student from list, dioct and csv."""
        self.student_dict.pop(email_address)
        self.save_students(self.student_dict.values())

    def update_student(self, student):
        """Updates student in list, dioct and csv."""
        self.student_dict.pop(student.email_address)
        self.student_dict[student.email_address] = student
        self.save_students(self.student_dict.values())

    def assign_course(self, student, course_id):
        """Assigns a course to a student."""
        if course_id not in student.course_list():
            student.add_course(course_id)
            self.update_student(student)
        else:
            print("*********Student is already part of this cours*********")

    def add_grade(self, student, course_id, grade, marks):
        """Assigns a grade and marks to a student for a course."""
        student_course_dict = student.course_dict()
        if course_id in student_course_dict:
            student_course_dict[course_id] = {"grade": grade, "marks": marks}
            student.course_dict_to_string(student_course_dict)
            self.update_student(student)
        else:
            print("*******Error, student not part of the course*********")

    def course_students(self, course_id):
        """Retrieves a list of students enrolled in a course."""
        student_list = []
        student_dict = {}
        for student in self.students:
            course_dict = student.course_dict()
            if course_id in course_dict:
                student_list.append(f"Student Email: {student.email_address} Name: {student.first_name} {student.last_name}, Grade: {course_dict[course_id]["grade"]}, Marks: {course_dict[course_id]["marks"]}")
                student_dict[student.email_address] = {"email_address": f"{student.email_address}","name": f"{student.first_name} {student.last_name}", "grade": course_dict[course_id]["grade"], "marks": course_dict[course_id]["marks"]}
        return student_list, student_dict

    def course_mark_stats(self, student_dict):
        """Calculates and returns course statistics (min, max, avg, median)."""
        stats =  {"min": 0, "max": 0, "avg":0, "median": 0}
        marks_list = [int(student_dict[student]["marks"]) for student in student_dict if student_dict[student]["marks"]]
        if student_dict:
            stats["min"] = min(marks_list)
            stats["max"] = max(marks_list)
            stats["avg"] = sum(marks_list)/len(marks_list)
            stats['median'] = statistics.median(marks_list)
        return stats


class Professor:
    def __init__(self, name, email_address, rank, courses=""):
        """Initialize professor"""
        self.name = name
        self.email_address = email_address
        self.rank = rank
        self.courses = courses

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"Professor(name={self.name}, email_address={self.email_address}, rank={self.rank}, courses={self.courses})"

    def __str__(self):
        """Returns a human-readable string representation."""
        return f"(name={self.name}, email_address={self.email_address}, rank={self.rank}, courses={self.courses})"

    def update_name(self, name):
        """Updates professor's name"""
        self.name = name

    def update_rank(self, rank):
        """Updates professor's rank"""
        self.rank = rank

    def course_list(self):
        """Gets professor's course list"""
        return self.courses.split(",")

    def add_course(self, course_id):
        """Adds course to a professor"""
        if not self.courses:
            self.courses = course_id
        else:
            self.courses = self.courses + "," + course_id

    def to_dict(self):
        """Converts professor obj to a dict"""
        return {
            "name": self.name,
            "email_address": self.email_address,
            "rank": self.rank,
            "courses": self.courses,
        }


class ProfessorManagement:
    """Initialize professor management"""
    def __init__(self):
        self.professors = self.load_professors()
        self.professor_dict = {professor.email_address: professor for professor in self.professors}

    def load_professors(self):
        """Load professor objs from csv"""
        if os.path.exists(professors_csv):
            with open(professors_csv, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                professors = [Professor(**record) for record in reader]
                return professors
        return []

    def save_professors(self, data):
        """Save professor objs to csv"""
        data = [professor.to_dict() for professor in data]
        fieldnames = data[0].keys()
        with open(professors_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        self.reload_professors()

    def reload_professors(self):
        """Reload professor objs"""
        self.professors = self.load_professors()
        self.professor_dict = {professor.email_address: professor for professor in self.professors}

    def display_professors(self):
        """Display professor objs"""
        print("*********Professors**************")
        for professor in self.professors:
            print(professor)
        print("*******************************")

    def add_new_professor(self, professor):
        """Adds new professor to list, dict and csv"""
        self.professor_dict[professor.email_address] = professor
        self.save_professors(self.professor_dict.values())

    def delete_professor(self, email_address):
        """Deletes existing professor from list, dict and csv"""
        self.professor_dict.pop(email_address)
        self.save_professors(self.professor_dict.values())

    def get_professor(self, email_address):
        """Gets professor given email_address"""
        return self.professor_dict[email_address]

    def assign_course(self, professor, course_id):
        """Assigns course to a professor"""
        if course_id not in professor.course_list():
            professor.add_course(course_id)
            self.update_professor(professor)
        else:
            print("Professor is currently teaching the course")

    def update_professor(self, professor):
        """Updates professor"""
        self.professor_dict.pop(professor.email_address)
        self.professor_dict[professor.email_address] = professor
        self.save_professors(self.professor_dict.values())

    def add_student_grade(self, student_email, course_id, grade, marks):
        """Adds grade to a student"""
        try:
            student = student_management.get_student(student_email)
            student_management.add_grade(student, course_id, grade, marks)
        except Exception as e:
            print(f"*******Error, {str(e)}*********")


class User:
    def __init__(self, user_id, password, role):
        """Initializes user."""
        self.user_id = user_id
        self.password = password
        self.role = role

    def set_password(self, password):
        """Sets user's password."""
        self.password = password

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"User(user_id={self.user_id}, password={self.password}, role={self.role})"

    def __str__(self):
        """Returns a human-readable string representation."""
        return f"{self.user_id}, {self.password}, {self.role}"

    def to_dict(self):
        """Converts user obj to a dict."""
        return {"user_id": self.user_id, "password": self.password, "role": self.role}


class UserManagement:
    def __init__(self):
        """Initializes user management."""
        self.users = self.load_users()
        self.users_dict = {user.user_id: user for user in self.users}

    def load_users(self):
        """Loads user objs from csv."""
        if os.path.exists(users_csv):
            with open(users_csv, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                users = [User(**record) for record in reader]
                return users
        return []

    def view_users(self):
        """Displays user objs."""
        print("*********Users**************")
        print("Students are of type student, Professors are of type professor")
        for user in self.users:
            print(user)
        print("*******************************")

    def add_user(self, user):
        """Adds user obj to list, dict and csv."""
        self.users_dict[user.user_id] = user
        self.save_users(self.users_dict.values())

    def check_user(self, user_id):
        """Checks for user in dict."""
        return user_id in self.users_dict

    def get_user(self, user_id):
        """Gets user from dict."""
        return self.users_dict[user_id]

    def update_user(self, user):
        """Updates user obj in list, dict and csv."""
        self.users_dict[user.user_id] = user
        self.save_users(self.users_dict.values())

    def delete_user(self, user_id):
        """Deletes user obj in list, dict and csv."""
        self.users_dict.pop(user_id)
        self.save_users(self.users_dict.values())

    def save_users(self, data):
        """Saves user obj to csv."""
        data = [user.to_dict() for user in data]
        fieldnames = data[0].keys()
        with open(users_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        self.reload_users()

    def reload_users(self):
        """Reloads user objs."""
        self.users = self.load_users()
        self.users_dict = {user.user_id: user for user in self.users}

    def login(self, user_id, password, user_input):
        """User login give user_id and password."""
        if user_id in self.users_dict and self.users_dict[user_id].role == user_input:
            if self.verify_password(password, self.users_dict[user_id].password):
                print("Successfully logged in")
                return True
        return False

    def encrypt_password(self, password):
        """Encrypts user password."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def change_password(self, user_id, password):
        """Changes user password."""
        user = self.get_user(user_id)
        user.set_password(hashlib.sha256(password.encode("utf-8")).hexdigest())
        self.update_user(user)

    def verify_password(self, password, hashed_password):
        """Decrypts and verify's user password."""
        return hashed_password == self.encrypt_password(password)

user_management = UserManagement()
student_management = StudentManagement()
professor_management = ProfessorManagement()

class Course:
    def __init__(self, course_id, credits, course_name, course_desc):
        """Initializes course."""
        self.course_id = course_id
        self.credits = credits
        self.course_name = course_name
        self.course_desc = course_desc

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"Course(course_id={self.course_id}, credits={self.credits}, course_name={self.course_name}, course_desc={self.course_desc})"

    def __str__(self):
        """Returns a human-readable string representation."""
        return f"Course(course_id={self.course_id}, credits={self.credits}, course_name={self.course_name}, course_desc={self.course_desc})"

    def to_dict(self):
        """Converts course obj to dict."""
        return {
            "course_id": self.course_id,
            "credits": self.credits,
            "course_name": self.course_name,
            "course_desc": self.course_desc
        }


class CourseManagement:
    def __init__(self):
        """Initialize course management."""
        self.courses = self.load_courses()
        self.course_dict = {course.course_id: course for course in self.courses}

    def get_course(self, course_id):
        """Gets course obj"""
        return self.course_dict[course_id]

    def load_courses(self):
        """Gets course objs from csv."""
        if os.path.exists(courses_csv):
            with open(courses_csv, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                courses = [Course(**record) for record in reader]
                return courses
        return []

    def save_courses(self, data):
        """Saves course objs to csv."""
        data = [course.to_dict() for course in data]
        fieldnames = data[0].keys()
        with open(courses_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        self.reload_courses()

    def reload_courses(self):
        """Reloads course objs."""
        self.courses = self.load_courses()
        self.course_dict = {courses.course_id: courses for courses in self.courses}

    def display_courses(self):
        """Displays course objs."""
        print("*********Courses**************")
        for course in self.courses:
            print(course)
        print("*******************************")

    def add_new_course(self, course):
        """Adds new course."""
        self.course_dict[course.course_id] = course
        self.save_courses(self.course_dict.values())

    def update_course(self, course):
        """Updates existing course."""
        self.course_dict[course.course_id] = course
        self.save_courses(self.course_dict.values())

    def delete_course(self, course_id):
        """Delets a course."""
        self.course_dict.pop(course_id)
        self.save_courses(self.course_dict.values())


course_management = CourseManagement()


class Grade:
    def __init__(self, grade_id, grade, marks_range):
        """Initialize grade"""
        self.grade_id = grade_id
        self.grade = grade
        self.marks_range = marks_range

    def __repr__(self):
        """Represents grade"""
        return f"Grade(grade_id={self.grade_id}, grade={self.grade}, marks_range={self.marks_range})"

    def to_dict(self):
        """Converts grade to dict"""
        return {
            "grade_id": self.grade_id,
            "grade": self.grade,
            "marks_range": self.marks_range,
        }

class GradeManagement:
    def __init__(self):
        """Initialize grade management"""
        self.grades = self.load_grades()
        self.grade_dict = {grade.grade_id: grade for grade in self.grades}
        self.save_grades(self.grade_dict.values())

    def load_grades(self):
        """Loads grade objs from csv"""
        if os.path.exists(grades_csv):
            with open(grades_csv, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                grades = [Grade(**record) for record in reader]
                return grades
        return []

    def save_grades(self, data):
        """Saves grade objs to csv"""
        data = [grade.to_dict() for grade in data]
        fieldnames = data[0].keys()
        with open(grades_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        self.reload_grades()

    def reload_grades(self):
        """Reloads grade objs"""
        self.grades = self.load_grades()
        self.grade_dict = {grade.grade_id: grade for grade in self.grades}

    def display_grades(self):
        """Display grade objs"""
        print("*********Grade Catalog**************")
        for grade in self.grades:
            print(grade)
        print("*******************************")

    def add_grade(self, grade):
        """Adds grade to list, dict and csv"""
        self.grade_dict[grade.grade_id] = grade
        self.save_grades(self.grade_dict.values())

    def delete_grade(self, grade_id):
        """Deletes grade from list, dict and csv"""
        self.grade_dict.pop(grade_id)
        self.save_grades(self.grade_dict.values())

    def update_grade(self, grade):
        """Updates grade in list, dict and csv"""
        self.grade_dict[grade.grade_id] = grade
        self.save_grades(self.grade_dict.values())

grade_management = GradeManagement()

def main():
    while True:
        print("\nWelcome to Check My Grade Application")
        user_input = input("Enter student (for student)\n or professor (for professor): ")
        if user_input == "student":
            print("********Login********")
            user_id = input("Enter email: ")
            password = input("Enter password: ")
            if user_management.login(user_id, password, user_input):
                while True:
                    student = student_management.get_student(user_id)
                    student_input = input((
                    "1 (for student record) \n"
                    "2 (to update student record) \n"
                    "3 (to select a course) \n"
                    "4 (check my grades) \n"
                    "5 (check my marks) \n"
                    "6 (to delete your account) \n"
                    "7 (to reset password) \n"
                    "10 (to log out) \n"
                    ))
                    if student_input == "1":
                        print(student)
                    elif student_input == "2":
                        modify_first_name= input("Enter first name to modify: ")
                        student.update_first_name(modify_first_name)
                        modify_last_name = input("Enter last name to modify: ")
                        student.update_last_name(modify_last_name)
                        student_management.update_student(student)
                    elif student_input == "3":
                        try:
                            course_management.display_courses()
                            selected_course_id = input("Select course id: ")
                            if selected_course_id not in course_management.course_dict:
                                raise Exception("********Not a valid course id********")

                            student_management.assign_course(student, selected_course_id)
                            print("********Succesfully added the course********")
                        except Exception as e:
                            print(f"Error: {str(e)}")
                            print("********Error assigning a course, please try again********")
                    elif student_input == "4":
                        print("*********Displaying Grades**************")
                        student.check_my_grades()
                        print("****************************************")
                    elif student_input == "5":
                        print("*********Displaying Marks**************")
                        student.check_my_marks()
                        print("***************************************")
                    elif student_input == "6":
                         registration = input("Are you sure to delete your account, enter yes for confirmation: ")
                         if registration == "yes":
                            student_management.delete_student(user_id)
                            user_management.delete_user(user_id)
                            print("********Succesfully deleted student account********")
                            break
                    elif student_input == "7":
                        password = input("Enter new password: ")
                        user_management.change_password(user_id, password)
                        print("Password reset successful")
                        break
                    elif student_input == "10":
                        break
                    else:
                        print("Invalid input")
            else:
                print("********student email not found, do you want to register?********")
                registration = input("Enter yes for account registration or else no: ")
                if registration == "yes":
                    
                    if not user_management.check_user(user_id):
                        first_name = input("Enter first name: ")
                        last_name = input("Enter last name: ")
                        user = User(user_id, user_management.encrypt_password(password), "student")
                        user_management.add_user(user)
                        student = Student(first_name, last_name, user_id)
                        student_management.add_new_student(student)
                        print("********Successfully registered the student account********")
                    else:
                        print("********student email is already taken, try with different email******")
                else:
                    print("Skip login")

        elif user_input == "professor":
            print("********Login********")
            user_id = input("Enter email: ")
            password = input("Enter password: ")
            if user_management.login(user_id, password, user_input):
                while True:
                    professor = professor_management.get_professor(user_id)
                    professor_input = input((
                    "1 (for professor details) \n"
                    "2 (for modify details) \n"
                    "3 (to manage courses) \n"
                    "5 (for students records)  \n"
                    "6 (to search students)  \n"
                    "7 (to display course students)  \n"
                    "8 (to manage grades)  \n"
                    "9 (to delete professor account)  \n"
                    "10 (to log out) \n"
                    "11 (to reset password) \n"
                    ))
                    if professor_input == "1":
                        print(professor)
                    elif professor_input == "2":
                        modify_name= input("Enter name to modify: ")
                        professor.update_name(modify_name)
                        modify_rank = input("Enter rank to modify: ")
                        professor.update_rank(modify_rank)
                        professor_management.update_professor(professor)
                    elif professor_input == "3":
                        while True:
                            course_input = input((
                            "1 (to add new course) \n"
                            "2 (to modify existing course) \n"
                            "3 (to delete a course) \n"
                            "4 (to self assign course) \n"
                            "10 (to exit courses) \n"
                            ))
                            course_management.display_courses()
                            if course_input == "1":
                                try:
                                    course_id = input("Enter course id: ")
                                    credits = input("Enter credits: ")
                                    course_name = input("Enter course name: ")
                                    course_desc = input("Enter course description: ")
                                    if course_id not in course_management.course_dict:
                                        course = Course(course_id, credits, course_name, course_desc)
                                        course_management.add_new_course(course)
                                        print(f"********Successfully created new {course} *******")
                                    else:
                                        print(f"********Course id already exists*******")
                                except Exception as e:
                                    print("********Error adding a new course, please try again********")
                            elif course_input == "2":
                                modify_course_id= input("Enter course id to modify: ")
                                modify_course_credits = input("Enter course credits to modify: ")
                                modify_course_name = input("Enter course name to modify: ")
                                modify_course_desc = input("Enter course description to modify: ")
                                if modify_course_id in course_management.course_dict:
                                    course = Course(modify_course_id, modify_course_credits, modify_course_name, modify_course_desc)
                                    course_management.update_course(course)
                                    print("***********Succesfully modified existing Course**********")
                                else:
                                    print("***********Course id doesn't exist**********")
                            elif course_input == "3":
                                delete_course_id = input("Enter Course id to delete: ")
                                if delete_course_id in course_management.course_dict:
                                    course_management.delete_course(delete_course_id)
                                    print("***********Succesfully deleted a Course**********")
                                else:
                                    print("***********Course id doesn't exist**********")
                            elif course_input == "4":
                                try:
                                    course_management.display_courses()
                                    selected_course_id = input("Select course id: ")
                                    if selected_course_id not in course_management.course_dict:
                                        raise Exception("Not a valid course id")

                                    professor_management.assign_course(professor, selected_course_id)
                                    print("********Succesfully added the course for teaching********")
                                except Exception as e:
                                    print(f"Error: {str(e)}")
                                    print("********Error assigning a course, please try again********")
                            elif course_input == "10":
                                break
                    elif professor_input == "5":
                        print("********Displaying all students********")
                        student_management.display_students()
                    elif professor_input == "6":
                        search_key = input("Enter key to search for students: ")
                        start = time.time()
                        retr_student_list = student_management.get_students(search_key)
                        end = time.time()
                        print(f"Time taken to get search results: {(end - start)*1000} ms")
                        print(f"********Search result for key: {search_key}, time elapsed: {(end - start)*1000} ms ********")
                        for student in retr_student_list:
                            print(student)
                        print("********************************************")

                    elif professor_input == "7":
                        prof_course_list = professor.course_list()
                        print("********Displaying professor Courses********")
                        for course in prof_course_list:
                            course_obj = course_management.get_course(course)
                            print(course_obj)
                        print("********************************************")

                        selected_course_id = input("Select course id: ")
                        if selected_course_id not in professor.course_list():
                            print("********Not a valid professor course id********")
                        print("********Displaying Course Report********")

                        student_list, student_dict = student_management.course_students(selected_course_id)
                        for student in student_list:
                            print(student)
                        print("******************************************\n")

                        print("************Course Stats*****************")
                        print(student_management.course_mark_stats(student_dict))
                        print("******************************************\n")

                        while True:
                            grade_input = input((
                            "1 (to assign student a grade) \n"
                            "2 (to modify grade) \n"
                            "3 (to sort students by grade) \n"
                            "4 (to sort students by email) \n"
                            "5 (to sort students by marks) \n"
                            "10 (to exit grades) \n"
                            ))

                            grade_management.display_grades()

                            if grade_input == "1":
                                student_email = input("Enter student email: ")
                                student_grade_id = input("Enter student grade: ")
                                student_marks = input("Enter student marks: ")
                                professor_management.add_student_grade(student_email, selected_course_id, student_grade_id, student_marks)

                            elif grade_input == "2":
                                student_email = input("Enter student email to modify grade: ")
                                student_grade_id = input("Enter new grade for student: ")
                                student_marks = input("Enter new marks for student: ")
                                professor_management.add_student_grade(student_email, selected_course_id, student_grade_id, student_marks)
                            elif grade_input == "3":
                                sorted_students = sorted(student_dict.values(), key=lambda x: x["grade"])
                                print("********Displaying Students Sorted By Grades********")
                                for student in sorted_students:
                                    print(student)
                                print("********************************************")
                            elif grade_input == "4":
                                sorted_students = sorted(student_dict.values(), key=lambda x: x["email_address"])
                                print("********Displaying Students Sorted By Email********")
                                for student in sorted_students:
                                    print(student)
                                print("********************************************")
                            elif grade_input == "5":
                                sorted_students = sorted(student_dict.values(), key=lambda x: x["marks"], reverse=True)
                                print("********Displaying Students Sorted By Marks********")
                                for student in sorted_students:
                                    print(student)
                                print("********************************************")
                            elif grade_input == "10":
                                break
                            else:
                                print("Invalid input")

                    elif professor_input == "8":

                        grade_management.display_grades()

                        while True:
                            grade_input = input((
                            "1 (to add new grade) \n"
                            "2 (to modify existing grade) \n"
                            "3 (to delete a grade) \n"
                            "10 (to exit grades) \n"
                            ))

                            grade_management.display_grades()

                            if grade_input == "1":
                                new_grade_id = input("Enter grade id: ")
                                new_grade = input("Enter grade: ")
                                new_marks_range = input("Enter marks range: ")
                                if new_grade_id not in grade_management.grade_dict:
                                    grade = Grade(new_grade_id, new_grade, new_marks_range)
                                    grade_management.add_grade(grade)
                                    print("***********Succesfully added a new grade**********")
                                else:
                                    print("***********Grade is already taken**********")
                            elif grade_input == "2":
                                modify_grade_id = input("Enter grade id to modify: ")
                                modify_grade = input("Enter grade to modify: ")
                                modify_marks_range = input("Enter marks range to modify: ")
                                if modify_grade_id in grade_management.grade_dict:
                                    grade = Grade(modify_grade_id, modify_grade, modify_marks_range)
                                    grade_management.update_grade(grade)
                                    print("***********Succesfully modified existing grade**********")
                                else:
                                    print("***********Grade id doesn't exist**********")
                            elif grade_input == "3":
                                delete_grade_id = input("Enter grade id to delete: ")
                                if delete_grade_id in grade_management.grade_dict:
                                    grade_management.delete_grade(delete_grade_id)
                                    print("***********Succesfully deleted a grade**********")
                                else:
                                    print("***********Grade id doesn't exist**********")
                            elif grade_input == "10":
                                break
                            else:
                                print("Invalid input")

                    elif professor_input == "9":
                        registration = input("Are you sure to delete your account, enter yes for confirmation: ")
                        if registration == "yes":
                            professor_management.delete_professor(user_id)
                            user_management.delete_user(user_id)
                            print("********Succesfully deleted professor account********")
                            break

                    elif professor_input == "10":
                        break
                    elif professor_input == "11":
                        password = input("Enter new password: ")
                        user_management.change_password(user_id, password)
                        print("Password reset successful")
                        break
                    else:
                        print("Invalid input")

            else:
                print("********professor email not found, do you want to register?********")
                registration = input("Enter yes for account registration or else no: ")
                if registration == "yes":
                    
                    if not user_management.check_user(user_id):
                        name = input("Enter name: ")
                        rank = input("Enter rank: ")
                        user = User(user_id, user_management.encrypt_password(password), "professor")
                        user_management.add_user(user)

                        professor = Professor(name, user_id, rank)
                        professor_management.add_new_professor(professor)
                        print("********Successfully registered the professor account********")
                    else:
                        print("********student email is already taken, try with different email******")
                else:
                    print("Skip login")
        else:
            print("********Invalid user type********")

if __name__ == "__main__":
    main()
