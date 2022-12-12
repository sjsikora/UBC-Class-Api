from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections
import json


c = fromSubjectPullSections('PHYS', 'UBCO', True)


with open('temp.json', 'w') as f:
    json.dump(c, f)