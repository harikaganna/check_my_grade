import unittest
import time
from datetime import datetime
from random import randint
from check_my_grade import Student, StudentManagement, Course, CourseManagement, Professor, ProfessorManagement, Grade, GradeManagement, User, UserManagement

class TestCheckMyGrade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up initial data for testing."""
        cls.student_management = StudentManagement()
        cls.course_management = CourseManagement()
        cls.professor_management = ProfessorManagement()
        cls.grade_management = GradeManagement()
        cls.user_management = UserManagement()

    def test_add_delete_modify_student(self):
        """Test adding, modifying, and deleting students."""
        email_prefix = "test_student"
        added_students = []

        # Add 1000 students
        for i in range(1000):
            email = f"{email_prefix}{i}@school.com"
            student = Student(f"First{i}", f"Last{i}", email)
            self.student_management.add_new_student(student)
            added_students.append(email)

        self.assertGreater(len(self.student_management.students), 1000)

        # Modify a student
        student = self.student_management.get_student(added_students[0])
        student.update_first_name("UpdatedFirst")
        self.student_management.update_student(student)
        self.assertEqual(self.student_management.get_student(added_students[0]).first_name, "UpdatedFirst")

        # Delete 1000 students
        for email in added_students:
            self.student_management.delete_student(email)

        self.assertGreater(len(self.student_management.students), 0)

    def test_search_students(self):
        """Test searching for students and measure execution time."""
        start_time = datetime.now()
        self.student_management.get_students("test_student")
        end_time = datetime.now()

        time_elapsed = (end_time - start_time).total_seconds() * 1000
        print(f"For 1000 records, search execution time: {time_elapsed} ms")

    def test_sort_students(self):
        """Test sorting students by marks and email, and measure execution time."""
        # Add some test students
        for i in range(10):
            student = Student(f"SortFirst{i}", f"SortLast{i}", f"sort{i}@email.com", marks=str(randint(50, 100)))
            self.student_management.add_new_student(student)

        # Sort by marks
        start_time = time.time()
        sorted_by_marks = sorted(self.student_management.students, key=lambda x: sum(map(int, x.marks_list())) if x.marks else 0)
        end_time = time.time()
        print(f"For 1000 records, sorting by marks took: {(end_time - start_time) * 1000} ms")

        # Sort by email
        start_time = time.time()
        sorted_by_email = sorted(self.student_management.students, key=lambda s: s.email_address)
        end_time = time.time()
        print(f"For 1000 records, sorting by email took: {(end_time - start_time) * 1000} ms")

    def test_add_delete_modify_course(self):
        """Test adding, modifying, and deleting courses."""
        course = Course("DATA101", 3, "Data Analytics", "Intro to DA")
        self.course_management.add_new_course(course)
        self.assertIn("DATA101", self.course_management.course_dict)

        # Modify course
        course.course_name = "Intro to DA"
        self.course_management.update_course(course)
        self.assertEqual(self.course_management.get_course("DATA101").course_name, "Intro to DA")

        # Delete course
        self.course_management.delete_course("DATA101")
        self.assertNotIn("DATA101", self.course_management.course_dict)

    def test_add_delete_modify_professor(self):
        """Test adding, modifying, and deleting professors."""
        professor = Professor("Dr. Harika", "harika@sjsu.edu", "Associate Professor")
        self.professor_management.add_new_professor(professor)
        self.assertIn("harika@sjsu.edu", self.professor_management.professor_dict)

        # Modify professor
        professor.update_rank("Professor")
        self.professor_management.update_professor(professor)
        self.assertEqual(self.professor_management.get_professor("harika@sjsu.edu").rank, "Professor")

        # Delete professor
        self.professor_management.delete_professor("harika@sjsu.edu")
        self.assertNotIn("harika@sjsu.edu", self.professor_management.professor_dict)

    def test_add_delete_modify_grade(self):
        """Test adding, modifying, and deleting grades."""
        grade = Grade("A", "Excellent", "90-100")
        self.grade_management.add_grade(grade)
        self.assertIn("A", self.grade_management.grade_dict)

        # Modify grade
        grade.marks_range = "85-100"
        self.grade_management.update_grade(grade)
        self.assertEqual(self.grade_management.grade_dict["A"].marks_range, "85-100")

        # Delete grade
        self.grade_management.delete_grade("A")
        self.assertNotIn("A", self.grade_management.grade_dict)

    def test_user_login(self):
        """Test user login functionality."""
        test_user = User("test_user", self.user_management.encrypt_password("password123"), "student")
        self.user_management.add_user(test_user)

        login_success = self.user_management.login("test_user", "password123", "student")
        self.assertTrue(login_success)

        wrong_password = self.user_management.login("test_user", "wrongpassword", "student")
        self.assertFalse(wrong_password)

        wrong_role = self.user_management.login("test_user", "password123", "professor")
        self.assertFalse(wrong_role)

        self.user_management.delete_user("test_user")

if __name__ == "__main__":
    unittest.main()
