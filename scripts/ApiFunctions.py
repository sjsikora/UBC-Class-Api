import requests
import re
import html
from scripts.UtilFunctions import *

def formatInputJson(inputJson: dict):
    deafultJson = {
        'campus': 'UBCO',
        'subjectCode': '',
        'courseCode': '',
        'sectionCode': '',
        'fullDetails': False
    }

    deafultJson.update(inputJson)

    return inputJson

def fromCampusPullSubjects(campus='UBCO'):

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

def fromSubjectPullCourses(subjectCode, campus='UBCO', fulldetails = False):

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

def fromSectionPullDetails(subjectCode, courseCode, sectionCode, campus='UBCO'):

    if campus == 'UBCO':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course={courseCode}&section={sectionCode}&campuscd=UBCO&dept={subjectCode}&pname=subjarea'
    elif campus == 'UBCV':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course={courseCode}&section={sectionCode}&campuscd=UBC&dept={subjectCode}&pname=subjarea'
    else:
        print("Invaild Campus in function fromSectionPullDetails.") 
        return {
            'error': "Invaild Campus in function fromSectionPullDetails."
        }
    session = requests.session()
    sectionPageHtml = html.unescape(session.get(url).text)

    sectionPageHtmlSplit = findTextBetweenText(sectionPageHtml, '</style>', '</table>\n\n\n')

    if sectionPageHtmlSplit == '':
        print(f"Invaild Course Combo: {subjectCode} {courseCode} {sectionCode} on campus {campus}")
        return {
            'error': f"Invaild Course Combo: {subjectCode} {courseCode} {sectionCode} on campus {campus}"
        }

    classSyllabusUrl = findTextBetweenText(sectionPageHtmlSplit, '<a href=', ' target="_blank" class="btn btn-primary btn-small pull-right">Outline/Syllabus</a>')
    classBuilding = findInstancesOfTextBetweenText(sectionPageHtmlSplit, '<td>', '</td>')[8]

    if classBuilding:
        classRoom = findTextBetweenText(sectionPageHtmlSplit, f'{classBuilding}</td><td>', '</td>')

    if "<td>Instructor:  </td><td>TBA</td>" in sectionPageHtmlSplit:
        classInstructor = 'TBA'
    elif "<td>Instructor:  </td><td><a href=" in sectionPageHtmlSplit:
        instructorUrl = findTextBetweenText(sectionPageHtmlSplit, '<td>Instructor:  </td><td><a href="', '">')
        classInstructor = findInstancesOfTextBetweenText(sectionPageHtmlSplit, f'<a href="{instructorUrl}">', '</a>')

    sectionPageHtmlStrongTag = findInstancesOfTextBetweenText(sectionPageHtmlSplit, "<strong>", "</strong>")
    classSeatsTotalRemaining = sectionPageHtmlStrongTag[1]
    classSeatsRegistered = sectionPageHtmlStrongTag[2]
    classSeatsGeneralRemaining = sectionPageHtmlStrongTag[3]
    classSeatsRestrictedRemaining = sectionPageHtmlStrongTag[4]


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


def fromCoursePullSections(subjectCode, courseCode, campus='UBCO', fulldetails = False):
    
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


            if classSection == 'COSC 301 101':
                print("")
                pass

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


def fromSubjectPullSections(subjectCode):

    coursesJson = fromSubjectPullCourses(subjectCode, fulldetails=True)

    i = 0
    while(i < len(coursesJson)):

        courseCode = coursesJson[i]["code"].split(" ")[1]
        sectionsJson = fromCoursePullSections(subjectCode, courseCode)
        coursesJson[i]['sections'] = sectionsJson

        i+=1

    return coursesJson
