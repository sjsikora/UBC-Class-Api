import requests
import json

url = 'http://127.0.0.1:5000'

campusSubject = requests.get(f'{url}/campusSubjects/campus=UBCO').text
campusSubject = requests.get(f'{url}/campusSubjects/campus=UBCV').text

campusSubject = requests.get(f'{url}/campusSubjects/campus=UBC').text


couseSections = requests.get(f'{url}/courseSections/campus=UBCO/subject=PHYS/course=112').text
couseSections = requests.get(f'{url}/courseSections/campus=UBCV/subject=INDG/course=295K').text

couseSections = requests.get(f'{url}/courseSections/campus=UBCO/subject=PHYS/course=001').text
couseSections = requests.get(f'{url}/courseSections/campus=UBC/subject=PHYS/course=001').text


courseSectionsFull = requests.get(f'{url}/courseSections/campus=UBCO/subject=PHYS/course=112/fullDetails').text
courseSectionsFull = requests.get(f'{url}/courseSections/campus=UBCV/subject=MATH/course=100/fullDetails').text

courseSectionsFull = requests.get(f'{url}/courseSections/campus=UBCV/subject=HDND/course=100/fullDetails').text


subjectCourse = requests.get(f'{url}/subjectCourses/campus=UBCO/subject=DATA').text ####
subjectCourse = requests.get(f'{url}/subjectCourses/campus=UBCV/subject=MATH').text ###

subjectCourse = requests.get(f'{url}/subjectCourses/campus=UBCO/subject=AGRO').text


subjectCourseFull = requests.get(f'{url}/subjectCourses/campus=UBCO/subject=DATA/fullDetails').text
subjectCourseFull = requests.get(f'{url}/subjectCourses/campus=UBCV/subject=MATH/fullDetails').text

subjectCourseFull = requests.get(f'{url}/subjectCourses/campus=UBCO/subject=AGRO/fullDetails').text


subjectSections = requests.get(f'{url}/subjectSections/campus=UBCO/subject=PHYS').text
subjectSections = requests.get(f'{url}/subjectSections/campus=UBCV/subject=MATH').text


subjectSections = requests.get(f'{url}/subjectSections/campus=UBCO/subject=PHYS/fullDetails').text
subjectSections = requests.get(f'{url}/subjectSections/campus=UBCV/subject=MATH/fullDetails').text