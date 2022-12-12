from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections
import json



subject = fromCampusPullSubjects('UBCV')

codeList = []

for sub in subject:
    codeList += [sub['code']]


i = codeList.index('PHRM')

codeList = codeList[i:]


for code in codeList:
    c = fromSubjectPullSections(code, 'UBCV', True)

    with open(f'{code}V.json', 'w') as f:
        json.dump(c, f)




#c = fromCoursePullSections("DHYG", "106", 'UBCV')


#with open(f'BIOCV.json', 'w') as f:
#    json.dump(c, f)