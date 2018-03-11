#!/usr/bin/env python3
import pandas as pd
import pickle as pk
from pathlib import *
import csv
import sys
import operator

# there is a built-in feature called credits, so I will change all the "credits" to something else
# if press ctrl + C, the data won't be saved

season_map = {'1': 'spring', '2': 'summer', '3': 'fall', '4': 'winter'}
integer_to_season = {'spring': '1', 'summer': '2', 'fall': '3', 'winter': '4'}

class Course:
	def __init__(self, department, number, name, credit):
		self.department = department
		self.number = number
		self.name = name
		self.credit = credit

class Institution:
	def __init__(self, name):
		self.name = name
		self.students_list = list()
		self.instructors_list = list()
		self.courses_catalog = list()
		self.courses_schedule = dict()

	def list_students(self):
		return self.students_list

	def enroll_student(self, student):
		self.students_list.append(student)
		student.school = self
	
	def hire_instructor(self, instructor):
		self.instructors_list.append(instructor)

	def list_course_catalog(self):
		return self.courses_catalog

	def list_course_schedule(self, year, quarter):
		return self.courses_schedule[year][integer_to_season[quarter]]

	def add_course(self, course):
		self.courses_catalog.append(course)

	# How to add course to schedule without year and quarter?
	def add_course_offering(self, courseOffering):
		if courseOffering.year not in self.courses_schedule:
			self.courses_schedule[courseOffering.year] = dict()
		if courseOffering.quarter not in self.courses_schedule[courseOffering.year]:
			self.courses_schedule[courseOffering.year][integer_to_season[courseOffering.quarter]] = list()
		self.courses_schedule[courseOffering.year][integer_to_season[courseOffering.quarter]].append(courseOffering)

class Person:
	def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation, email):
		self.last_name = last_name
		self.first_name = first_name
		self.school = school
		self.date_of_birth = date_of_birth
		self.username = username
		self.affiliation = affiliation
		self.email = email

class Instructor(Person):
	def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation, email):
		super().__init__(last_name, first_name, school, date_of_birth, username, affiliation, email)
		self.courses_catalog = list()
		self.courses_schedule = dict()

	def list_courses(self, year=None, quarter=None):
		new_dict = dict()
		a = sorted(self.courses_schedule, key = operator.itemgetter(0),reverse = True)
		for key in a:
			new_dict[key] = self.courses_schedule[key]
		for key in new_dict:
			temp_dict = dict()
			b = new_dict[key]
			c = sorted(b, key = operator.itemgetter(0), reverse=True)
			for key2 in b:
				new_dict[key][key2] = self.courses_schedule[key][key2]

		self.courses_schedule = new_dict

		return self.courses_schedule
	
	# instructor needs a behavior to add course right?

class Student(Person):
	def __init__(self, last_name, first_name, school, date_of_birth, username, affiliation, email):
		super().__init__(last_name, first_name, school, date_of_birth, username, affiliation, email)
		self.courses_catalog = list()
		self.courses_schedule = dict()
		self.gpas = 0.0

	def list_courses(self):
		new_dict = dict()
		a = sorted(self.courses_schedule, key = operator.itemgetter(0),reverse = True)
		for key in a:
			new_dict[key] = self.courses_schedule[key]
		for key in new_dict:
			temp_dict = dict()
			b = new_dict[key]
			c = sorted(b, key = operator.itemgetter(0), reverse=True)
			for key2 in b:
				new_dict[key][key2] = self.courses_schedule[key][key2]

		self.courses_schedule = new_dict

		return self.courses_schedule

	def list_credits(self):
		res = 0
		for cr in self.courses_catalog:
			res += int(cr.credit)
		return res

	def gpa(self):
		return self.gpas

class CourseOffering:
	def __init__(self, course, section_number, instructor, year, quarter):
		self.course = course
		self.section_number = section_number
		self.instructor = instructor
		self.year = year
		self.quarter = str.lower(quarter)
		self.student_list = list()
		self.student_grade = dict()
		self.username_grade = dict()

	def register_students(self, student):
		self.student_list.append(student)
		student.courses_catalog.append(self.course)
		if self.year not in student.courses_schedule:
			student.courses_schedule[self.year] = dict()
		if integer_to_season[self.quarter] not in student.courses_schedule[self.year]:
			student.courses_schedule[self.year][integer_to_season[self.quarter]] = list()
		student.courses_schedule[self.year][integer_to_season[self.quarter]].append(self.course)


	def get_students(self):
		if len(self.student_list) == 0:
			print ('No student has registered yet!')
		return self.student_list

	def submit_grade(self, grade, student=None, username=None):
		self.username_grade[student] = grade
		score = 0
		if grade == 'A+' or grade == 'A':
			score = 4.0
		elif grade == 'A-':
			score = 3.7
		elif grade == 'B+':
			score = 3.3
		elif grade == 'B':
			score = 3.0
		elif grade == 'B-':
			score = 2.7
		elif grade == 'C+':
			score = 2.3
		elif grade == 'C':
			score = 2.0
		elif grade == 'C-':
			score = 1.7
		elif grade == 'D+':
			score = 1.3
		elif grade == 'D':
			score = 1.0
		elif grade == 'F':
			score = 0

		student.gpas = student.gpas + int(self.course.credit)*int(score)

	def get_grade(self, student=None, username=None):
		return self.student_grade[student]

def print_selection():
	print("Please select an option from the following:")
	print("1   Create a course")
	print("2   Schedule a course offering")
	print("3   List course catalog")
	print("4   List course schedule")
	print("5   Hire an instructor")
	print("6   Assign an instructor to a course")
	print("7   Enroll a student")
	print("8   Register a student for a course")
	print("9   List enrolled students")
	print("10  List students registered for a course")
	print("11  Submit student grade")
	print("12  Get Student records")
	print("13  Exit")
