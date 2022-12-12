from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections
import json



subject = fromCampusPullSubjects('UBCO')

for sub in subject:
    c = fromSubjectPullSections(sub["code"], 'UBCO', True)

    with open(f'{sub["code"]}.json', 'w') as f:
        json.dump(c, f)

