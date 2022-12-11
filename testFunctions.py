from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections
import json


c = fromSubjectPullSections('PHYS', campus='UBCO', fulldetails=True)


#Invaild Course Combo: PHYS 111 001 on campus UBCO
#Invaild Course Combo: PHYS 301 001 on campus UBCO
#Invaild Course Combo: PHYS 304 001 on campus UBCO
#Invaild Course Combo: PHYS 331 001 on campus UBCO

#c = fromCoursePullSections('MATH', '100', 'UBCV', True)


with open('temp.json', 'w') as f:
    json.dump(c, f)