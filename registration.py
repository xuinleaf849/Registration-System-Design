#!/usr/bin/env python3
from registrar import *
import pandas as pd
import pickle as pk
from pathlib import *
import csv
import sys
import operator


print("Welcome to the Registration System")
school_name = input("Please enter the name of your institution: ")

ins = Institution(school_name)

if Path(school_name+".pkl").exists():
    with open(school_name+".pkl", 'rb') as ipt:
        ins = pk.load(ipt)

while True:
# get user input at main menu
    print_selection()
    selection_main_menu = input("Please enter your choice: ")

    # Create a course
    if str(selection_main_menu) == '1':
        department = input("Please input course department: ")
        number = input("Please input course number: ")
        name = input("Plase input course name: ")
        credit = input("Please input course credit: ")
        current_course = Course(department, number, name, credit)
        ins.add_course(current_course)
        continue

    # Schedule a course offering
    elif str(selection_main_menu) == '2':
        department = input("Please input course department: ")
        number = input("Please input course number: ")
        course = None
        findCourse = False
        for cr in ins.courses_catalog:
            if cr.department == department and cr.number == number:
                course = cr
                year = input("Please input course year: ")
                quarter = input("Please input course quarter: ")
                quarter = str.lower(quarter)
                section_number = input("Please input course section number: ")
                courseOffering = CourseOffering(cr, section_number, None, year, quarter)
                ins.add_course_offering(courseOffering)
                break

    # List course catalog
    elif str(selection_main_menu) == '3':
        for cr in ins.courses_catalog:
            res = cr.department+cr.number+" "+cr.name+" "+cr.credit
            print(res)

    # List course schedule
    elif str(selection_main_menu) == '4':
        year = input("Please input course year: ")
        quarter = input("Please input course quarter: ")
        quarter = str.lower(quarter)

        if year not in ins.courses_schedule or integer_to_season[quarter] not in ins.courses_schedule[year]:
            print("Year or quarter not found! Please double check your input!")
            continue

        for cr in ins.courses_schedule[year][integer_to_season[quarter]]:
            res = cr.course.department + \
                    cr.course.number+" " + \
                    cr.course.name+" "+cr.course.credit
            print(res)

    # Hire an instructor
    elif str(selection_main_menu) == '5':
        last_name = input("Please input the last name: ")
        first_name = input("Please input the first name: ")
        school = ins.name
        dob = input("Please input date of birth in mm-dd-year: ")
        user_name = input("Please input a user_name: ")
        affiliation = input("Please input the affiliation(student,faculty,staff): ")
        email = input("Please input the email address: ")
        instructor = Instructor(last_name, first_name, school, dob, user_name, affiliation, email)
        ins.hire_instructor(instructor)

    # Assign an instructor to a course
    elif str(selection_main_menu) == '6':
        instructor_username = input("Please input username of instructor: ")
        department = input("Please input course department: ")
        number = input("Please input course number: ")
        section_number = input("Please input section number: ")
        year = input("Please input course year: ")
        quarter = input("Please input course quarter: ")
        quarter = str.lower(quarter)

        course = None
        findCourse = False
        for cr in ins.courses_catalog:
            if cr.department == department and cr.number == number:
                course = cr
                findCourse = True
                break

        if not findCourse:
            print("No such course in record!")
            continue

        instructor = None
        findInstructor = False	
        for i in ins.instructors_list:
            if i.username == instructor_username:
                i.courses_catalog.append(course)
                if year not in i.courses_schedule:
                    i.courses_schedule[year] = dict()
                if integer_to_season[quarter] not in i.courses_schedule[year]:
                    i.courses_schedule[year][integer_to_season[quarter]] = list()
                i.courses_schedule[year][integer_to_season[quarter]].append(course)
                findInstructor = True
                for co in ins.courses_schedule[year][integer_to_season[quarter]]:
                    if co.course.number == number and co.course.department == department and co.section_number == section_number:
                        co.instructor = i
                        break
                break

    # Enroll a student
    elif str(selection_main_menu) == '7':
        last_name = input("Please input the last name: ")
        first_name = input("Please input the first name: ")
        school = ins.name
        dob = input("Please input date of birth in mm-dd-year: ")
        user_name = input("Please input a user_name: ")
        affiliation = input("Please input the affiliation(student,faculty,staff): ")
        email = input("Please input the email address: ")
        student = Student(last_name, first_name, school, dob, user_name, affiliation, email)
        ins.enroll_student(student)

    # Register a student for a course
    elif str(selection_main_menu) == '8':
        student_username = input("Please input username of student: ")
        department = input("Please input course department: ")
        number = input("Please input course number: ")
        section_number = input("Please input section number: ")
        year = input("Please input course year: ")
        quarter = input("Please input course quarter: ")
        quarter = str.lower(quarter)

        findCourse = False
        findStudent = False

        for co in ins.courses_schedule[year][integer_to_season[quarter]]:
            if co.section_number == section_number and co.course.department == department and co.course.number == number:
                findCourse = True
                for s in ins.students_list:
                    if s.username == student_username:
                        findStudent = True
                        co.register_students(s)
                        break
                break
        if not findCourse or not findStudent:
            print("Student or course is not found!")

    # List enrolled students
    elif str(selection_main_menu) == '9':
        for s in ins.students_list:
            print("Student name:"+s.last_name+" "+s.first_name)
            print("Student school: "+s.school.name)
            print("Student birthday: "+s.date_of_birth)
            print("Student username: "+s.username)
            print("Student email: "+s.email)

    # List students registered for a course
    elif str(selection_main_menu) == '10':
        department = input("Please input department: ")
        number = input("Please input course number: ")
        section_number = input("Please input section number: ")
        year = input("Please input year: ")
        quarter = input("Please input quarter: ")
        quarter = str.lower(quarter)

        for co in ins.courses_schedule[year][integer_to_season[quarter]]:
            if co.section_number == section_number:
                for s in co.student_list:
                    print("Student name:"+s.last_name+" "+s.first_name)
                    print("Student school: "+s.school)
                    print("Student birthday: "+s.date_of_birth)
                    print("Student username: "+s.username)
                    print("Student email: "+s.email)

    # Submit student grade
    elif str(selection_main_menu) == '11':
        student_username = input("Please input student username: ")
        department = input("Please input department: ")
        number = input("Please input course number: ")
        section_number = input("Please input section number: ")
        year = input("Please input year: ")
        quarter = input("Please input quarter: ")
        quarter = str.lower(quarter)
        grade = input("Pleae give student a grade: ")

        for co in ins.courses_schedule[year][integer_to_season[quarter]]:
            if co.course.department == department and co.course.number == number and co.section_number == section_number:
                for s in co.student_list:
                    if s.username == student_username:
                        co.submit_grade(grade, s)
                        break
                break
    
    # Get Student records
    elif str(selection_main_menu) == '12':
        user_name = input("Please input student username: ")
        for student in ins.students_list:
            if student.username == user_name:
                print("Student's courses: ")
                for course in student.courses_catalog:
                    print(course.name)
                print("\n")
                print("Student's credits: ")
                print(str(student.list_credits()))
                print("Student's gpa: ")
                print(student.gpa())
                break

    # exit
    elif str(selection_main_menu) == '13':
        with open(school_name+".pkl", 'wb') as output:
            pk.dump(ins, output, pk.HIGHEST_PROTOCOL)
        del ins
        sys.exit()
