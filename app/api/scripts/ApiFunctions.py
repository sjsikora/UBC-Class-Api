import requests
import urllib3
import re
from app.api.scripts.UtilFunctions import *
from bs4 import BeautifulSoup

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

    http = urllib3.PoolManager()
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    subjectsHtmlList = soup.find_all('tr')
    subjectsHtmlList.pop(0)
    

    subjectJsonList = []

    for subjectHtml in subjectsHtmlList:

        subjectCode: str = ''
        subjectProperName: str = ''
        subjectFaculty: str = ''
        isOffered: bool = False

        tdTagsList = subjectHtml.find_all('td')

        if len(tdTagsList) < 3:
            return subjectJsonList

        subjectCode = tdTagsList[0].string
        isOffered = '*' not in subjectCode

        if not isOffered:
            subjectCode = subjectCode[:-2]

        subjectProperName = tdTagsList[1].string.strip()
        subjectFaculty = tdTagsList[2].string.strip()

        subjectJson = {
            "code": subjectCode,
            "properName": subjectProperName,
            "faculty": subjectFaculty,
            "offered": isOffered
        }

        subjectJsonList += [subjectJson]

    return subjectJsonList

def fromSubjectPullCourses(subjectCode, campus, fulldetails = False):

    if campus == "UBCO":
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&campuscd=UBCO&dept={subjectCode}&pname=subjarea'
    elif campus == 'UBCV':
        url = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-department&campuscd=UBC&dept={subjectCode}&pname=subjarea'
    else:
        print("Invaild Campus in function fromSubjectPullCourses.") 
        return {
            'error': "Invaild Campus in function fromSubjectPullCourses."
        }

    http = urllib3.PoolManager()
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    courseHtmlList = soup.find_all('tr')
    courseHtmlList.pop(0)

    ## Recheck this -------------------------------------
    if len(courseHtmlList) == 0:
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

        tdTags = courseHtml.find_all('td')

        if len(courseHtml) <= 1:
            return courseJsonList

        courseCode = tdTags[0].string
        courseTitle = tdTags[1].string

        if not fulldetails:
            courseJson = {
                "code": courseCode,
                "title": courseTitle
            }
        else:

            courseCodeList = courseCode.split(' ')

            if campus == 'UBCO':
                courseUrl = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course={courseCodeList[1]}&campuscd=UBCO&dept={courseCodeList[0]}&pname=subjarea'
            elif campus == 'UBCV':
                courseUrl = f'https://courses.students.ubc.ca/cs/courseschedule?tname=subj-course&course={courseCodeList[1]}&campuscd=UBO&dept={courseCodeList[0]}&pname=subjarea'

            coursePage = http.request('GET', courseUrl)
            courseSoup = BeautifulSoup(coursePage.data, 'html.parser')

            coursePTags = courseSoup.find_all('p')

            courseDescription = coursePTags[0].string
            courseCredits = float(coursePTags[1].string[9:])
            coursePreReqs = str(coursePTags[2])
            coursePreReqs = re.sub('<[^>]+>', '', coursePreReqs)[14:]

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

    http = urllib3.PoolManager()
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    #Per Section    
    sectionTerm: int = 0
    sectionDays: str = ''
    sectionStart: str = ''
    sectionEnd: str = ''
    sectionBuilding: str = ''
    sectionRoom: str  = ''

    classSyllabusUrl: str = ''
    classInstructor: list = []
    classSeatsTotalRemaining: int = 0
    classSeatsRegistered: int = 0
    classSeatsGeneralRemaining: int = 0
    classSeatsRestrictedRemaining: int = 0


    classHtmlTable = soup.find_all('table')

    if len(classHtmlTable) == 2:
        print(f'ERROR: {courseCode} {sectionCode} {subjectCode} {campus} fromSectionPullDetails')
        return {
            'error': f'Cant find {courseCode} {sectionCode} {subjectCode} {campus}'
        }
    

    sectionInfo = classHtmlTable[1].find_all('td')

    if len(sectionInfo) == 6:
        sections = [sectionInfo]
    elif len(sectionInfo) == 12:
        sections = [sectionInfo[6:], sectionInfo[:6]]
    else:
        sections = []

    sectionJsonList = []
    instructorHtmlIndex = 1

    for section in sections:

        sectionTerm = section[0].string

        if sectionTerm:
            if sectionTerm.isdigit():
                sectionTerm = int(sectionTerm)
            else:
                sectionTerm = 0

            instructorHtmlIndex = 2

            sectionDays = str(section[1].string)
            sectionDays = sectionDays.split(' ')
            sectionDays.pop(0)

    
            sectionStart = section[2].string
            sectionEnd = section[3].string
            sectionBuilding = section[4].string

            sectionRoom = section[5]
            if sectionRoom.find('a'):
                sectionRoom = sectionRoom.find('a').string
            elif sectionRoom.string:
                sectionRoom = sectionRoom.string
            else:
                sectionRoom = ''


            sectionJson = {
                "term": sectionTerm,
                "days": sectionDays,
                "start": str(sectionStart),
                "end": str(sectionEnd),
                "building": str(sectionBuilding),
                "room": str(sectionRoom)
            }
            

            sectionJsonList += [sectionJson]

    instructorsHtml = classHtmlTable[instructorHtmlIndex].find_all('a')

    classInstructor = []

    if len(instructorsHtml) == 0:
        if ("TBA" in classHtmlTable[2].text):
            classInstructor = ['TBA']
    else:
        for instructorHtml in instructorsHtml:
            classInstructor += [instructorHtml.string]
    
    for ATag in soup.find_all('a'):
        if ATag.string == 'Outline/Syllabus':
            classSyllabusUrl = ATag.get('href')

    strongTags = soup.find_all('strong')

    strongTagString = []
    blockedSeats = False
    for strongTag in strongTags:
        strongTag = strongTag.string
        strongTagString += [strongTag]

        if ('Standard Timetable' in strongTag) or ('this section is blocked from registration.' in strongTag) or ('cancelled' in strongTag) or ("temp. unavailable" in strongTag):
            blockedSeats = True

    if not blockedSeats:
        i = strongTagString.index('Seat Summary')
        classSeatsTotalRemaining = strongTagString[i+1]
        classSeatsRegistered = strongTagString[i+2]
        classSeatsGeneralRemaining = strongTagString[i+3]
        classSeatsRestrictedRemaining = strongTagString[i+4]

    classJson = {
        "syllabus": str(classSyllabusUrl),
        "instructor": classInstructor,
        "classSeatsTotalRemaining": classSeatsTotalRemaining,
        "classSeatsRegistered": classSeatsRegistered,
        "classSeatsGeneralRemaining": classSeatsGeneralRemaining,
        "classSeatsRestrictedRemaining": classSeatsRestrictedRemaining,
    }

    if len(sectionJsonList) == 1:
        classJson.update(sectionJsonList[0])
    elif len(sectionJsonList) > 1:
        classJson['sectionTerms'] = sectionJsonList

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

    http = urllib3.PoolManager()
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    mainHtml = soup.find_all('table')

    if len(mainHtml) == 2:
        print(f"ERROR: Can not find {subjectCode} {courseCode} at campus {campus}")
        return {
            "error": f"ERROR: Can not find {subjectCode} {courseCode} at campus {campus}"
        }

    mainHtml = mainHtml[1]

    classHtmlList = mainHtml.find_all('tr')
    classHtmlList.pop(0)


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

        classInfo = classHtml.find_all('td')

        classStatus = classInfo[0].string
        classSection = classInfo[1].find('a')

        classDays = str(classInfo[6].string)
        classDays = classDays.split(' ')
        classDays.pop(0)

        classStart = str(classInfo[7].string)
        classEnd = str(classInfo[8].string)
        classTerm = classInfo[3].string

        classActivity = classInfo[2].string
        classDelivery = classInfo[4].string.strip()
        classInterval = classInfo[5].string

        if classInterval:
            classInterval = classComments.get_text()
        else:
            classInterval = ''

        classComments = classInfo[9]
        classInPersonAttendance = str(classInfo[10].string).strip() == 'Yes'

        if classComments:
            classComments = classComments.get_text()
            classComments = classComments[20:]
        else:
            classComments = ''

        if len(classTerm) == 3:
            classTerm = 3
        elif classTerm == 'X':
            pass
        elif classTerm == 'C':
            pass
        elif classTerm == 'A':
            pass
        else:
            classTerm = int(classTerm)

        #If not classSection, then we have either a year long course, or a course with different days at the same time
        if classSection:

            classSection = classSection.string

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

            classJsonToAdd = {}
            if fulldetails:
                classCodeDetails = classSection.split(' ')
                classJsonToAdd = fromSectionPullDetails(classCodeDetails[0], classCodeDetails[1], classCodeDetails[2], campus)
                classJson.update(classJsonToAdd)

            classJsonList += [classJson]
        else:
            if not fulldetails:
                if classJsonList[len(classJsonList) - 1]['term'] == classTerm and (classTerm != 3):
                    timingList = []

                    if 'days' in classJsonList[len(classJsonList) - 1].keys():
                        days = classJsonList[len(classJsonList) - 1]['days']
                        start = classJsonList[len(classJsonList) - 1]['start']
                        end = classJsonList[len(classJsonList) - 1]['end']

                        del classJsonList[len(classJsonList) - 1]['days']
                        del classJsonList[len(classJsonList) - 1]['start']
                        del classJsonList[len(classJsonList) - 1]['end']

                        for day in days:
                            timingJson = {
                                day: {
                                    'start': start,
                                    'end': end
                                }
                            }
                            timingList += [timingJson]
                    else:
                        timingList += [classJsonList[len(classJsonList) - 1]['timing']]
                    
                    for day in classDays:
                        timingJson = {
                            day: {
                                'start': classStart,
                                'end': classEnd
                            }
                        }

                        timingList += [timingJson]
                    
                    classJsonList[len(classJsonList) - 1]['timing'] = timingList
                #Same year courses
                elif ('days' in classJsonList[len(classJsonList) - 1].keys()):
                    if (classJsonList[len(classJsonList) - 1]['days'] == classDays) and (classJsonList[len(classJsonList) - 1]['start'] == classStart) and ((classJsonList[len(classJsonList) - 1]['end'] == classEnd)):
                        pass
                else:
                    print("Class is offered diffferent days and/or times on different terms.")
                    timingList = []

                    term = classJsonList[len(classJsonList) - 1]['term']
                    days = classJsonList[len(classJsonList) - 1]['days']
                    start = classJsonList[len(classJsonList) - 1]['start']
                    end = classJsonList[len(classJsonList) - 1]['end']

                    classJsonList[len(classJsonList) - 1]['term'] = 3
                    del classJsonList[len(classJsonList) - 1]['days']
                    del classJsonList[len(classJsonList) - 1]['start']
                    del classJsonList[len(classJsonList) - 1]['end']

                    for day in days:
                        JsonToPush = {}

                        timingJson = {
                            day: {
                                'start': start,
                                'end': end
                            }
                        }

                        timingList += [JsonToPush]

                    JsonToPush[term] = timingList
                        
                    
                    for day in classDays:
                        timingJson = {
                            day: {
                                'start': classStart,
                                'end': classEnd
                            }
                        }
                        timingList += [JsonToPush]

                    JsonToPush[classTerm] = timingJson

                    classJsonList[len(classJsonList) - 1]['timing'] = JsonToPush
                    

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


