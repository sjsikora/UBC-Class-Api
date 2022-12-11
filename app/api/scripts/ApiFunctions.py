import requests
import re
import html
from app.api.scripts.UtilFunctions import *

def fromCampusPullSubjects(campus):

    if campus == "UBCO":
        url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-all-departments&pname=subjarea&campuscd=UBCO'
    elif campus == 'UBCV':
        url = 'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-all-departments&pname=subjarea&campuscd=UBC'
    else:
        print("Invaild Campus in function fromCampusPullSubjects. ") 
        return {
            'error': "Invaild Campus in function fromCampusPullSubjects."
        }

    session = requests.session()
    urlHtml = html.unescape(session.get(url).text)
    subjectHtmlList = findInstancesOfTextBetweenText(urlHtml, 'class=section', '</tr>')
    session.close()

    subjectJsonList = []

    for subjectHtml in subjectHtmlList:

        subjectCode: str = ''
        subjectProperName: str = ''
        subjectFaculty: str = ''
        subjectUrl: str = ''
        isOffered: bool = False

        subjectCode = findTextBetweenText(subjectHtml, '<b>', '</b>')

        isOffered = subjectCode == ''

        if isOffered:
            subjectUrl = findTextBetweenText(subjectHtml, '<a href=', '>').strip()
            subjectCode = findTextBetweenText(subjectHtml, f'{subjectUrl}>', '</a>').strip()
            subjectUrl = "https://courses.students.ubc.ca" + subjectUrl
        else:
            subjectCode = subjectCode[:-2]

        subjectProperName, subjectFaculty = findInstancesOfTextBetweenText(subjectHtml, '<td style="white-space: nowrap">', '</td>')
        subjectProperName = subjectProperName.strip()
        subjectFaculty = subjectFaculty.strip()

        subjectJson = {
            "code": subjectCode,
            "properName": subjectProperName,
            "faculty": subjectFaculty,
            "offered": isOffered
        }

        subjectJsonList += [subjectJson]

    return subjectJsonList

def fromSubjectPullCourses(subjectCode, campus, fulldetails = False):

    session = requests.session()

    if campus == "UBCO":
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&campuscd=UBCO&dept={subjectCode}&pname=subjarea'
    elif campus == 'UBCV':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&campuscd=UBC&dept={subjectCode}&pname=subjarea'
    else:
        print("Invaild Campus in function fromSubjectPullCourses.") 
        return {
            'error': "Invaild Campus in function fromSubjectPullCourses."
        }
    
    urlHtml = html.unescape(session.get(url).text)
    courseHtmlList = findInstancesOfTextBetweenText(urlHtml, 'class=section', '</tr>')

    if courseHtmlList == '':
        return {
            'error': f'Can not find course {subjectCode} in campus {campus}'
        }

    courseJsonList = []

    for courseHtml in courseHtmlList:

        courseCode: str = ''
        courseCredits: float = 0
        coursePreReqs: str = ''
        courseDescription: str = ''
        courseTitle: str = ''


        courseUrl = findTextBetweenText(courseHtml, '<a href=', '>').strip()
        courseCode = findTextBetweenText(courseHtml, f'{courseUrl}>', '</a>').strip()
        courseTitle = findTextBetweenText(courseHtml, '</td><td>', '</td></a>').strip()

        if not fulldetails:

            courseJson = {
                "code": courseCode,
                "title": courseTitle
            }

        else:
            classPageUrl = "https://courses.students.ubc.ca" + courseUrl
            classPageHtml = html.unescape(session.get(classPageUrl).text)
            session.close()

            coursePTags = findInstancesOfTextBetweenText(classPageHtml, '<p>', '</p>')
            courseDescription = coursePTags[0]
            courseCredits = float(coursePTags[1][9:])
            coursePreReqs = findTextBetweenText(classPageHtml, '<p>Pre-reqs:', '</p>')

            if coursePreReqs != '':
                coursePreReqs = re.sub('<[^>]+>', '', coursePreReqs)[5:]


            courseJson = {
                "code": courseCode,
                "credits": courseCredits,
                "preReqs": coursePreReqs,
                "description": courseDescription,
                "title": courseTitle
            }

        courseJsonList += [courseJson]

    return courseJsonList

def fromSectionPullDetails(subjectCode, courseCode, sectionCode, campus):

    if campus == 'UBCO':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course={courseCode}&section={sectionCode}&campuscd=UBCO&dept={subjectCode}&pname=subjarea'
    elif campus == 'UBCV':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course={courseCode}&section={sectionCode}&campuscd=UBC&dept={subjectCode}&pname=subjarea'
    else:
        print("Invaild Campus in function fromSectionPullDetails.") 
        return {
            'error': "Invaild Campus in function fromSectionPullDetails."
        }


    classSyllabusUrl: str = ''
    classInstructor: list = ''
    classBuilding: str = ''
    classRoom: int = ''
    classSeatsTotalRemaining: int = 0
    classSeatsRegistered: int = 0
    classSeatsGeneralRemaining: int = 0
    classSeatsRestrictedRemaining: int = 0

    session = requests.session()
    sectionPageHtml = html.unescape(session.get(url).text)

    if campus == 'UBCV':
        sectionPageHtmlSplit = findTextBetweenText(sectionPageHtml, 'Save To Worklist</a>\n\n\n\n\n\n\n', '<b>Book Summary</b>')
    else:
        sectionPageHtmlSplit = findTextBetweenText(sectionPageHtml, '</style>', '</table>\n')

    if sectionPageHtmlSplit == '':
        print(f"Invaild Course Combo: {subjectCode} {courseCode} {sectionCode} on campus {campus}")
        return {
            'error': f"Invaild Course Combo: {subjectCode} {courseCode} {sectionCode} on campus {campus}"
        }

    classSyllabusUrl = findTextBetweenText(sectionPageHtmlSplit, '<a href=', ' target="_blank" class="btn btn-primary btn-small pull-right">Outline/Syllabus</a>')

    classSections = findTextBetweenText(sectionPageHtmlSplit, '<th>Room</th></tr></thead>', '</table>')
    classSections = findInstancesOfTextBetweenText(classSections, '<td>', '</td>')
    

















    classBuilding = findInstancesOfTextBetweenText(sectionPageHtmlSplit, '<td>', '</td>')

    ########  FIX YEAR LONG COURSE!!!!!!!!!!
    if len(classBuilding) >= 9:
        classBuilding = classBuilding[8]


    if classBuilding:
        classRoom = findTextBetweenText(sectionPageHtmlSplit, f'{classBuilding}</td><td>', '</td>')

        if campus == 'UBCV':
            classRoom = findTextBetweenText(classRoom, 'target="_blank">', '</a>')

    if "<td>Instructor:  </td><td>TBA</td>" in sectionPageHtmlSplit:
        classInstructor = 'TBA'
    elif "<td>Instructor:  </td><td><a href=" in sectionPageHtmlSplit:
        instructorUrl = findTextBetweenText(sectionPageHtmlSplit, '<td>Instructor:  </td><td><a href="', '">')
        classInstructor = findInstancesOfTextBetweenText(sectionPageHtmlSplit, f'<a href="{instructorUrl}">', '</a>')

    if ('The remaining seats in this section are only available through a Standard Timetable (STT)' not in sectionPageHtmlSplit) and ('this section is blocked from registration.' not in sectionPageHtmlSplit):

        sectionPageHtmlStrongTag = findInstancesOfTextBetweenText(sectionPageHtmlSplit, "<strong>", "</strong>")
        i = sectionPageHtmlStrongTag.index("Seat Summary")

        classSeatsTotalRemaining = sectionPageHtmlStrongTag[i+1]
        classSeatsRegistered = sectionPageHtmlStrongTag[i+2]
        classSeatsGeneralRemaining = sectionPageHtmlStrongTag[i+3]
        classSeatsRestrictedRemaining = sectionPageHtmlStrongTag[i+4]



    classJson = {
        "syllabusUrl": classSyllabusUrl,
        "instructor": classInstructor,
        "building": classBuilding,
        "room": classRoom,
        "seatsTotalRemaining": classSeatsTotalRemaining,
        "seatsRegistered": classSeatsRegistered,
        "seatsGeneralRemaining": classSeatsGeneralRemaining,
        "seatsRestrictedRemaining": classSeatsRestrictedRemaining
    }

    return classJson


def fromCoursePullSections(subjectCode, courseCode, campus, fulldetails = False):
    
    if campus == "UBCO":
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course={courseCode}&campuscd=UBCO&dept={subjectCode}&pname=subjarea'
    elif campus == 'UBCV':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course={courseCode}&campuscd=UBC&dept={subjectCode}&pname=subjarea'
    else:
        print("Invaild Campus in function fromCoursePullSections.") 
        return {
            'error': "Invaild Campus in function fromCoursePullSections."
        }

    session = requests.session()
    classPageHtml = html.unescape(session.get(url).text)
    classHtmlList = findInstancesOfTextBetweenText(classPageHtml, 'class=section', '</tr>')
    session.close()

    if len(classHtmlList) == 0:
        print(f"ERROR: Can not find {subjectCode} {courseCode} at campus {campus}")
        return {
            "error": f"ERROR: Can not find {subjectCode} {courseCode} at campus {campus}"
        }


    classJsonList = []

    for classHtml in classHtmlList:

        classStatus: str = '' 
        classSection: str = ''
        classActivity: str = ''
        classTerm: int = 0
        classDelivery: str = ''
        classInterval: str = ''
        classDays: list = []
        classStart: str = ''
        classEnd: str = ''
        classComments: str = ''
        classInPersonAttendance: bool = False
        classJsonToAdd = {}

        classUrl = findTextBetweenText(classHtml, '<a href=', 'onmouseover=').strip()

        if classUrl != '':
            classSection = findTextBetweenText(classHtml, ',2000)">', '</a>').strip()
        else:
            classUrl = findTextBetweenText(classHtml, '<a href=', '>').strip()
            classSection = findTextBetweenText(classHtml, f'<a href={classUrl} >', '</a>').strip()

        classTdtags = findInstancesOfTextBetweenText(classHtml, '<td>', '</td>') 
        
        classStatus = classTdtags[0].strip()
        classActivity = classTdtags[2].strip()
        classTerm = classTdtags[3].strip()
        if len(classTerm) > 1:
            classTerm = 3
        else:
            classTerm = int(classTerm)

        classDelivery = classTdtags[4].strip()

        if classStatus != "Cancelled":

            classInterval = classTdtags[5].strip()
            classDays = classTdtags[6].strip().split(" ")
            classStart = classTdtags[7].strip()
            classEnd = classTdtags[8].strip()

            classComments = findTextBetweenText(classHtml, '<div class=\'accordion-inner\'>', '</p></div>')
            if classComments: 
                classComments = re.sub('<[^>]+>', ' ', classComments)

            classInPersonAttendance = classTdtags[9].strip() == "Yes"

            if fulldetails:
                classCodeDetails = classSection.split(' ')
                classJsonToAdd = fromSectionPullDetails(classCodeDetails[0], classCodeDetails[1], classCodeDetails[2], campus)

        classJson = {
            "section": classSection,
            "status": classStatus,
            "activity": classActivity,
            "term": classTerm,
            "delivery": classDelivery,
            "interval": classInterval,
            "days": classDays,
            "start": classStart,
            "end": classEnd,
            "comments": classComments,
            "inPersonAttendance": classInPersonAttendance
        }

        if classJsonToAdd:
            classJson.update(classJsonToAdd)

        classJsonList += [classJson]
    

    return classJsonList


def fromSubjectPullSections(subjectCode, campus, fulldetails= False):

    coursesJson = fromSubjectPullCourses(subjectCode, fulldetails=True, campus = campus)

    i = 0
    while(i < len(coursesJson)):

        courseCode = coursesJson[i]["code"].split(" ")[1]
        sectionsJson = fromCoursePullSections(subjectCode, courseCode, fulldetails=fulldetails, campus = campus)
        coursesJson[i]['sections'] = sectionsJson

        i+=1

    return coursesJson


